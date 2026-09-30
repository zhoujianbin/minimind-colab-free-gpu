#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; export PATH="$HOME/.local/bin:$PATH"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo '输入问题开始对话；输入 exit 退出。每次回答会重新加载教学模型，可能需要十几秒。'
while true; do
 read -r -p '你：' PROMPT || break
 [[ "$PROMPT" == exit ]] && break
 OUTPUT="$(colab exec -s "$SESSION" -f "$ROOT/remote/chat_once.py" --env "PROMPT=$PROMPT" --timeout 300 2>&1)"; echo "$OUTPUT"; echo "$OUTPUT" | grep -q INFERENCE_OK || { echo '推理失败' >&2; exit 1; }
done
