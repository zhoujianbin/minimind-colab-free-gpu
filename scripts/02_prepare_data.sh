#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; SAMPLE_COUNT="${SAMPLE_COUNT:-50000}"; export PATH="$HOME/.local/bin:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT="$(colab exec -s "$SESSION" -f "$ROOT/remote/setup_and_prepare.py" --env "SAMPLE_COUNT=$SAMPLE_COUNT" --timeout 3600 2>&1)"; echo "$OUTPUT"; echo "$OUTPUT" | grep -q 'DATA_READY' || { echo '数据准备未成功完成' >&2; exit 1; }
VERIFY="$(colab exec -s "$SESSION" -f "$ROOT/remote/verify_data.py" --timeout 120 2>&1)"; echo "$VERIFY"; echo "$VERIFY" | grep -q 'DATA_VERIFIED' || { echo '数据完整性校验失败' >&2; exit 1; }
