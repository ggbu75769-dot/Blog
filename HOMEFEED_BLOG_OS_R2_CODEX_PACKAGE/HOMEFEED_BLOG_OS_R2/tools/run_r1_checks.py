#!/usr/bin/env python3
"""Executable offline regressions; no paid calls, posting, DB or human assessment."""
from __future__ import annotations
from pathlib import Path
import sys,json,copy,re,subprocess,tempfile,hashlib,datetime,unicodedata
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from reference_core.canonical import canonical_bytes,content_hash,strict_json_loads
from reference_core.contracts import validate,Violation,assess_handoff,bundle_hash,instant,safe_path,fetch_guard,velocity_interval,plan_action
from reference_core.render import render_html,public_text,verify_export_files,build_reference_export
import yaml
RESULTS=[]
def check(name,fn,layer='OFFLINE_REFERENCE'):
    try:detail=fn();RESULTS.append({'name':name,'layer':layer,'status':'PASS','detail':str(detail or 'OK')})
    except Exception as e:RESULTS.append({'name':name,'layer':layer,'status':'FAIL','detail':f'{type(e).__name__}: {e}'})
def need(ok,detail='assertion failed'):
    if not ok:raise AssertionError(detail)
def reject(fn,contains=None):
    try:fn()
    except (Violation,ValueError,TypeError) as e:
        if contains:need(contains in str(e),f'wrong rejection: {e}')
        return str(e)
    raise AssertionError('invalid input accepted')
load=lambda p:json.loads((ROOT/p).read_text())
B=load('examples/r1/reference_bundle.json');NOW=instant('2026-09-15T12:00:00Z')
def rebind(b):
    b['gate']['target_content_hash']=content_hash(b['article']);b['gate']['evidence_bundle_hash']=bundle_hash(b)
def bad_bundle(mut,expected=None,resign=True,mode='REPLAY',now=NOW):
    b=copy.deepcopy(B);mut(b)
    if resign:rebind(b)
    d=assess_handoff(b,now,mode=mode);need(not d.allowed,'invalid handoff accepted')
    if expected:need(d.code==expected,f'expected {expected}, got {d.code}')
    return d.code

def schema_bad(name,path,mut,expected=None):
    v=load(path);mut(v);return reject(lambda:validate(name,v),expected)

