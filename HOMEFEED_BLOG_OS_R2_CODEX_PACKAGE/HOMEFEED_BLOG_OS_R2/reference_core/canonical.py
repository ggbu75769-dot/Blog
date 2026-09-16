"""HFBO-NFC-INT-1: restricted, cross-language canonical bytes for immutable IR.
Not RFC8785/JCS. Integer-valued JSON numbers within the JS safe range are supported;
fractions must be modeled as decimal strings. Source raw bytes retain their own hash.
"""
from __future__ import annotations
import hashlib,json,math,unicodedata
from typing import Any
MAX_SAFE_INTEGER=9007199254740991

def _text(value:str)->str:
    if any(0xD800<=ord(c)<=0xDFFF for c in value):
        raise ValueError('CANON_INVALID_UNICODE')
    return unicodedata.normalize('NFC',value)

def normalized(value:Any)->Any:
    if value is None or isinstance(value,bool):return value
    if isinstance(value,str):return _text(value)
    if isinstance(value,(int,float)):
        if not math.isfinite(value) or int(value)!=value or abs(value)>MAX_SAFE_INTEGER:
            raise ValueError('CANON_NOT_SAFE_INTEGER')
        return int(value)
    if isinstance(value,list):return [normalized(v) for v in value]
    if isinstance(value,dict):
        result={}
        for key,v in value.items():
            if not isinstance(key,str):raise ValueError('CANON_NON_STRING_KEY')
            key=_text(key)
            if key in result:raise ValueError('CANON_NORMALIZED_KEY_COLLISION')
            result[key]=normalized(v)
        return result
    raise TypeError('CANON_UNSUPPORTED_TYPE')

def canonical_bytes(value:Any)->bytes:
    return json.dumps(normalized(value),ensure_ascii=False,sort_keys=True,
                      separators=(',',':'),allow_nan=False).encode('utf-8')

def content_hash(value:Any)->str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def strict_json_loads(text:str)->Any:
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('JSON_DUPLICATE_KEY')
            result[k]=v
        return result
    return json.loads(text,object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError('JSON_NONFINITE')))
