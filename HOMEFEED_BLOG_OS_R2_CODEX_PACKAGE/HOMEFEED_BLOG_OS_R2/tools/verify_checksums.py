#!/usr/bin/env python3
"""Verify an unmodified delivered package. Tests regenerate reports, so run this first."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,re,sys

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();root=a.root.resolve();manifest=root/'PACKAGE_SHA256SUMS.txt';errors=[];seen=set();count=0
 if not manifest.is_file():print('Missing PACKAGE_SHA256SUMS.txt');return 1
 for line in manifest.read_text(encoding='utf-8').splitlines():
  if not line:continue
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
  if not m:errors.append('MALFORMED_LINE');continue
  expected,name=m.groups();path=PurePosixPath(name)
  if path.is_absolute() or any(x in ('','.','..') for x in name.split('/')) or '\\' in name or ':' in name or name in seen:errors.append('UNSAFE_OR_DUPLICATE_PATH '+name);continue
  seen.add(name);full=root/path
  if not full.is_file() or full.is_symlink() or any(x.is_symlink() for x in full.parents if x!=root and x.is_relative_to(root)) or not full.resolve().is_relative_to(root):errors.append('FILE_MISSING_OR_ESCAPE '+name);continue
  actual=hashlib.sha256(full.read_bytes()).hexdigest();count+=1
  if actual!=expected:errors.append('HASH_MISMATCH '+name)
 for e in errors:print(e)
 print(f'Package files verified: {count}; errors: {len(errors)}')
 return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
