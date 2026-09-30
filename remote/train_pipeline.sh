#!/usr/bin/env bash
set -euo pipefail
cd /content/minimind/trainer
HIDDEN_SIZE="${HIDDEN_SIZE:-512}"; LAYERS="${LAYERS:-8}"; PRETRAIN_SEQ="${PRETRAIN_SEQ:-256}"; SFT_SEQ="${SFT_SEQ:-384}"
DEVICE="${DEVICE:-cuda:0}"; DTYPE="${DTYPE:-float16}"; EPOCHS="${EPOCHS:-1}"; NUM_WORKERS="${NUM_WORKERS:-4}"
PRETRAIN_BATCH="${PRETRAIN_BATCH:-16}"; PRETRAIN_ACCUM="${PRETRAIN_ACCUM:-4}"; SFT_BATCH="${SFT_BATCH:-8}"; SFT_ACCUM="${SFT_ACCUM:-2}"
test -s ../dataset/pretrain_t2t_mini.jsonl; test -s ../dataset/sft_t2t_mini.jsonl
if [[ "$DEVICE" == cuda:* ]]; then nvidia-smi --query-gpu=name,memory.total --format=csv,noheader; fi
TOTAL_START=$(date +%s); echo "TRAINING_START=$(date -Iseconds)"; echo "CONFIG hidden=$HIDDEN_SIZE layers=$LAYERS device=$DEVICE dtype=$DTYPE"
echo '=== 1/2 从随机权重开始预训练 ==='; PRETRAIN_START=$(date +%s)
python train_pretrain.py --save_dir ../out --save_weight pretrain --data_path ../dataset/pretrain_t2t_mini.jsonl --from_weight none --from_resume 0 --device "$DEVICE" --dtype "$DTYPE" --epochs "$EPOCHS" --batch_size "$PRETRAIN_BATCH" --accumulation_steps "$PRETRAIN_ACCUM" --hidden_size "$HIDDEN_SIZE" --num_hidden_layers "$LAYERS" --max_seq_len "$PRETRAIN_SEQ" --num_workers "$NUM_WORKERS" --log_interval 20 --save_interval 500
PRETRAIN_END=$(date +%s); test -s ../out/pretrain_${HIDDEN_SIZE}.pth; echo "PRETRAIN_SECONDS=$((PRETRAIN_END-PRETRAIN_START))"
echo '=== 2/2 监督微调 SFT ==='; SFT_START=$(date +%s)
python train_full_sft.py --save_dir ../out --save_weight full_sft --data_path ../dataset/sft_t2t_mini.jsonl --from_weight pretrain --from_resume 0 --device "$DEVICE" --dtype "$DTYPE" --epochs "$EPOCHS" --batch_size "$SFT_BATCH" --accumulation_steps "$SFT_ACCUM" --hidden_size "$HIDDEN_SIZE" --num_hidden_layers "$LAYERS" --max_seq_len "$SFT_SEQ" --num_workers "$NUM_WORKERS" --log_interval 20 --save_interval 500
SFT_END=$(date +%s); test -s ../out/full_sft_${HIDDEN_SIZE}.pth
echo "SFT_SECONDS=$((SFT_END-SFT_START))"; echo "TOTAL_SECONDS=$((SFT_END-TOTAL_START))"; echo "TRAINING_END=$(date -Iseconds)"
touch /content/minimind-training.complete; echo TRAINING_COMPLETE
