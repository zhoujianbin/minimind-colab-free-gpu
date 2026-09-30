#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; DEST="${1:-outputs}"; export PATH="$HOME/.local/bin:$PATH"
mkdir -p "$DEST"
for f in pretrain_512.pth full_sft_512.pth; do colab download -s "$SESSION" "/content/minimind/out/$f" "$DEST/$f"; done
shasum -a 256 "$DEST"/*.pth; ls -lh "$DEST"