# Original eight schema gaps: structural rejections or added semantic-layer checks.
check('B01 missing metric is not zero',lambda:schema_bad('MetricRow','examples/metric_row.json',lambda x:x.update(status='NOT_UPDATED',value=0)))
check('B02 unknown article type rejected',lambda:schema_bad('ArticleIR','examples/article_ir.json',lambda x:x.update(article_type='anything_at_all')))
check('B03 discriminator binds payload',lambda:reject(lambda:validate('AgentEnvelope',{'outcome':'produced','payload_type':'ResearchPack','payload':B['article'],'missing_items':[],'public_claims_added':[]})))
check('B04 evidence reversed interval rejected',lambda:schema_bad('EvidenceItem','examples/evidence_item.json',lambda x:x.update(valid_until='2000-01-01T00:00:00Z')))
check('B05 traversal filename rejected',lambda:schema_bad('ExportManifest','examples/export/manifest.json',lambda x:x['files'][0].update(path='../outside.txt')))
check('B06 executable citation URL rejected',lambda:reject(lambda:validate('PublicCitation',{**B['article']['public_citations'][0],'url':'javascript:alert(1)'})))
check('B07 unsupported first-person record rejected',lambda:reject(lambda:validate('Claim',{**B['claims'][0],'kind':'author_experience','author_record_id':None,'evidence_ids':[]})))
check('B08 reversed observation interval rejected',lambda:schema_bad('Observation','examples/observation.json',lambda x:x.update(value_interval={'lower':20,'upper':10})))
check('Writer cannot forge gate field',lambda:schema_bad('ArticleIR','examples/article_ir.json',lambda x:x.update(gate_report={'verdict':'PASS'})))
check('Produced response cannot be null',lambda:reject(lambda:validate('AgentEnvelope',{'outcome':'produced','payload_type':'ArticleIR','payload':None,'missing_items':[],'public_claims_added':[]})))
check('Correct discriminator accepted',lambda:validate('AgentEnvelope',{'outcome':'produced','payload_type':'ArticleIR','payload':B['article'],'missing_items':[],'public_claims_added':[]}))
check('Blog assignment cannot be null',lambda:reject(lambda:validate('RoutingDecision',{'opportunity_id':B['opportunity']['id'],'blog_id':None,'decision':'ASSIGN','audience_reason':'test','overlap_article_ids':[],'missing_items':[]})))
check('PASS cannot contain critical finding',lambda:reject(lambda:validate('GateReport',{**B['gate'],'findings':[{'code':'F','severity':'critical','block_ids':[],'claim_ids':[],'reason':'unverified','suggested_action':'hold'}]})))
check('Required human review cannot be missing',lambda:reject(lambda:validate('GateReport',{**B['gate'],'human_review_required':True,'human_reviewed_by':None})))
check('Title source hostname credentials rejected',lambda:reject(lambda:validate('PublicCitation',{**B['article']['public_citations'][0],'url':'https://user:pass@example.com/a'})))
check('Duplicate block id rejected',lambda:schema_bad('ArticleIR','examples/article_ir.json',lambda x:x['blocks'].append(copy.deepcopy(x['blocks'][0]))))
check('Orphan citation rejected',lambda:schema_bad('ArticleIR','examples/article_ir.json',lambda x:x['blocks'][0].update(citation_ids=['missing'])))
check('Visual required cannot be text-only',lambda:schema_bad('ContentBrief','examples/content_brief.json',lambda x:x.update(visual_required=True,text_only_allowed=True)))
check('Unknown canonical card id rejected',lambda:reject(lambda:validate('CardPlan',{'brief_id':B['brief']['id'],'options':[{'option_id':'one','title':'t','image_direction':'d','lead':'l','promises':['p'],'required_claim_ids':[],'risk_notes':[]}],'recommended_option_id':'missing','is_prediction':False})))
check('Source scope cannot be empty',lambda:schema_bad('SourceRegistration','examples/source_registration.json',lambda x:x.update(allowed_blog_ids=[])))
check('Unupdated null metric is accepted',lambda:validate('MetricRow',{**load('examples/metric_row.json'),'status':'NOT_UPDATED','value':None}))
check('Observed actual zero is accepted',lambda:validate('MetricRow',{**load('examples/metric_row.json'),'status':'OBSERVED','value':0}))
check('Negative pageviews rejected',lambda:schema_bad('MetricRow','examples/metric_row.json',lambda x:x.update(metric='pv',value=-1)))
check('Percent is not normalized ratio',lambda:schema_bad('MetricRow','examples/metric_row.json',lambda x:x.update(metric='referral_ratio',unit='ratio',value=30)))
check('Metric period cannot be reversed',lambda:schema_bad('MetricRow','examples/metric_row.json',lambda x:x.update(period_end='2000-01-01T00:00:00Z')))

