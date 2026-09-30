#!/usr/bin/env bash
set -euo pipefail
cd /content/minimind/trainer
HIDDEN_SIZE="${HIDDEN_SIZE:-512}"; LAYERS="${LAYERS:-8}"; PRETRAIN_SEQ="${PRETRAIN_SEQ:-256}"; SFT_SEQ="${SFT_SEQ:-384}"
echo '=== 1/2 从随机权重开始预训练 ==='
python train_pretrain.py --epochs 1 --batch_size 16 --accumulation_steps 4 --hidden_size "$HIDDEN_SIZE" --num_hidden_layers "$LAYERS" --max_seq_len "$PRETRAIN_SEQ" --num_workers 4 --log_interval 20 --save_interval 500
echo '=== 2/2 监督微调 SFT ==='
python train_full_sft.py --epochs 1 --batch_size 8 --accumulation_steps 2 --hidden_size "$HIDDEN_SIZE" --num_hidden_layers "$LAYERS" --max_seq_len "$SFT_SEQ" --num_workers 4 --log_interval 20 --save_interval 500
echo TRAINING_COMPLETE
