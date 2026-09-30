#!/usr/bin/env python3
import hashlib,os,shutil
from pathlib import Path
src=Path('/content/minimind/out'); mount=Path('/content/drive/MyDrive'); dst=mount/'minimind-from-scratch'
if not mount.is_dir(): raise SystemExit('Google Drive 尚未挂载到 /content/drive')
dst.mkdir(parents=True,exist_ok=True)
for name in ('pretrain_512.pth','full_sft_512.pth'):
 source=src/name
 if not source.exists() or source.stat().st_size<1024*1024: raise SystemExit(f'源模型缺失或不完整: {source}')
 tmp=dst/(name+'.part'); shutil.copy2(source,tmp); os.replace(tmp,dst/name)
 h=hashlib.sha256((dst/name).read_bytes()).hexdigest(); print('saved:',dst/name,'sha256:',h)
