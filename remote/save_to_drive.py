#!/usr/bin/env python3
from pathlib import Path
import shutil
src=Path('/content/minimind/out'); dst=Path('/content/drive/MyDrive/minimind-from-scratch'); dst.mkdir(parents=True,exist_ok=True)
for name in ('pretrain_512.pth','full_sft_512.pth'):
 shutil.copy2(src/name,dst/name); print('saved:',dst/name)
