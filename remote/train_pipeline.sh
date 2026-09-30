#!/usr/bin/env bash
set -euo pipefail
cd /content/minimind/trainer
HIDDEN_SIZE="${HIDDEN_SIZE:-512}"; LAYERS="${LAYERS:-8}"; PRETRAIN_SEQ="${PRETRAIN_SEQ:-256}"; SFT_SEQ="${SFT_SEQ:-384}"
TOTAL_START=$(date +%s)
echo "TRAINING_START=$(date -Iseconds)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true

echo '=== 1/2 从随机权重开始预训练 ==='
PRETRAIN_START=$(date +%s)
python train_pretrain.py --epochs 1 --batch_size 16 --accumulation_steps 4 --hidden_size "$HIDDEN_SIZE" --num_hidden_layers "$LAYERS" --max_seq_len "$PRETRAIN_SEQ" --num_workers 4 --log_interval 20 --save_interval 500
PRETRAIN_END=$(date +%s)
echo "PRETRAIN_SECONDS=$((PRETRAIN_END-PRETRAIN_START))"

echo '=== 2/2 监督微调 SFT ==='
SFT_START=$(date +%s)
python train_full_sft.py --epochs 1 --batch_size 8 --accumulation_steps 2 --hidden_size "$HIDDEN_SIZE" --num_hidden_layers "$LAYERS" --max_seq_len "$SFT_SEQ" --num_workers 4 --log_interval 20 --save_interval 500
SFT_END=$(date +%s)
echo "SFT_SECONDS=$((SFT_END-SFT_START))"
echo "TOTAL_SECONDS=$((SFT_END-TOTAL_START))"
echo "TRAINING_END=$(date -Iseconds)"
echo TRAINING_COMPLETE
