#!/usr/bin/env python3
"""Build checked reference article files without network or platform posting."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from editorial_r2.reader import write_preview
for p in sorted((ROOT/'examples/editorial_r2').glob('*/article_ir.json')):
    a=json.loads(p.read_text());write_preview(a,p.parent);print(p.parent.name, 'LOCAL_PREVIEW_WRITTEN_NOT_PLATFORM_VERIFIED')
