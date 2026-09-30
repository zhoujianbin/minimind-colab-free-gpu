#!/usr/bin/env python3
import os
from pathlib import Path
base=Path('/content'); pidfile=base/'minimind-training.pid'; exitfile=base/'minimind-training.exit'; log=base/'minimind-training.log'; marker=base/'minimind-training.complete'
if log.exists(): print(log.read_text(errors='replace')[-8000:])
print(); print('--- 训练状态 ---')
pid=int(pidfile.read_text()) if pidfile.exists() else None; running=False
if pid:
 try:
  os.kill(pid,0); state=Path(f'/proc/{pid}/stat').read_text().split()[2] if Path(f'/proc/{pid}/stat').exists() else '?'
  running=state!='Z'
 except ProcessLookupError: pass
if running: print('RUNNING PID',pid)
elif exitfile.exists():
 rc=int(exitfile.read_text().strip()); print('SUCCEEDED' if rc==0 and marker.exists() else 'FAILED','EXIT_CODE',rc)
else: print('NOT_STARTED_OR_UNKNOWN')
print('--- 输出文件 ---'); out=Path('/content/minimind/out')
if out.exists():
 for p in sorted(out.glob('*.pth')): print(p.name,round(p.stat().st_size/1024/1024,2),'MiB')
