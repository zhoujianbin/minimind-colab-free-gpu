#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; export PATH="$HOME/.local/bin:$PATH"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
colab exec -s "$SESSION" -f "$ROOT/remote/status_training.py" --timeout 60
