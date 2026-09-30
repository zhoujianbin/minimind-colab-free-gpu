#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; DEST="${1:-outputs}"; HIDDEN_SIZE="${HIDDEN_SIZE:-512}"; export PATH="$HOME/.local/bin:$PATH"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$DEST"
VERIFY="$(colab exec -s "$SESSION" -f "$ROOT/remote/verify_models.py" --env "HIDDEN_SIZE=$HIDDEN_SIZE" --timeout 120 2>&1)"; echo "$VERIFY"; echo "$VERIFY" | grep -q 'MODELS_VERIFIED' || { echo '远端模型校验失败' >&2; exit 1; }
for f in "pretrain_${HIDDEN_SIZE}.pth" "full_sft_${HIDDEN_SIZE}.pth"; do
 tmp="$DEST/.$f.part"; rm -f "$tmp"; colab download -s "$SESSION" "/content/minimind/out/$f" "$tmp"; test -s "$tmp"; mv -f "$tmp" "$DEST/$f"
done
shasum -a 256 "$DEST"/*.pth; ls -lh "$DEST"
