"""Pure renderer for reference IR. Does not publish or assert editor compatibility."""
from __future__ import annotations
from pathlib import Path
from html import escape
import hashlib,json
from .contracts import validate,require,safe_path,web_url

def public_text(article:dict)->str:
    validate('ArticleIR',article)
    out=[article['title'],'']
    for b in article['blocks']:
        t=b['type']
        if t in ('paragraph','heading','quote','callout'):out.append(b['text'])
        elif t=='list':out.extend((str(i+1)+'. ' if b['ordered'] else '- ')+x for i,x in enumerate(b['items']))
        elif t=='table':
            out.append(' | '.join(b['headers']));out.extend(' | '.join(row) for row in b['rows'])
        elif t=='image':out.append(b['caption'])
        if b['citation_ids']:out.append('출처: '+', '.join(b['citation_ids']))
        out.append('')
    if article['public_citations']:
        out.append('참고 자료')
        out.extend(f"[{c['id']}] {c['publisher']} — {c['title']}\n{c['url']}" for c in article['public_citations'])
    return '\n'.join(out).rstrip()+'\n'

def render_html(article:dict,asset_map:dict[str,str]|None=None)->str:
    validate('ArticleIR',article);asset_map=asset_map or {};parts=[f"<h1>{escape(article['title'])}</h1>"]
    for b in article['blocks']:
        t=b['type'];bid=escape(b['block_id'],quote=True)
        if t in ('paragraph','heading','quote','callout'):
            tag={'paragraph':'p','heading':'h2','quote':'blockquote','callout':'aside'}[t]
            body=f'<{tag}>{escape(b["text"])}</{tag}>'
        elif t=='list':
            tag='ol' if b['ordered'] else 'ul';body=f'<{tag}>'+''.join('<li>'+escape(x)+'</li>' for x in b['items'])+f'</{tag}>'
        elif t=='table':
            body='<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(x)+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
        else:
            require(b['asset_id'] in asset_map,'RENDER_ASSET_MISSING');src=asset_map[b['asset_id']];safe_path(src)
            body=f'<figure><img src="{escape(src,quote=True)}" alt="{escape(b["alt_text"],quote=True)}"><figcaption>{escape(b["caption"])}</figcaption></figure>'
        if b['citation_ids']:
            body+='<p class="citation">출처: '+', '.join(f'<a href="#citation-{escape(cid,quote=True)}">{escape(cid)}</a>' for cid in b['citation_ids'])+'</p>'
        parts.append(f'<section data-block-id="{bid}">{body}</section>')
    if article['public_citations']:
        parts.append('<footer><h2>참고 자료</h2><ul>')
        for c in article['public_citations']:
            web_url(c['url']);parts.append(f'<li id="citation-{escape(c["id"],quote=True)}">{escape(c["publisher"])} — <a rel="noopener noreferrer" href="{escape(c["url"],quote=True)}">{escape(c["title"])}</a></li>')
        parts.append('</ul></footer>')
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:;"><title>원고 전송 미리보기</title><style>body{font-family:Arial,'Noto Sans CJK KR',sans-serif;max-width:760px;margin:32px auto;padding:0 20px;line-height:1.85}h1{font-size:1.8rem;line-height:1.5}h2{font-size:1.2rem;margin-top:2rem}img{max-width:100%;height:auto}.table-scroll{overflow-x:auto}table{border-collapse:collapse;min-width:100%}td,th{border:1px solid;padding:.5rem}.citation,footer{font-size:.85rem}a{overflow-wrap:anywhere}p{overflow-wrap:anywhere}</style></head><body><article>'''+''.join(parts)+'</article></body></html>'

def verify_export_files(root:Path,files:list[dict])->None:
    root=root.resolve();seen=set()
    for entry in files:
        key=safe_path(entry['path']);require(key not in seen,'FILE_PATH_DUPLICATE');seen.add(key)
        raw=root/entry['path'];require(not raw.is_symlink(),'FILE_SYMLINK')
        for part in raw.relative_to(root).parents:
            if str(part)!='.':require(not (root/part).is_symlink(),'DIRECTORY_SYMLINK')
        p=raw.resolve();require(p.is_relative_to(root),'FILE_ESCAPE');require(p.is_file(),'FILE_MISSING')
        data=p.read_bytes();require(len(data)==entry['size_bytes'],'FILE_SIZE');require(hashlib.sha256(data).hexdigest()==entry['sha256'],'FILE_HASH')

def build_reference_export(article:dict,out:Path)->list[dict]:
    require(article['is_reference_example'],'REFERENCE_ONLY_RENDER')
    out.mkdir(parents=True,exist_ok=True)
    payloads={'article.txt':(public_text(article),'text/plain'),'preview.html':(render_html(article),'text/html')}
    files=[]
    for name,(text,mime) in payloads.items():
        data=text.encode('utf-8');(out/name).write_bytes(data)
        files.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'mime':mime,'size_bytes':len(data),'visibility':'public'})
    verify_export_files(out,files)
    return files
