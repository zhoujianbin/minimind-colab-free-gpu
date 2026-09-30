#!/usr/bin/env bash
set -euo pipefail
if ! command -v uv >/dev/null 2>&1; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi
export PATH="$HOME/.local/bin:$PATH"
if ! command -v colab >/dev/null 2>&1; then uv tool install google-colab-cli; fi
colab version
echo '安装完成。请把 export PATH="$HOME/.local/bin:$PATH" 加入 shell 配置。'
