#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; SAMPLE_COUNT="${SAMPLE_COUNT:-50000}"
export PATH="$HOME/.local/bin:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
colab upload -s "$SESSION" "$ROOT/remote/setup_and_prepare.py" /content/setup_and_prepare.py
cat <<PY | colab exec -s "$SESSION" --timeout 1800
import runpy,sys
sys.argv=['setup_and_prepare.py','--sample-count','$SAMPLE_COUNT']
runpy.run_path('/content/setup_and_prepare.py',run_name='__main__')
PY
