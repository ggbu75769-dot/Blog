from pathlib import Path
import unittest,json,copy,sys,tempfile,re
from dataclasses import asdict
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from editorial_r2.reader import reader_html,reader_text,lint_article,validate_editorial_review,next_action,write_preview
from reference_core.canonical import content_hash
from reference_core.contracts import Violation
from jsonschema import ValidationError,Draft202012Validator
A=json.loads((ROOT/'examples/editorial_r2/01_DATALAB/article_ir.json').read_text())
POL={'writer_id':'writer','authorized_reviewer_ids':['editor'],'reader_calibration_status':'NOT_RUN','review_kinds_by_reviewer':{'editor':['REFERENCE_ANNOTATION','MODEL_SEMANTIC_REVIEW']}}
def review(a):
 return {'schema_version':'r2.editorial.1','article_id':a['id'],'revision_id':a['revision_id'],'blog_id':a['blog_id'],'content_hash':content_hash(a),'reviewer_id':'editor','review_kind':'REFERENCE_ANNOTATION','verdict':'PASS','dimensions':dict.fromkeys(['payoff','promise','coherence','voice','specificity'],'PASS'),'payoffs':[{'id':'P1','kind':'worked_example','reader_change':'정규화 그래프 최고점만으로 원래 규모를 비교할 수 없음을 이해한다.','anchors':[{'block_id':'D05','quote':'10 → 20'},{'block_id':'D06','quote':'두 묶음은 크기가 전혀 다른데 바뀐 숫자는 같습니다.'}],'source_ids':['NV-DATA'],'comparison_scope':'이 세션 R1 예제와 비교; 독립 독자평가 아님'}],'findings':[],'scope_note':'Reference annotation for contract tests only.'}
