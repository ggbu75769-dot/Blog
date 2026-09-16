#!/usr/bin/env python3
"""Inspect an explicitly supplied legacy package. Static/schema findings are not production exploits."""
from pathlib import Path
import json,copy,subprocess,hashlib,unicodedata,re,datetime
import jsonschema
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--baseline',type=Path,required=True,help='Unpacked 4.0.0-final.1 package')
parser.add_argument('--output',type=Path,required=True,help='New probe report; archived reports are not overwritten automatically')
args=parser.parse_args()
base=args.baseline.resolve()
if not (base/'schemas/domain.schema.json').is_file():parser.error('baseline package not found')
D=json.loads((base/'schemas/domain.schema.json').read_text())['$defs']
load=lambda p:json.loads((base/p).read_text())
rows=[]
def schema_probe(id,name,obj,desc):
 v=jsonschema.Draft202012Validator({'$defs':D,'$ref':'#/$defs/'+name},format_checker=jsonschema.FormatChecker())
 errors=list(v.iter_errors(obj));rows.append({'id':id,'kind':'NEGATIVE_SCHEMA_PROBE','finding':desc,'legacy_result':'ACCEPTED' if not errors else 'REJECTED','production_exploit_proven':False})
m=load('examples/metric_row.json');m.update(status='NOT_UPDATED',value=0);schema_probe('B01','MetricRow',m,'미갱신과 숫자0의 모순')
a=load('examples/article_ir.json');a['article_type']='anything_at_all';schema_probe('B02','ArticleIR',a,'정의되지 않은 글 형식')
env={'outcome':'produced','payload_type':'ResearchPack','payload':a,'missing_items':[],'public_claims_added':[]};schema_probe('B03','AgentEnvelope',env,'타입 라벨과 실제 payload 불일치')
e=load('examples/evidence_item.json');e['valid_until']='2000-01-01T00:00:00Z';schema_probe('B04','EvidenceItem',e,'검증보다 먼저 만료되는 근거')
m=load('examples/export/manifest.json');m['files'][0]['path']='../outside.txt';schema_probe('B05','ExportManifest',m,'상위 경로로 탈출하는 파일명')
c=copy.deepcopy(load('examples/article_ir.json')['public_citations'][0]);c['url']='javascript:alert(1)';schema_probe('B06','PublicCitation',c,'실행 가능한 비HTTP 출처 URL')
cl=load('examples/claims.json')[0];cl.update(kind='author_experience',author_record_id=None,evidence_ids=[],support_status='SUPPORTED');schema_probe('B07','Claim',cl,'근거·경험기록 없는 SUPPORTED 체험')
ob=load('examples/observation.json');ob['value_interval']={'lower':20,'upper':10};schema_probe('B08','Observation',ob,'관측 구간 상하한 역전')
sql=(base/'db/reference_schema.sql').read_text()
for id,table,needle,desc in [
('B09','evidence_items','allowed_blog_ids','근거 RLS가 블로그 allowlist를 검사하지 않음'),
('B10','source_snapshots','allowed_blog_ids','공유 원문에 블로그별 범위가 없음')]:
 policy=re.search(r'CREATE POLICY [^\n]+ ON '+table+r' [^\n]+',sql).group(0)
 rows.append({'id':id,'kind':'STATIC_DDL_INSPECTION','finding':desc,'legacy_result':'MISSING' if needle not in policy else 'PRESENT','excerpt':policy,'database_executed':False})
for id,table,needle,desc in [
('B11','article_revisions','FOREIGN KEY (tenant_id, blog_id, article_id, parent_revision_id)','부모 버전 FK가 같은 article을 강제하지 않음'),
('B12','exports','FOREIGN KEY (tenant_id, blog_id, article_id, revision_id)','출력의 article과 revision을 별도 FK로만 검사함'),
('B13','exports','FOREIGN KEY (tenant_id, blog_id, revision_id, review_report_id)','출력의 검수보고서와 revision 결속이 없음')]:
 table_sql=re.search(r'CREATE TABLE '+table+r'\s*\(.*?\n\);',sql,re.S).group(0)
 rows.append({'id':id,'kind':'STATIC_DDL_INSPECTION','finding':desc,'legacy_result':'MISSING' if needle not in table_sql else 'PRESENT','database_executed':False})
value={'value':1.0}
py=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
js=subprocess.check_output(['node','-e','process.stdout.write(JSON.stringify({value:1.0}))'],text=True)
rows.append({'id':'B14','kind':'CROSS_LANGUAGE_EXECUTED','finding':'정수값을 가진 float의 Python/JS 직렬화 차이','legacy_result':'MISMATCH' if py!=js else 'MATCH','python_bytes':py,'javascript_bytes':js})
rows.append({'id':'B15','kind':'STATIC_CONTRACT_INSPECTION','finding':'articles.brief_id NOT NULL인데 사전 조사 상태도 Article에 포함됨','legacy_result':'INCONSISTENT_LIFECYCLE','database_executed':False})
rows.append({'id':'B16','kind':'STATIC_DDL_INSPECTION','finding':'동기 API의 idempotency 저장 계약은 있으나 전용 DDL 없음','legacy_result':'MISSING' if 'CREATE TABLE api_idempotency (' not in sql else 'PRESENT','database_executed':False})
rows.append({'id':'B17','kind':'STATIC_DDL_INSPECTION','finding':'같은 metric 논리키의 current가 두 개일 수 있는 DDL','legacy_result':'MISSING' if 'CREATE UNIQUE INDEX one_current_metric' not in sql else 'PRESENT','database_executed':False})
report={'baseline_package':'4.0.0-final.1','executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_document_checks':'not re-executed by this probe; see the separately archived baseline report','scope':'schema negatives, cross-language bytes, static DDL; NOT production vulnerability test','probes':rows}
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