# New cross-file binding and fail-closed handoff checks.
check('Valid reference bundle passes only as REPLAY',lambda:need(assess_handoff(B,NOW,mode='REPLAY').code=='REFERENCE_GATE_PASS'))
check('Replay cannot be labelled LIVE',lambda:need(assess_handoff(B,NOW,mode='LIVE').code=='REPLAY_CANNOT_BECOME_LIVE'))
check('Expired at exact boundary',lambda:bad_bundle(lambda b:None,'STALE_AT_HANDOFF',now=instant('2026-09-15T13:00:00Z')))
check('Article wording changed after review',lambda:bad_bundle(lambda b:b['article'].update(title='changed'),'CONTENT_CHANGED',resign=False))
check('Evidence summary changed after review',lambda:bad_bundle(lambda b:b['evidence'][0].update(summary='changed'),'REVIEW_CONTEXT_CHANGED',resign=False))
check('Source permission change invalidates review',lambda:bad_bundle(lambda b:b['sources'][0]['permissions'].update(send_to_model=False),'REVIEW_CONTEXT_CHANGED',resign=False))
check('New review still cannot allow denied transfer',lambda:bad_bundle(lambda b:b['sources'][0]['permissions'].update(send_to_model=False),'MODEL_TRANSFER_NOT_ALLOWED'))
check('Other blog evidence denied',lambda:bad_bundle(lambda b:b['evidence'][0].update(allowed_blog_ids=['11111111-1111-4111-8111-111111111111']),'EVIDENCE_SCOPE'))
check('Other blog raw snapshot denied',lambda:bad_bundle(lambda b:b['snapshots'][0].update(allowed_blog_ids=['11111111-1111-4111-8111-111111111111']),'SNAPSHOT_SCOPE'))
check('Other blog source registration denied',lambda:bad_bundle(lambda b:b['sources'][0].update(allowed_blog_ids=['11111111-1111-4111-8111-111111111111']),'SOURCE_SCOPE'))
check('Other tenant evidence denied',lambda:bad_bundle(lambda b:b['evidence'][0].update(tenant_id='11111111-1111-4111-8111-111111111111'),'RESOURCE_TENANT'))
check('Wrong revision report denied',lambda:bad_bundle(lambda b:b['gate'].update(revision_id='11111111-1111-4111-8111-111111111111'),'GATE_SCOPE'))
check('Wrong blog profile denied',lambda:bad_bundle(lambda b:b['profile'].update(id='11111111-1111-4111-8111-111111111111'),'PROFILE_SCOPE'))
check('Profile version changed denied',lambda:bad_bundle(lambda b:b['profile'].update(version=2),'PROFILE_VERSION'))
check('Brief from another opportunity denied',lambda:bad_bundle(lambda b:b['brief'].update(opportunity_id='11111111-1111-4111-8111-111111111111'),'OPPORTUNITY_SCOPE'))
check('Orphan factual claim denied',lambda:bad_bundle(lambda b:b['article']['blocks'][0].update(claim_ids=['11111111-1111-4111-8111-111111111111']),'CLAIM_ORPHAN'))
check('Conflict not treated as supported',lambda:bad_bundle(lambda b:b['claims'][0].update(support_status='CONFLICTING'),'CLAIM_UNSUPPORTED'))
check('Unavailable source not silently substituted',lambda:bad_bundle(lambda b:b['sources'][0].update(status='UNAVAILABLE'),'SOURCE_UNAVAILABLE'))
check('Future review cannot grant readiness',lambda:bad_bundle(lambda b:b['gate'].update(checked_at='2026-09-15T12:30:00Z'),'REVIEW_IN_FUTURE'))
check('Paused blog cannot keep producing',lambda:bad_bundle(lambda b:b['profile'].update(status='PAUSED'),'BLOG_NOT_ACTIVE'))
check('Expired source permission blocks download',lambda:bad_bundle(lambda b:b['sources'][0]['permissions'].update(expires_at='2026-09-15T11:30:00Z'),'STALE_AT_HANDOFF'))

check('Metadata-only source not body evidence',lambda:bad_bundle(lambda b:b['snapshots'][0].update(read_scope='metadata'),'EVIDENCE_READ_SCOPE_INSUFFICIENT'))
check('Future source snapshot denied',lambda:bad_bundle(lambda b:b['snapshots'][0].update(observed_at='2026-09-15T12:30:00Z'),'SNAPSHOT_FUTURE'))
def forge_live(b):
    b['article']['is_reference_example']=False;b['profile']['is_demo']=False;b['provenance']='LIVE'
check('Relabelled run cannot promote replay snapshot',lambda:bad_bundle(forge_live,'REPLAY_SNAPSHOT_IN_LIVE',mode='LIVE'))

# Cross-language canonicalization executes actual Python and Node implementations.
for vector in load('examples/r1/canonical_vectors.json'):
 def cross(v=vector):
    p=subprocess.run(['node',str(ROOT/'reference_core/canonical.mjs'),'--stdin'],input=json.dumps(v['value'],ensure_ascii=False),text=True,capture_output=True,check=True)
    out=json.loads(p.stdout);need(out['hash']==content_hash(v['value'])==v['expected_hash'],'digest mismatch');need(out['canonical'].encode()==canonical_bytes(v['value']),'byte mismatch')
    return out['hash']
 check('Python/JS '+vector['name'],cross,'CROSS_LANGUAGE_EXECUTED')
