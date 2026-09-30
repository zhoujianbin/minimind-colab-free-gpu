#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"; SESSION="${1:-minimind-t4}"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if colab status -s "$SESSION" >/dev/null 2>&1; then echo "会话 $SESSION 已存在"; else colab new -s "$SESSION" --gpu T4; fi
STATUS="$(colab status -s "$SESSION")"; echo "$STATUS"; echo "$STATUS" | grep -q 'Hardware: T4' || { echo '错误：会话不是 T4' >&2; exit 1; }
colab exec -s "$SESSION" -f "$ROOT/remote/verify_gpu.py" --timeout 60
colab url -s "$SESSION"
