#!/usr/bin/env bash
set -euo pipefail
if ! command -v uv >/dev/null 2>&1; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi
export PATH="$HOME/.local/bin:$PATH"
uv tool install --force google-colab-cli==0.7.4
colab version | grep -q '0.7.4' || { echo 'Colab CLI 版本校验失败' >&2; exit 1; }
colab version
echo '安装完成。请把 export PATH="$HOME/.local/bin:$PATH" 加入 shell 配置。'