check('NFC key collision rejected',lambda:reject(lambda:canonical_bytes({'é':1,'e\u0301':2})))
check('Nonfinite value rejected',lambda:reject(lambda:canonical_bytes({'n':float('nan')})))
check('Unsafe integer rejected',lambda:reject(lambda:canonical_bytes({'n':9007199254740992})))
check('Fraction requires decimal string',lambda:reject(lambda:canonical_bytes({'n':0.3})))
check('Unpaired surrogate rejected',lambda:reject(lambda:canonical_bytes({'s':'\ud800'})))
check('Duplicate raw JSON key rejected',lambda:reject(lambda:strict_json_loads('{"a":1,"a":2}')))
check('JSON infinity rejected',lambda:reject(lambda:strict_json_loads('{"x":Infinity}')))

# Security boundary examples. No live DNS/HTTP performed.
for name,url,hosts,ips in [
 ('redirect to localhost','http://127.0.0.1/a',['127.0.0.1'],['127.0.0.1']),
 ('metadata IP','http://169.254.169.254/latest',['169.254.169.254'],['169.254.169.254']),
 ('host suffix attack','https://example.com.attacker.test/a',['example.com'],['93.184.216.34']),
 ('mixed DNS answers','https://example.com/a',['example.com'],['93.184.216.34','10.0.0.1']),
 ('IPv6 loopback','http://[::1]/a',['::1'],['::1'])]:
 check('Fetch guard '+name,lambda u=url,h=hosts,i=ips:reject(lambda:fetch_guard(u,h,i)))
check('Public allowlisted fetch plan accepted',lambda:fetch_guard('https://example.com/a',['example.com'],['93.184.216.34']))
for path in ['../a','/tmp/a','a\\b','a//b','CON.txt','a/../b','A:drive','name.','a\x00b']:
 check('Portable path rejects '+repr(path),lambda p=path:reject(lambda:safe_path(p)))

for path in ['a?.png','a*.txt','a|b','x#y.png','a%2Fb','a\x7fb','a<b']:
 check('Portable filename reserved '+repr(path),lambda p=path:reject(lambda:safe_path(p)))

# Rendering actually writes files, verifies hashes, and checks conservation/sanitization.
def render_cases():
    a=copy.deepcopy(B['article'])
    a['blocks'].append({'block_id':'TABLE','type':'table','headers':['조건','설명'],'rows':[['일부','<img src=x onerror=alert(1)>']],'claim_ids':[],'citation_ids':[]})
    a['blocks'].append({'block_id':'LIST','type':'list','ordered':True,'items':['첫 번째','두 번째'],'claim_ids':[],'citation_ids':[]})
    html=render_html(a);txt=public_text(a)
    need('<img src=x' not in html and '&lt;img src=x' in html,'unescaped markup')
    need('출처:' in txt and '[PUB01]' in txt,'citation omitted')
    need(html.count('data-block-id=')==len(a['blocks']),'block lost')
    need('첫 번째' in html and '일부' in txt,'content lost')
    files=build_reference_export(a,ROOT/'tests/adversarial/rendered_reference');need(len(files)==2)
    (ROOT/'tests/adversarial/rendered_reference/files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
    return 'IR → escaped HTML/TXT → on-disk digest check; not editor UAT'
check('Reference render conservation and escaping',render_cases,'LOCAL_FILE_EXECUTED')
check('Image without resolved file mapping rejected',lambda:reject(lambda:render_html({**B['article'],'blocks':[{'block_id':'IMG','type':'image','asset_id':'11111111-1111-4111-8111-111111111111','caption':'설명','alt_text':'설명','claim_ids':[],'citation_ids':[]}]})))
check('Unequal table columns rejected',lambda:reject(lambda:validate('ArticleIR',{**B['article'],'blocks':[{'block_id':'T','type':'table','headers':['A','B'],'rows':[['only one']],'claim_ids':[],'citation_ids':[]}]})))
def file_tamper():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d);(p/'a.txt').write_bytes(b'good');f={'path':'a.txt','size_bytes':4,'sha256':hashlib.sha256(b'good').hexdigest()};verify_export_files(p,[f]);(p/'a.txt').write_bytes(b'evil');return reject(lambda:verify_export_files(p,[f]),'FILE_HASH')
check('Post-render file corruption detected',file_tamper,'LOCAL_FILE_EXECUTED')
def file_link():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d);(p/'real').write_bytes(b'ok');(p/'link').symlink_to(p/'real');return reject(lambda:verify_export_files(p,[{'path':'link','size_bytes':2,'sha256':hashlib.sha256(b'ok').hexdigest()}]),'FILE_SYMLINK')
check('Symlink file is not exported',file_link,'LOCAL_FILE_EXECUTED')

