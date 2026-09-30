#!/usr/bin/env python3
import torch
print('PyTorch:',torch.__version__); print('CUDA:',torch.cuda.is_available())
if not torch.cuda.is_available(): raise SystemExit('当前会话没有 CUDA GPU')
name=torch.cuda.get_device_name(0); print('GPU:',name)
if 'T4' not in name: raise SystemExit(f'需要 Tesla T4，实际为 {name}')
