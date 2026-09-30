#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; export PATH="$HOME/.local/bin:$PATH"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
colab upload -s "$SESSION" "$ROOT/remote/train_pipeline.sh" /content/train_pipeline.sh
colab exec -s "$SESSION" -f "$ROOT/remote/start_training.py" --timeout 60 \
  --env "HIDDEN_SIZE=${HIDDEN_SIZE:-512}" --env "LAYERS=${LAYERS:-8}" \
  --env "PRETRAIN_SEQ=${PRETRAIN_SEQ:-256}" --env "SFT_SEQ=${SFT_SEQ:-384}" \
  --env "DEVICE=${DEVICE:-cuda:0}" --env "DTYPE=${DTYPE:-float16}" --env "EPOCHS=${EPOCHS:-1}" \
  --env "NUM_WORKERS=${NUM_WORKERS:-4}" --env "PRETRAIN_BATCH=${PRETRAIN_BATCH:-16}" \
  --env "PRETRAIN_ACCUM=${PRETRAIN_ACCUM:-4}" --env "SFT_BATCH=${SFT_BATCH:-8}" --env "SFT_ACCUM=${SFT_ACCUM:-2}"
echo '查看进度：bash scripts/04_status.sh'