# Momentum and queue actions: arithmetic rules, not predicted engagement.
o=load('examples/observation.json');o.update(source_updated_at=None,metric_status='OBSERVED',metric_value=12000,display_precision='rounded',value_interval={'lower':11500,'upper':12499},observed_at='2026-09-15T10:00:00Z')
p=copy.deepcopy(o);p.update(metric_value=13000,value_interval={'lower':12500,'upper':13499},observed_at='2026-09-15T11:00:00Z')
check('Rounded velocity remains an interval',lambda:need(velocity_interval(o,p)=={'status':'INTERVAL','lower':1.0,'upper':1999.0}))
check('Different observer sessions not a trend',lambda:need(velocity_interval(o,{**p,'observer_session':'different'})['status']=='INCOMPARABLE'))
check('Counter reset not negative momentum',lambda:need(velocity_interval(o,{**p,'metric_value':500,'value_interval':{'lower':450,'upper':549}})['status']=='COUNTER_RESET_OR_REVISION'))
check('Unknown observations not zero momentum',lambda:need(velocity_interval(o,{**p,'metric_status':'NOT_AVAILABLE','metric_value':None})['status']=='MISSING'))
baseargs={'signals_verified':True,'scheduled_event_verified':False,'brief_ready':True,'ready_count':0,'queue_limit':2,'budget_approved':True,'needs_paid_call':True,'user_can_post_before_expiry':True,'total_repairs':0}
for name,updates,expected in [
 ('ready candidate',{},'WRITE'),('no demand evidence',{'signals_verified':False},'RESEARCH'),
 ('scheduled not happened',{'signals_verified':False,'scheduled_event_verified':True},'PREPARE_ONLY'),
 ('manual backlog full',{'ready_count':2},'QUEUE_FULL_REFRESH_ONLY'),
 ('no paid budget',{'budget_approved':False},'BUDGET_REQUIRED'),
 ('user cannot post in time',{'user_can_post_before_expiry':False},'REFRAME_OR_DEFER'),
 ('global repair budget exhausted',{'total_repairs':6},'HUMAN_REVIEW')]:
 check('Planner '+name,lambda u=updates,e=expected:need(plan_action(**{**baseargs,**u})==e))

# Actual schema/API normalization, plus explicitly STATIC SQL invariants.
def api_sync():
    api=yaml.safe_load((ROOT/'api/openapi.yaml').read_text());d=load('schemas/domain.schema.json')['$defs']
    for n,v in d.items():need(json.dumps(v,sort_keys=True).replace('#/$defs/','#/components/schemas/')==json.dumps(api['components']['schemas'][n],sort_keys=True),n)
    create=api['components']['schemas']['ArticleCreate'];need('brief_id' not in create['required'])
    need(not any(re.search('/(publish|login|auto-post)(/|$)',p) for p in api['paths']))
    return f'{len(d)} embedded domain types identical; no public publisher'
