# 故障排查

## 网页打开后仍是 CPU

CLI 创建的 GPU 会话可能显示为“未知笔记本 GPU”。运行：

```bash
colab sessions
colab url -s minimind-t4 --open
```

不要误删 GPU 会话。网页资源面板写“Google Compute Engine 后端”并不能证明是 CPU，应运行 `torch.cuda.is_available()`。

## NVIDIA-SMI 找不到 libnvidia-ml.so

GPU 可能已被免费配额系统收回，而 VM 和文件暂时保留。立即执行 `scripts/06_download_models.sh`。不要把唯一模型留在 `/content`。

## Connection was lost

Colab CLI 的 WebSocket 可能短暂断开。先看 `colab status`，然后 `colab restart-kernel -s minimind-t4`。后台 shell 进程有时仍在运行，检查训练日志再决定是否重启。

## pip 在编译 numpy/scikit-learn

新 Colab 可能使用 Python 3.13，MiniMind 完整 requirements 中的旧版本没有 wheel。本仓库只安装训练必需包，避免安装 sentence-transformers/scikit-learn 等非核心依赖。

## OAuth invalid code verifier

授权码只对应生成它的那一次命令。重新运行 `colab new`，打开新链接并使用新授权码，不要复用旧码。

## 无法保存 Notebook

Scratchpad 或只读 Notebook 不会自动保存。使用“复制到云端硬盘”，或者坚持 CLI 主路线并把代码留在本地 Git 仓库。

## CUDA out of memory

降低 batch size 或 max_seq_len，并提高 accumulation_steps。例如 batch 从 16 降到 8，同时 accumulation 从 4 提到 8。
