#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
SESSION="${1:-minimind-t4}"
if colab sessions 2>/dev/null | grep -q "\[$SESSION\]"; then echo "会话 $SESSION 已存在"; else colab new -s "$SESSION" --gpu T4; fi
colab status -s "$SESSION"
echo 'import torch; print("CUDA:",torch.cuda.is_available()); print("GPU:",torch.cuda.get_device_name(0) if torch.cuda.is_available() else "none")' | colab exec -s "$SESSION" --timeout 60
colab url -s "$SESSION"