class EditorialTests(unittest.TestCase):
 def setUp(self): self.a=copy.deepcopy(A);self.r=review(self.a);self.p=copy.deepcopy(POL)
 def validate(self):return validate_editorial_review(self.a,self.r,self.p)
 def reject(self):
  with self.assertRaises((Violation,ValueError,ValidationError)):self.validate()
 def test_valid_references(self):self.validate()
 def test_other_article(self):self.r['article_id']='other';self.reject()
 def test_other_revision(self):self.r['revision_id']='other';self.reject()
 def test_other_blog(self):self.r['blog_id']='other';self.reject()
 def test_stale_hash(self):self.a['title']+=' 변경';self.reject()
 def test_anchor_not_real(self):self.r['payoffs'][0]['anchors'][0]['quote']='존재하지않는 근거';self.reject()
 def test_anchor_missing_block(self):self.r['payoffs'][0]['anchors'][0]['block_id']='no';self.reject()
 def test_unknown_source(self):self.r['payoffs'][0]['source_ids']=['invented'];self.reject()
 def test_missing_source(self):self.r['payoffs'][0]['source_ids']=[];self.reject()
 def test_self_review(self):self.r['reviewer_id']='writer';self.reject()
 def test_unauthorized_reviewer(self):self.r['reviewer_id']='stranger';self.reject()
 def test_empty_value_does_not_pass(self):self.r['payoffs']=[];self.reject()
 def test_empty_answer_dimension(self):self.r['dimensions']['payoff']='UNKNOWN';self.reject()
 def test_major_finding_cannot_pass(self):
  self.r['findings']=[{'code':'MISSING_PAYOFF','severity':'major','anchors':[{'block_id':'TITLE','quote':self.a['title']}],'reason':'test','repair':'RESEARCH'}];self.reject()
 def test_unknown_property(self):self.r['ai_probability']=0;self.reject()
 def test_fake_human_review_kind(self):self.r['review_kind']='SIMULATED_HUMAN_VERIFIED';self.reject()
 def test_unknown_fact_stops(self):self.assertEqual(next_action(self.a,self.r,self.p,'UNKNOWN')['action'],'FACT_REVIEW')
 def test_no_review_stops(self):self.assertEqual(next_action(self.a,None,self.p,'VERIFIED')['action'],'EDITORIAL_REVIEW')
 def test_reference_not_production(self):self.assertEqual(next_action(self.a,self.r,self.p,'VERIFIED')['action'],'REFERENCE_PREVIEW_ONLY')
 def test_human_calibration_not_invented(self):
  self.a['is_reference_example']=False;self.r=review(self.a);self.r['review_kind']='MODEL_SEMANTIC_REVIEW';self.assertEqual(next_action(self.a,self.r,self.p,'VERIFIED')['action'],'OWNER_REVIEW')
 def test_r1_gate_still_needed(self):
  self.a['is_reference_example']=False;self.r=review(self.a);self.r['review_kind']='MODEL_SEMANTIC_REVIEW';self.p['reader_calibration_status']='VALIDATED';v=next_action(self.a,self.r,self.p,'VERIFIED');self.assertEqual(v['action'],'HANDOFF_GATE_REQUIRED');self.assertFalse(v['auto_ready'])
 def test_unknown_dimension_not_passed(self):
  self.r['dimensions']['voice']='UNKNOWN';self.r['verdict']='UNKNOWN';self.assertEqual(next_action(self.a,self.r,self.p,'VERIFIED')['action'],'EDITORIAL_REVIEW')
 def test_missing_content_goes_research(self):
  self.r['verdict']='FAIL';self.r['dimensions']['payoff']='FAIL';self.r['findings']=[{'code':'MISSING_PAYOFF','severity':'major','anchors':[{'block_id':'TITLE','quote':self.a['title']}],'reason':'missing substantive answer','repair':'RESEARCH'}];self.assertEqual(next_action(self.a,self.r,self.p,'VERIFIED')['action'],'RESEARCH')
 def test_wording_only_local_edit(self):
  self.r['verdict']='FAIL';self.r['dimensions']['voice']='FAIL';self.r['findings']=[{'code':'REPEATED_CLOSING','severity':'major','anchors':[{'block_id':'TITLE','quote':self.a['title']}],'reason':'wording only','repair':'LOCAL_EDIT'}];self.assertEqual(next_action(self.a,self.r,self.p,'VERIFIED')['action'],'LOCAL_EDIT')
 def test_reader_text_no_id(self):
  text=reader_text(self.a);self.assertNotIn('NV-DATA',text);self.assertIn('NAVER Developers',text);self.assertIn('https://developers.naver.com',text)
 def test_reader_html_no_public_id(self):self.assertNotIn('NV-DATA',reader_html(self.a))
 def test_every_text_is_preserved(self):
  text=reader_text(self.a)
  for b in self.a['blocks']:
   if 'text' in b:self.assertIn(b['text'],text)
 def test_table_preserved(self):self.assertIn('1,000 → 2,000',reader_text(self.a));self.assertIn('<table>',reader_html(self.a))
 def test_xss_escaped(self):
  self.a['blocks'][0]['text']='보안 문자열 <img src=x onerror=alert(1)> 입니다.';h=reader_html(self.a);self.assertNotIn('<img src=x',h);self.assertIn('&lt;img',h)
 def test_no_warnings_means_no_ai_verdict(self):
  result=[asdict(x) for x in lint_article(self.a)];self.assertFalse(any('ai_probability' in x for x in result))
 def test_duplicate_warning(self):
  b=copy.deepcopy(self.a['blocks'][0]);b['block_id']='duplicate';self.a['blocks'].append(b);self.assertIn('EXACT_PARAGRAPH_DUPLICATE',[x.code for x in lint_article(self.a)])
 def test_generic_warning_not_block(self):
  self.a['blocks'][0]['text']='현대 사회에서 삶의 질을 높이는 방법을 설명합니다.';f=lint_article(self.a);self.assertTrue(any(x.code=='GENERIC_PHRASE' for x in f));self.assertFalse(any(x.severity=='block' for x in f))
 def test_fake_popularity_requires_review(self):
  self.a['blocks'][0]['text']='요즘 다들 이 기능을 사용합니다.';self.assertIn('CLAIM_OR_POPULARITY_REVIEW',[x.code for x in lint_article(self.a)])
 def test_missing_image_marker_block(self):
  self.a['blocks'][0]['text']='여기에 사진을 넣으세요.';self.assertTrue(any(x.severity=='block' for x in lint_article(self.a)))
 def test_internal_work_note_block(self):
  self.a['blocks'][0]['text']='reader_value: 좋은 판단을 돕는 문장';self.assertIn('INTERNAL_NOTES_VISIBLE',[x.code for x in lint_article(self.a)])
 def test_control_character_does_not_hide_marker(self):
  self.a['blocks'][0]['text']='read\u200ber_value: 메모';self.assertIn('INTERNAL_NOTES_VISIBLE',[x.code for x in lint_article(self.a)])
 def test_lint_not_universal_first_person_ban(self):
  self.a['blocks'][0]['text']='직접 사용한 기록을 제공받기 전에는 사용 후기를 만들지 않습니다.';self.assertFalse(any(x.severity=='block' for x in lint_article(self.a)))
 def test_needed_terms_not_duplicate_paragraph(self):
  self.a['blocks'][0]['text']='USB-C와 USB-C 케이블은 확인해야 합니다.';self.assertNotIn('EXACT_PARAGRAPH_DUPLICATE',[x.code for x in lint_article(self.a)])
 def test_export_does_not_create_approval(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);r=write_preview(self.a,p);self.assertIsNone(r['viral_probability']);self.assertFalse(r['naturalness_verified_by_code']);self.assertTrue((p/'article.txt').exists())
 def test_sample_labels_honest(self):
  for p in (ROOT/'examples/editorial_r2').glob('*/sample_status.json'):
   s=json.loads(p.read_text());self.assertEqual(s['trend_validation'],'NOT_RUN');self.assertFalse(s['live_pipeline_generated']);self.assertEqual(s['human_blind_review'],'NOT_RUN')
 def test_schema_syntax(self):Draft202012Validator.check_schema(json.loads((ROOT/'schemas/r2/editorial_review.schema.json').read_text()))
 def test_work_trace_and_unrun(self):
  d=json.loads((ROOT/'contracts/r2/work.json').read_text());done=set();a={x['id'] for x in d['acceptance_tests']}
  self.assertEqual(len(d['tasks']),10);self.assertEqual(len(a),30)
  for t in d['tasks']:
   self.assertTrue(set(t['depends_on'])<=done);self.assertTrue(set(t['acceptance_ids'])<=a);self.assertEqual(t['implementation_status'],'NOT_STARTED');done.add(t['id'])
  self.assertTrue(all(t['execution_status']=='NOT_RUN' for t in d['acceptance_tests']))
 def test_new_api_has_no_publishing(self):
  import yaml
  d=yaml.safe_load((ROOT/'api/r2/editorial.openapi.yaml').read_text());self.assertTrue(all('/publish' not in x for x in d['paths']))
 def test_formula_example_not_fake_measurement(self):
  t=reader_text(self.a);self.assertIn('가상 숫자',t);self.assertIn('실제 검색량이나 API 응답이 아닙니다',t);self.assertEqual(10/20*100,50);self.assertEqual(1000/2000*100,50)
 def test_real_blind_label_requires_actual_authorized_role(self):
  self.r['review_kind']='BLIND_READER_REVIEW';self.reject()
 def test_reference_annotation_cannot_be_promoted(self):
  self.a['is_reference_example']=False;self.r=review(self.a);self.p['reader_calibration_status']='VALIDATED';self.assertEqual(next_action(self.a,self.r,self.p,'VERIFIED')['action'],'REFERENCE_PREVIEW_ONLY')
 def test_duplicate_sources_share_public_number(self):
  c=copy.deepcopy(self.a['public_citations'][0]);c['id']='alias';self.a['public_citations'].append(c);self.a['blocks'][0]['citation_ids']=['alias'];h=reader_html(self.a);self.assertIn('href="#source-1"',h);self.assertNotIn('href="#source-2"',h)
 def test_final_critical_exception_preserved(self):
  a=json.loads((ROOT/'examples/editorial_r2/02_GOOGLE_PHOTOS/article_ir.json').read_text());t=reader_text(a);self.assertIn('기본 갤러리에서는 그 사진을 볼 수 없습니다',t);self.assertIn('오프라인',t);self.assertIn('삭제를 미루세요',t)
if __name__=='__main__':unittest.main()
