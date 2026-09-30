#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"; SESSION="${1:-minimind-t4}"; FORCE="${2:-}"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATUS="$(colab exec -s "$SESSION" -f "$ROOT/remote/status_training.py" --timeout 60 2>&1 || true)"; echo "$STATUS"
if echo "$STATUS" | grep -q 'RUNNING PID' && [[ "$FORCE" != '--force' ]]; then echo '训练仍在运行，拒绝停止。确需中断请加 --force。' >&2; exit 1; fi
echo "请确认模型已下载。即将停止：$SESSION"; read -r -p '输入 STOP 确认：' answer
[[ "$answer" == STOP ]] || exit 1
colab stop -s "$SESSION"
