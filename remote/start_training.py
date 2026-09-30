#!/usr/bin/env python3
import json,os,subprocess,time
from pathlib import Path
base=Path('/content'); pidfile=base/'minimind-training.pid'; exitfile=base/'minimind-training.exit'; status=base/'minimind-training-status.json'; log=base/'minimind-training.log'
if pidfile.exists():
 try:
  pid=int(pidfile.read_text()); os.kill(pid,0)
  state=Path(f'/proc/{pid}/stat').read_text().split()[2] if Path(f'/proc/{pid}/stat').exists() else '?'
  if state!='Z': raise SystemExit(f'训练进程已存在 PID={pid}')
 except ProcessLookupError: pass
for p in (exitfile,status):
 if p.exists(): p.unlink()
wrapper="bash /content/train_pipeline.sh; rc=$?; echo $rc > /content/minimind-training.exit; exit $rc"
fh=log.open('w'); proc=subprocess.Popen(['bash','-lc',wrapper],stdout=fh,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,start_new_session=True); fh.close()
pidfile.write_text(str(proc.pid)); status.write_text(json.dumps({'pid':proc.pid,'started_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'log':str(log)})); print('TRAINING_STARTED',proc.pid)