check('API/schema parity and pre-brief create',api_sync,'STATIC_CONTRACT')
sql=(ROOT/'db/reference_schema.sql').read_text()
def ddl_links():
    tables={}
    # Structural scanner handles both one-line and multiline declarations.
    # It is intentionally not advertised as a full PostgreSQL parser.
    for m in re.finditer(r'CREATE TABLE (\w+)\s*\(',sql):
        start=m.end();depth=1;i=start;quoted=False
        while i<len(sql) and depth:
            char=sql[i]
            if char=="'":
                if quoted and i+1<len(sql) and sql[i+1]=="'":i+=2;continue
                quoted=not quoted
            elif not quoted:
                if char=='(':depth+=1
                elif char==')':depth-=1
            i+=1
        need(depth==0,'unbalanced table '+m.group(1));tables[m.group(1)]=sql[start:i-1]

    keys=lambda text:{tuple(x.strip() for x in raw.split(',')) for raw in re.findall(r'(?:UNIQUE|PRIMARY KEY)\s*\(([^)]+)\)',text)}|{('id',)}
    count=0
    for n,text in tables.items():
        for fields,target,tfields in re.findall(r'FOREIGN KEY\s*\(([^)]+)\)\s+REFERENCES\s+(\w+)\s*\(([^)]+)\)',text):
            need(target in tables,'missing table '+target);need(tuple(x.strip() for x in tfields.split(',')) in keys(tables[target]),n+' target unique missing '+target+' '+tfields);count+=1
    return f'{count} composite FK declarations structurally reference unique keys; PostgreSQL NOT_RUN'
check('Composite FK target declarations',ddl_links,'STATIC_DDL_ONLY')
for name,needle in [
 ('B11 parent same article','FOREIGN KEY (tenant_id, blog_id, article_id, parent_revision_id)'),
 ('B12 export exact article and revision','FOREIGN KEY (tenant_id, blog_id, article_id, revision_id, content_hash)'),
 ('B13 export exact reviewed revision','FOREIGN KEY (tenant_id, blog_id, revision_id, review_report_id, content_hash, review_bundle_hash)'),
 ('B15 opportunity before brief','opportunity_id uuid NOT NULL, brief_id uuid, state'),
 ('B16 synchronous idempotency','CREATE TABLE api_idempotency ('),
 ('B17 one current metric','CREATE UNIQUE INDEX one_current_metric')]:
 check(name,lambda n=needle:need(n in sql),'STATIC_DDL_ONLY')
for table in ['sources','source_snapshots','evidence_items']:
 check('B09/B10 scoped RLS '+table,lambda t=table:need('allowed_blog_ids &&' in re.search(r'CREATE POLICY tenant_blog_scope ON '+t+r'[^\n]+',sql).group(0)),'STATIC_DDL_ONLY')
check('RLS enabled for synchronous idempotency',lambda:need('ALTER TABLE api_idempotency FORCE ROW LEVEL SECURITY;' in sql),'STATIC_DDL_ONLY')

report={'release':'4.1.0-r1','executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':sum(r['status']=='PASS' for r in RESULTS),'failed':sum(r['status']=='FAIL' for r in RESULTS),'checks':RESULTS,'scope':'offline reference rules, actual Python/Node bytes, local render/files, static contract/DDL only','not_run':['PostgreSQL parse/migrations/RLS/transactions/concurrency','production HTTP auth and signed download integration','live source/model full pipeline','semantic factuality and image-rights human review','human naturalness and ready-to-post time study','Naver/Tistory editor UAT','homefeed and monthly-one-million efficacy']}
(ROOT/'reports/R1_REGRESSION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# R1 회귀검사 실행 결과','',f"PASS {report['passed']} / FAIL {report['failed']}",f"실행: {report['executed_at']}",'','코드가 실제 실행된 범위와 정적 DDL 검사를 layer로 구분한다. 제품 통합·사람 평가·조회수 검증은 아니다.','','| 검사 | 범위 | 결과 |','|---|---|---|']
lines += [f"| {x['name']} | {x['layer']} | {x['status']} |" for x in RESULTS]
lines += ['','## 미실행']+['- '+s for s in report['not_run']]
(ROOT/'reports/R1_REGRESSION.md').write_text('\n'.join(lines)+'\n')
print(f"R1 PASS {report['passed']} / FAIL {report['failed']}")
for x in RESULTS:
    if x['status']=='FAIL':print(x['name'],x['detail'])
sys.exit(1 if report['failed'] else 0)
