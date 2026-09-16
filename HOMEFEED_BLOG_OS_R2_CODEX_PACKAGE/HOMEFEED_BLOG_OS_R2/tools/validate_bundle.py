#!/usr/bin/env python3
"""Offline design-package validation; NOT an application/E2E/editor/viral-performance test.
Run from any cwd: python tools/validate_bundle.py [--root path]
Dependencies: jsonschema, PyYAML. Does not access network, credentials, DB or paid models.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import jsonschema
import yaml

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=ap.parse_args();root=args.root.resolve();results=[]
 def load(p):return json.loads((root/p).read_text(encoding='utf-8'))
 def check(name,fn):
  try:
   detail=fn()
   results.append({'id':f'DOC-{len(results)+1:03d}','name':name,'status':'PASS','detail':str(detail or 'OK')})
  except Exception as e:results.append({'id':f'DOC-{len(results)+1:03d}','name':name,'status':'FAIL','detail':f'{type(e).__name__}: {e}'})
 def need(cond,msg='invariant failed'):
  if not cond:raise AssertionError(msg)
 def count_atleast(values,n):need(len(values)>=n);return len(values)
 def refs(x):
  if isinstance(x,dict):
   if '$ref'in x:yield x['$ref']
   for v in x.values():yield from refs(v)
  elif isinstance(x,list):
   for v in x:yield from refs(v)
 def uniq(xs):need(len(xs)==len(set(xs)),'duplicates');return len(xs)
 sys.path.insert(0,str(root))
 from reference_core.canonical import canonical_bytes as canonical
 D=load('schemas/domain.schema.json')['$defs']; E=load('schemas/example_map.json')
 check('Domain Draft 2020-12 syntax',lambda:jsonschema.Draft202012Validator.check_schema({'$defs':D}))
 check('Domain refs resolve locally',lambda:[need(r.startswith('#/$defs/') and r.split('/')[-1] in D,r) for r in refs(D)])
 def validate(obj,name):
  schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$defs':D,'$ref':'#/$defs/'+name}
  jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(obj)
 for path,name in E['examples'].items():check('Example '+path,lambda p=path,n=name:validate(load('examples/'+p),n))
 for path,name in E['array_examples'].items():check('Array example '+path,lambda p=path,n=name:[validate(x,n) for x in load('examples/'+p)])
 for path in sorted((root/'schemas').glob('*.schema.json')):
  if path.name=='domain.schema.json':continue
  check('Schema wrapper '+path.name,lambda p=path:need(json.loads(p.read_text())['$ref'].split('/')[-1] in D))
 T=load('contracts/tasks.json');Q=load('contracts/requirements.json');A=load('contracts/acceptance_tests.json')
 # Support records in array or explicit top-level keys; contracts are deterministic.
 if isinstance(T,dict):T=T['tasks']
 if isinstance(Q,dict):Q=Q['requirements']
 if isinstance(A,dict):A=A['tests'] if 'tests'in A else A['acceptance_tests']
 tids={t['id'] for t in T};qids={q['id'] for q in Q};aids={a['id'] for a in A}
 check('Unique task IDs',lambda:uniq([t['id'] for t in T]));check('Unique requirement IDs',lambda:uniq([q['id'] for q in Q]));check('Unique acceptance IDs',lambda:uniq([a['id'] for a in A]))
 def task_links():
  for t in T:
   need(set(t['depends_on'])<=tids,t['id']+' missing dependency')
   need(set(t['requirements'])<=qids,t['id']+' requirement')
   need(set(t['acceptance_ids'])<=aids,t['id']+' AT')
   need((root/t['spec']).is_file(),t['spec'])
   need(t['status']=='NOT_STARTED','design task marked implemented')
  need(set().union(*(set(t['requirements']) for t in T))==qids,'uncovered requirement')
  need(set().union(*(set(t['acceptance_ids']) for t in T))==aids,'uncovered AT')
  return f'{len(T)} tasks / {len(Q)} requirements / {len(A)} planned acceptance cases'
 check('Task, requirement, acceptance traceability',task_links)
 def dag():
  order=(root/'contracts/task_order.txt').read_text().split()
  need(set(order)==tids,'order coverage');done=set()
  for tid in order:
   t=next(x for x in T if x['id']==tid);need(set(t['depends_on'])<=done,'dependency after task: '+tid);done.add(tid)
  return len(done)
 check('Topological task order',dag)
 check('Acceptance specs explicitly NOT_RUN',lambda:[need(x['execution_status']=='NOT_RUN' and x['design_only'] is True,x['id']) for x in A])
 def reverse_trace():
  taskmap={t['id']:t for t in T}; reqmap={q['id']:q for q in Q}
  for a in A:
   need(a['task_id'] in taskmap and a['requirement_id'] in reqmap,a['id'])
   need(a['id'] in taskmap[a['task_id']]['acceptance_ids'] and a['id'] in reqmap[a['requirement_id']]['acceptance_ids'],a['id']+' reverse link')
  return len(A)
 check('Bidirectional task/requirement/AT links',reverse_trace)
 C=load('contracts/editorial_benchmark_cases.json')
 check('24 editorial scenarios explicitly unexecuted',lambda:(need(len(C['cases'])==24),[need(c['execution_status']=='NOT_RUN' and c['required_behavior'] and c['forbidden_behavior'],c['id']) for c in C['cases']]))
 check('Reference implementation exists but not the product app',lambda:[need((root/p).is_file(),p) for p in ['reference_core/canonical.py','reference_core/canonical.mjs','reference_core/contracts.py','reference_core/render.py','tools/run_r1_checks.py']])
 states=load('contracts/states.json');valid=set(states['article_states'])
 check('All state transitions are defined',lambda:[need(k in valid and set(v)<=valid,k) for k,v in states['transitions'].items()])
 check('HANDOFF_READY not a publication state',lambda:need('HANDOFF_READY'in valid and not {'PUBLISHED','PUBLISHING'}&valid))
 defaults=load('contracts/defaults.json')
 check('Manual-only and replay defaults',lambda:need(defaults['public_posting_enabled'] is False and defaults['mode']=='REPLAY'))
 check('Single primary-blog calendar-month target',lambda:need(defaults['primary_goal']=={'platform':'naver','scope':'single_primary_blog','metric':'calendar_month_pv','target':1000000}))
 check('Paid access disabled without approved budget',lambda:need(defaults['budget']['monthly_budget_minor'] is None and defaults['budget']['require_approved_budget_for_paid_call']))
 check('Ranking weights sum to one, not a probability',lambda:need(abs(sum(defaults['ranking']['weights'].values())-1)<1e-9 and defaults['ranking']['not_a_probability']))
 check('Bounded lease heartbeat',lambda:need(0<defaults['lease']['heartbeat_seconds']<defaults['lease']['seconds']))
 api=yaml.safe_load((root/'api/openapi.yaml').read_text());ops=[(p,m,v) for p,ps in api['paths'].items() for m,v in ps.items() if m in {'get','post','patch','put','delete'}]
 check('OpenAPI version and unique operation IDs',lambda:(need(api['openapi']=='3.1.0'),uniq([o['operationId'] for _,_,o in ops])))
 check('OpenAPI schema references resolve',lambda:[need(r.startswith('#/components/schemas/') and r.split('/')[-1] in api['components']['schemas'],r) for r in refs(api)])
 def api_params():
  for p,m,o in ops:
   actual={a['name'] for a in o.get('parameters',[]) if a['in']=='path'}
   need(actual==set(re.findall(r'\{(\w+)\}',p)),p)
   if m in {'post','patch','put','delete'}:need(any(a['name']=='Idempotency-Key' and a.get('required') for a in o.get('parameters',[])),p)
  return len(ops)
 check('API path params and write idempotency headers',api_params)
 check('No platform publisher routes',lambda:[need(not re.search(r'/(publish|login|auto-post)(/|$)',p),p) for p in api['paths']])
 check('Writer contract cannot carry a server gate',lambda:need('gate_report'not in D['ArticleIR']['properties'] and D['ArticleIR']['additionalProperties'] is False and D['GateReport']['properties']['issuer']=={'const':'review_service'}))
 article=load('examples/article_ir.json');claims=load('examples/claims.json');brief=load('examples/content_brief.json');claimids={x['id'] for x in claims};citids={x['id'] for x in article['public_citations']}
 check('Example scope isolation and brief link',lambda:(need(article['tenant_id']==brief['tenant_id'] and article['blog_id']==brief['blog_id'] and article['brief_id']==brief['id']),[need(x['tenant_id']==article['tenant_id'] and x['blog_id']==article['blog_id']) for x in claims]))
 check('All article claim/citation refs exist',lambda:[need(set(b['claim_ids'])<=claimids and set(b['citation_ids'])<=citids,b['block_id']) for b in article['blocks']])
 check('Unique article blocks',lambda:uniq([b['block_id'] for b in article['blocks']]))
 check('Table rows match headers',lambda:[need(all(len(row)==len(b['headers']) for row in b['rows']),b['block_id']) for b in article['blocks'] if b['type']=='table'])
 check('Reference text-only example not fake image-ready',lambda:need(article['is_reference_example'] is True and brief['text_only_allowed'] and not brief['visual_required'] and not brief['required_asset_ids']))
 public='\n'.join((root/'examples/export'/p).read_text() for p in ['article.txt','article.md'])
 check('Public reference has no working placeholders or tool tokens',lambda:need(not re.search(r'\[TODO\]|\{\{.*?\}\}|여기에.*삽입||BEGIN PRIVATE|api[_-]?key\s*=',public,re.I)))
 m=load('examples/export/manifest.json');review=load('examples/review_findings.json')
 ch=hashlib.sha256(canonical(article)).hexdigest()
 check('Immutable IR hash matches manifest and review',lambda:need(ch==m['content_hash']==review['input_content_hash']))
 def manifests():
  for f in m['files']:
   p=(root/'examples/export'/f['path']).resolve();need(p.is_relative_to((root/'examples/export').resolve()),'path escape')
   b=p.read_bytes();need(len(b)==f['size_bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path'])
  need(m['status']=='REFERENCE_EXAMPLE' and m['public_posting_performed'] is False)
  return len(m['files'])
 check('Export reference file sizes, hashes, scope',manifests)
 sources=load('contracts/sources.json');sources=sources['sources'] if isinstance(sources,dict) else sources
 check('Source register IDs unique',lambda:uniq([s['id'] for s in sources]))
 def source_fields():
  for s in sources:need('url'in s and s['url'].startswith('https://') and ('limits'in s or 'limitations'in s),s['id'])
  return len(sources)
 check('Source provenance and limitation fields',source_fields)
 sql=(root/'db/reference_schema.sql').read_text();sqltables=re.findall(r'CREATE TABLE (\w+)\s*\(',sql)
 check('SQL table names unique (text structure only)',lambda:uniq(sqltables))
 check('Reference DDL clearly unapplied',lambda:need('NOT APPLIED OR TESTED AGAINST POSTGRESQL'in sql))
 check('Each reference table enables and forces RLS (text only)',lambda:[need('ALTER TABLE '+t+' ENABLE ROW LEVEL SECURITY;'in sql and 'ALTER TABLE '+t+' FORCE ROW LEVEL SECURITY;'in sql,t) for t in sqltables])
 check('Durable job/budget/fencing fields exist (text only)',lambda:[need(s in sql,s) for s in ['fencing_token','SKIP LOCKED','budget_reservations','call_intents','overrun_micro','article_current_revision_fk']])
 # Deliberately bad schema payloads; these only exercise schema rejection, not service safety semantics.
 def rejects(name,mut):
  try:validate(mut,name)
  except jsonschema.ValidationError:return 'invalid fixture rejected'
  raise AssertionError('invalid fixture accepted')
 bad=json.loads(json.dumps(article));bad['gate_report']={'verdict':'PASS'}
 check('Negative schema: writer cannot add gate_report',lambda:rejects('ArticleIR',bad))
 bad2=json.loads(json.dumps(article));bad2['blog_id']='not-a-uuid'
 check('Negative schema: invalid blog UUID',lambda:rejects('ArticleIR',bad2))
 bad3=json.loads(json.dumps(m));bad3['public_posting_performed']=True
 check('Negative schema: export cannot claim public posting',lambda:rejects('ExportManifest',bad3))
 bad4=json.loads(json.dumps(load('examples/opportunity.json')));bad4['not_a_probability']=False
 check('Negative schema: opportunity not a calibrated probability',lambda:rejects('Opportunity',bad4))
 check('Required implementation handoff files exist',lambda:[need((root/p).is_file(),p) for p in ['README.md','CODEX_START_HERE.md','AGENTS.md','.env.example','docs/17_TASK_SPECIFICATIONS.md','docs/18_ACCEPTANCE_TESTS.md','prompts/08_FINAL_REVIEW.md']])
 check('Documentation sequence 00 through 38 exists',lambda:need({p.name[:2] for p in (root/'docs').glob('*.md')}=={f'{i:02d}' for i in range(39)}))
 check('No private credentials or artifact tool citation tokens in authored docs',lambda:[need(not re.search(r'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|',p.read_text(encoding='utf-8')),str(p)) for p in (root/'docs').glob('*.md')])
 report={'artifact':'HOMEFEED BLOG OS R2 base-compatible design package','validation_kind':'OFFLINE_DOCUMENT_AND_SCHEMA_CHECKS_ONLY','executed_at':datetime.now(timezone.utc).isoformat(),'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']=='FAIL' for r in results),'checks':results,'not_run':['application implementation','PostgreSQL parse/migration/RLS/concurrency','LIVE source/model pipeline','image-generation/asset-render pipeline','Naver/Tistory editor UAT','human naturalness blind study','homefeed exposure/growth validation'],'planned_product_acceptance_cases':len(A)}
 (root/'reports').mkdir(exist_ok=True)
 (root/'reports/DOCUMENT_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# 문서·스키마 검증 실행 보고서','',f"실행 시각: {report['executed_at']}",f"실제 실행 결과: PASS {report['passed']} / FAIL {report['failed']}.",'','**제품 기능·DB·실제 블로그·조회수 시험의 통과 결과가 아니다.**','',f'별도 제품 인수시험 {len(A)}개는 설계만 작성했으며 모두 NOT_RUN 상태다.','','| ID | 검사 | 결과 |','|---|---|---|']
 for x in results:lines.append(f"| {x['id']} | {x['name']} | {x['status']} |")
 lines+=['','## 미실행 영역']+['- '+x for x in report['not_run']]
 failures=[x for x in results if x['status']=='FAIL']
 if failures:lines+=['','## 수정 필요']+[x['name']+': '+x['detail'] for x in failures]
 (root/'reports/DOCUMENT_VALIDATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(f"PASS {report['passed']} / FAIL {report['failed']} / planned product AT {len(A)} NOT_RUN")
 for x in failures:print(x['name'],x['detail'])
 return 1 if failures else 0
if __name__=='__main__':sys.exit(main())
