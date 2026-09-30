#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; export PATH="$HOME/.local/bin:$PATH"
cat <<'PY' | colab exec -s "$SESSION" --timeout 60
import os,subprocess
p='/content/minimind-training.log'; print(open(p).read()[-5000:] if os.path.exists(p) else '训练日志尚未生成')
print('
--- 训练进程 ---')
print(subprocess.run("ps -eo pid,etime,pcpu,pmem,cmd | grep -E 'train_pretrain|train_full_sft' | grep -v grep",shell=True,text=True,capture_output=True).stdout or '当前没有训练进程')
out='/content/minimind/out'; print('--- 输出文件 ---')
if os.path.isdir(out):
 for name in os.listdir(out): print(name,round(os.path.getsize(os.path.join(out,name))/1024/1024,2),'MiB')
PY
