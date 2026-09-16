// HFBO-NFC-INT-1; code-point key order, NOT JS's default UTF-16 key order.
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
function text(s) {
  for (const c of s) { const n=c.codePointAt(0); if(n>=0xD800&&n<=0xDFFF) throw Error('CANON_INVALID_UNICODE'); }
  return s.normalize('NFC');
}
function cmp(a,b) {
  const x=Array.from(a,c=>c.codePointAt(0)),y=Array.from(b,c=>c.codePointAt(0));
  for(let i=0;i<Math.min(x.length,y.length);i++)if(x[i]!==y[i])return x[i]-y[i];
  return x.length-y.length;
}
export function canonicalString(v) {
  if(v===null)return 'null';
  if(typeof v==='boolean')return v?'true':'false';
  if(typeof v==='string')return JSON.stringify(text(v));
  if(typeof v==='number') {if(!Number.isSafeInteger(v))throw Error('CANON_NOT_SAFE_INTEGER');return String(v);}
  if(Array.isArray(v))return '['+v.map(canonicalString).join(',')+']';
  if(typeof v==='object') {
    const normalized=new Map();
    for(const [k,x] of Object.entries(v)){const nk=text(k);if(normalized.has(nk))throw Error('CANON_NORMALIZED_KEY_COLLISION');normalized.set(nk,x);}
    return '{'+[...normalized.keys()].sort(cmp).map(k=>JSON.stringify(k)+':'+canonicalString(normalized.get(k))).join(',')+'}';
  }
  throw Error('CANON_UNSUPPORTED_TYPE');
}
export function canonicalHash(v){return createHash('sha256').update(canonicalString(v),'utf8').digest('hex');}
if(process.argv[2]==='--stdin'){
 try{const value=JSON.parse(readFileSync(0,'utf8'));process.stdout.write(JSON.stringify({canonical:canonicalString(value),hash:canonicalHash(value)}));}
 catch(e){process.stdout.write(JSON.stringify({error:e.message}));process.exitCode=2;}
}
