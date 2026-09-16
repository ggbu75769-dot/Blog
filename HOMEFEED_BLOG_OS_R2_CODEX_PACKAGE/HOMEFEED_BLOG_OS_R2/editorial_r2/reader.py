"""Reader-facing output and narrow quality triage.

Structural checks only. Cannot determine truth, human authorship, originality,
readability, or viral potential. Semantic reviews must be obtained separately.
All inputs to a production decision must come from authenticated internal services.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass,asdict
from html import escape
from pathlib import Path
import json,re,unicodedata,hashlib
from typing import Any,Iterable
from reference_core.contracts import validate,require,web_url,safe_path
from reference_core.canonical import content_hash

@dataclass(frozen=True)
class Finding:
    code:str
    severity:str
    block_ids:tuple[str,...]
    excerpt:str
    action:str

def normal(s:str)->str:
    return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFC',s) if unicodedata.category(c)!='Cf')).strip()

def block_text(b:dict)->str:
    if b['type'] in ('paragraph','heading','quote','callout'):return b['text']
    if b['type']=='list':return '\n'.join(b['items'])
    if b['type']=='table':return '\n'.join([' | '.join(b['headers'])]+[' | '.join(r) for r in b['rows']])
    if b['type']=='image':return b['caption']
    raise ValueError('UNSUPPORTED_BLOCK')

PLACEHOLDERS=re.compile(r'(?:\[\[(?:TODO|IMAGE|SOURCE)\b[^\]]*\]\]|\{\{[^}]+\}\}|여기에\s*(?:사진|이미지|본문|출처)\s*(?:을|를)?\s*(?:넣|입력)|(?:^|\n)\s*출처:\s*(?:PUB|CLAIM|SRC)[-_]?\d+)')
INTERNAL=re.compile(r'\b(?:claim_ids|citation_ids|reader_value|AgentEnvelope|evidence_bundle_hash)\b|(?:cite|filecite)')
PROMO=re.compile(r'삶의 질을 (?:높|향상)|현대 사회에서|완벽한 선택|다양한 장점을|이번 포스팅에서는|지금까지 알아보았습니다')
FAKECERTAINTY=re.compile(r'(?:누구나|무조건|100%)\s*(?:성공|해결|효과|가능)|바이럴\s*(?:보장|확률\s*\d)|대부분의 사람들은|요즘\s*다들')

def lint_article(article:dict)->list[Finding]:
    validate('ArticleIR',article)
    findings=[];seen={}
    units=[{'block_id':'TITLE','type':'paragraph','text':article['title']}]+article['blocks']
    for b in units:
        raw=block_text(b);text=normal(raw);bid=b['block_id']
        for code,pattern in [('INCOMPLETE_COPY',PLACEHOLDERS),('INTERNAL_NOTES_VISIBLE',INTERNAL)]:
            if m:=pattern.search(text):findings.append(Finding(code,'block',(bid,),m.group(0),'REPAIR_EXPORT'))
        if b['type'] in ('paragraph','callout','quote') and len(text)>45:
            if text in seen:findings.append(Finding('EXACT_PARAGRAPH_DUPLICATE','review',(seen[text],bid),text[:180],'LOCAL_EDIT'))
            else:seen[text]=bid
        if m:=PROMO.search(text):findings.append(Finding('GENERIC_PHRASE','review',(bid,),m.group(0),'EDITORIAL_REVIEW'))
        if m:=FAKECERTAINTY.search(text):findings.append(Finding('CLAIM_OR_POPULARITY_REVIEW','review',(bid,),m.group(0),'CHECK_EVIDENCE'))
    # These findings are warnings, not a probabilistic AI detector.
    return findings


def _citation_map(article:dict)->dict:
    result={c['id']:c for c in article['public_citations']}
    require(len(result)==len(article['public_citations']),'CITATION_ID_DUPLICATE')
    for c in result.values():web_url(c['url'])
    for b in article['blocks']:
        require(set(b['citation_ids'])<=set(result),'CITATION_UNRESOLVED')
    return result


def _citation_numbers(cmap:dict)->dict:
    by_key={};numbers={}
    for cid,c in cmap.items():
        key=(c['publisher'],c['title'],c['url'])
        if key not in by_key:by_key[key]=len(by_key)+1
        numbers[cid]=by_key[key]
    return numbers

def reader_text(article:dict)->str:
    """No internal citation tokens; each cited block has a normal numbered footnote.
    Reference links are complete in a deduplicated bibliography. Do not silently
    suppress facts/conditions/quotes to improve appearance.
    """
    validate('ArticleIR',article);cmap=_citation_map(article)
    numbers=_citation_numbers(cmap)
    out=[article['title'],'']
    for b in article['blocks']:
        if b['type']=='list':out.extend((f'{i}. ' if b['ordered'] else '• ')+x for i,x in enumerate(b['items'],1))
        else:out.append(block_text(b))
        if b['citation_ids']:
            out[-1]+=' '+''.join(f'[{numbers[c]}]' for c in dict.fromkeys(b['citation_ids']))
        out.append('')
    if cmap:
        out.append('참고한 원문')
        seen=set()
        for c in cmap.values():
            key=(c['publisher'],c['title'],c['url'])
            if key in seen:continue
            seen.add(key);out.extend([f'[{numbers[c["id"]]}] '+c['publisher']+' — '+c['title'],c['url'],''])
    return '\n'.join(out).rstrip()+'\n'


def reader_html(article:dict,asset_map:dict[str,str]|None=None)->str:
    validate('ArticleIR',article);cmap=_citation_map(article);asset_map=asset_map or {}
    numbers=_citation_numbers(cmap)
    nodes=[f'<h1>{escape(article["title"])}</h1>']
    for b in article['blocks']:
        typ=b['type']
        if typ in ('paragraph','heading','quote','callout'):
            tag={'paragraph':'p','heading':'h2','quote':'blockquote','callout':'aside'}[typ]
            body=f'<{tag}>{escape(b["text"])}</{tag}>'
        elif typ=='list':
            tag='ol' if b['ordered'] else 'ul';body=f'<{tag}>'+''.join('<li>'+escape(x)+'</li>' for x in b['items'])+f'</{tag}>'
        elif typ=='table':
            body='<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(x)+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
        elif typ=='image':
            require(b['asset_id'] in asset_map,'IMAGE_FILE_NOT_RESOLVED');src=asset_map[b['asset_id']];safe_path(src)
            body=f'<figure><img src="{escape(src,quote=True)}" alt="{escape(b["alt_text"],quote=True)}"><figcaption>{escape(b["caption"])}</figcaption></figure>'
        else:raise ValueError('UNSUPPORTED_BLOCK')
        if b['citation_ids']:
            links=[]
            for cid in b['citation_ids']:
                c=cmap[cid]; links.append(f'<a href="#source-{numbers[cid]}" title="{escape(c["publisher"]+": "+c["title"],quote=True)}">[{numbers[cid]}]</a>')
            refs='<sup class="attribution">'+''.join(dict.fromkeys(links))+'</sup>'
            if typ in ('paragraph','heading','quote','callout'):
                closing='</'+{'paragraph':'p','heading':'h2','quote':'blockquote','callout':'aside'}[typ]+'>'
                body=body[:-len(closing)]+' '+refs+closing
            else:body+=refs
        nodes.append('<section>'+body+'</section>')
    if cmap:
        nodes.append('<footer><h2>참고한 원문</h2><ul>')
        seen=set()
        for c in cmap.values():
            key=(c['publisher'],c['title'],c['url'])
            if key in seen:continue
            seen.add(key);nodes.append(f'<li id="source-{numbers[c["id"]]}">'+escape(c['publisher'])+' — <a href="'+escape(c['url'],quote=True)+'" rel="noopener noreferrer">'+escape(c['title'])+'</a></li>')
        nodes.append('</ul></footer>')
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self';"><title>원고 미리보기</title><style>
body{font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;max-width:720px;margin:40px auto;padding:0 20px;color:#202633;line-height:1.95;background:#fff}h1{font-size:1.8rem;line-height:1.5;letter-spacing:-.04em;margin-bottom:2rem}h2{font-size:1.2rem;line-height:1.65;margin:2.2rem 0 .7rem}p{margin:.6rem 0 1rem;word-break:keep-all;overflow-wrap:anywhere}.attribution{font-size:.62em;color:#68717d;margin-left:.15em;white-space:nowrap}a{color:#315d76;overflow-wrap:anywhere}.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:.88rem}td,th{border-bottom:1px solid #d5dce2;padding:10px 12px;text-align:left;vertical-align:top}th{background:#eef3f5}footer{border-top:1px solid #d5dce2;margin-top:2rem;font-size:.8rem}footer li{margin-bottom:.6rem}img{max-width:100%;height:auto}blockquote,aside{border-left:3px solid #8a9caa;margin:1rem 0;padding-left:1rem}h1,h2,th{word-break:keep-all;overflow-wrap:break-word}@media(max-width:480px){body{margin:24px auto;padding:0 18px}h1{font-size:1.5rem}td,th{padding:8px}}
</style></head><body><article>'''+''.join(nodes)+'</article></body></html>'


def write_preview(article:dict,out:Path)->dict:
    """Preview only: does not authorize handoff or imply a real platform test."""
    out.mkdir(parents=True,exist_ok=True)
    files={}
    for name,text in [('article.txt',reader_text(article)),('preview.html',reader_html(article))]:
        data=text.encode();(out/name).write_bytes(data);files[name]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    private={'purpose':'EDITORIAL_REFERENCE_PREVIEW_NOT_PRODUCTION_APPROVAL','article_id':article['id'],'revision_id':article['revision_id'],'content_hash':content_hash(article),'files':files,'claims_verified_by_code':False,'naturalness_verified_by_code':False,'viral_probability':None,'findings':[asdict(f) for f in lint_article(article)]}
    (out/'preview_record.json').write_text(json.dumps(private,ensure_ascii=False,indent=2)+'\n')
    return private


def validate_editorial_review(article:dict,review:dict,policy:dict)->None:
    """Validate references, scope and fresh hashes; NOT reviewer authenticity.
    In production reviewer identity/policy approval must come from authenticated
    services, never from the writer's JSON, a web page, or a mutable client flag.
    """
    from jsonschema import Draft202012Validator
    root=Path(__file__).resolve().parents[1]
    schema=json.loads((root/'schemas/r2/editorial_review.schema.json').read_text())
    Draft202012Validator(schema).validate(review)
    for field in ('article_id','revision_id','blog_id'):
        key='id' if field=='article_id' else field
        require(review[field]==article[key],f'REVIEW_{field.upper()}_MISMATCH')
    require(review['content_hash']==content_hash(article),'STALE_EDITORIAL_REVIEW')
    require(review['reviewer_id']!=policy['writer_id'],'SELF_REVIEW_NOT_INDEPENDENT')
    require(review['reviewer_id'] in policy['authorized_reviewer_ids'],'REVIEWER_UNAUTHORIZED')
    allowed=policy.get('review_kinds_by_reviewer',{}).get(review['reviewer_id'],[])
    require(review['review_kind'] in allowed,'REVIEW_KIND_NOT_AUTHORIZED')
    blocks={b['block_id']:block_text(b) for b in article['blocks']};blocks['TITLE']=article['title']
    for item in review['findings']+review['payoffs']:
        for anchor in item['anchors']:
            require(anchor['block_id'] in blocks,'ANCHOR_BLOCK_MISSING')
            require(anchor['quote'] in blocks[anchor['block_id']],'ANCHOR_NOT_IN_FINAL_COPY')
    for payoff in review['payoffs']:
        require(set(payoff['source_ids'])<=set(c['id'] for c in article['public_citations']),'PAYOFF_SOURCE_UNKNOWN')
        require(payoff['kind']=='editorial_judgment' or bool(payoff['source_ids']),'PAYOFF_EVIDENCE_MISSING')
    require(review['verdict']!='PASS' or (review['dimensions']['payoff']=='PASS' and review['dimensions']['promise']=='PASS' and bool(review['payoffs'])),'EMPTY_PAYOFF_CANNOT_PASS')
    require(not(review['verdict']=='PASS' and any(f['severity'] in ('critical','major') for f in review['findings'])),'MAJOR_FINDING_CANNOT_PASS')


def next_action(article:dict,review:dict|None,policy:dict,fact_state:str)->dict:
    """Non-probabilistic workflow triage; never predicts virality or authorship."""
    require(fact_state in ('VERIFIED','BLOCKED','UNKNOWN'),'FACT_STATE_INVALID')
    if fact_state!='VERIFIED':return {'action':'FACT_REVIEW','reason':'factual correctness not supplied as verified','auto_ready':False}
    if any(f.severity=='block' for f in lint_article(article)):return {'action':'REPAIR_EXPORT','reason':'public copy has unresolved internal text','auto_ready':False}
    if review is None:return {'action':'EDITORIAL_REVIEW','reason':'no final-copy editorial review','auto_ready':False}
    validate_editorial_review(article,review,policy)
    if review['verdict']=='FAIL':
        codes={f['code'] for f in review['findings']}
        a='RESEARCH' if {'MISSING_PAYOFF','UNSUPPORTED_SPECIFICITY'}&codes else 'LOCAL_EDIT'
        return {'action':a,'reason':'review findings require repair','auto_ready':False}
    if review['verdict']=='UNKNOWN' or 'UNKNOWN' in review['dimensions'].values():return {'action':'EDITORIAL_REVIEW','reason':'unresolved semantic assessment','auto_ready':False}
    require(all(x=='PASS' for x in review['dimensions'].values()),'DIMENSION_FAIL_CANNOT_PASS')
    if article['is_reference_example'] or review['review_kind']=='REFERENCE_ANNOTATION':return {'action':'REFERENCE_PREVIEW_ONLY','reason':'sample cannot become production by changing review','auto_ready':False}
    if policy['reader_calibration_status']!='VALIDATED':return {'action':'OWNER_REVIEW','reason':'real reader calibration has not run','auto_ready':False}
    return {'action':'HANDOFF_GATE_REQUIRED','reason':'editorial pass still requires R1 facts/rights/files/freshness gate','auto_ready':False}
