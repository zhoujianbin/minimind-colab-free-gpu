#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; export PATH="$HOME/.local/bin:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
colab upload -s "$SESSION" "$ROOT/remote/train_pipeline.sh" /content/train_pipeline.sh
cat <<'PY' | colab exec -s "$SESSION" --timeout 60
import subprocess
log=open('/content/minimind-training.log','w')
subprocess.Popen(['bash','/content/train_pipeline.sh'],stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,start_new_session=True)
print('训练已在后台启动')
PY
echo '查看进度：bash scripts/04_status.sh'
