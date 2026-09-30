#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
errors=[]
pattern=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
for f in root.rglob('*.md'):
 text=f.read_text(encoding='utf-8')
 for target in pattern.findall(text):
  if target.startswith(('http://','https://','#','mailto:')): continue
  path=target.split('#')[0]
  if path and not (f.parent/path).resolve().exists(): errors.append(f'{f.relative_to(root)} -> {target}')
if errors:
 print('损坏的本地链接:',file=sys.stderr); print(*errors,sep='\n',file=sys.stderr); raise SystemExit(1)
nb=json.loads((root/'notebooks/colab_minimind_from_scratch.ipynb').read_text()); assert nb['nbformat']==4
required=['remote/setup_and_prepare.py','remote/start_training.py','remote/status_training.py','remote/verify_models.py','remote/train_pipeline.sh']
for p in required: assert (root/p).exists(),p
print('repository contract: OK')
