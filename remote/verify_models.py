#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
base=Path('/content'); exitfile=base/'minimind-training.exit'; marker=base/'minimind-training.complete'; out=base/'minimind/out'
if not exitfile.exists() or exitfile.read_text().strip()!='0' or not marker.exists(): raise SystemExit('训练尚未成功完成，拒绝下载')
result={}; hidden=os.environ.get('HIDDEN_SIZE','512')
for name in (f'pretrain_{hidden}.pth',f'full_sft_{hidden}.pth'):
 p=out/name
 if not p.exists() or p.stat().st_size<1024*1024: raise SystemExit(f'模型缺失或过小: {p}')
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 result[name]={'bytes':p.stat().st_size,'sha256':h.hexdigest()}
print('MODELS_VERIFIED',json.dumps(result))
