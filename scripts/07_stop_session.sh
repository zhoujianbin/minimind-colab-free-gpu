#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"; SESSION="${1:-minimind-t4}"
echo "请先确认模型已经下载。即将停止：$SESSION"; read -r -p '输入 STOP 确认：' answer
[[ "$answer" == STOP ]] || exit 1
colab stop -s "$SESSION"
