#!/usr/bin/env bash
set -euo pipefail
SESSION="${SESSION:-minimind-t4}"; export PATH="$HOME/.local/bin:$PATH"
colab ssh -s "$SESSION"
# 进入远端后运行：cd /content/minimind && python eval_llm.py --load_from model --weight full_sft --hidden_size 512 --num_hidden_layers 8 --max_new_tokens 256 --temperature 0.7 --top_p 0.9 --open_thinking 0 --device cuda:0
