# 发布前复现报告

## 状态

- 静态审查：通过
- 全新 Colab CPU 小规模端到端冒烟测试：通过
- 全新免费 T4、50k + 50k BF16 完整复现：通过
- 同条件 FP16/BF16 对照推理：通过
- 模型完整性和原子下载：通过
- 发布结论：当前审查分支可合并

## CPU 冒烟测试（2026-09-30）

在一个全新 Colab CPU 会话中执行公开脚本，未复用旧 VM 文件：

- MiniMind commit：`f659b55761b754d306bd140573493a6543cafd7f`
- 数据：预训练 20 条 + SFT 20 条
- 模型：hidden size 64、2 层，约 0.53M 参数
- sequence length：32
- batch：2
- 预训练：10/10 mini-batch，22 秒
- SFT：10/10 mini-batch，11 秒
- 总训练：33 秒
- 两个权重：各 1,893,396 bytes
- 训练退出码：0
- 成功标记：存在
- 推理：成功加载 full_sft 权重并生成 token（该极小模型输出无语义，符合预期）
- 下载：通过临时文件原子下载，本地 SHA-256 与远端一致

哈希：

```text
pretrain_64.pth  b518375ceda81bab0b8c9f11855a33abd14b6b56413496da16cdb095927c03e0
full_sft_64.pth  b7da1f3a5f39e69aa4823687c9342b834e41ffae3eebdf8ac2755c6762351be8
```

## 冒烟测试发现并修复的问题

1. `colab exec -f` 在 IPython kernel 中会附带 `-f kernel.json`，普通 `argparse.parse_args()` 会失败；改为 `parse_known_args()`。
2. Colab 执行单元中出现 `SystemExit` 时，CLI 进程不一定返回非零；关键阶段必须输出并检查成功 sentinel。
3. 数据准备现在同时检查 `DATA_READY` 和独立的 `DATA_VERIFIED`。
4. 训练状态现在区分 RUNNING、SUCCEEDED、FAILED，并正确识别 zombie 进程。
5. 下载前检查退出码、成功标记、文件大小和远端 SHA-256；下载使用 `.part` 后原子改名。

## T4 完整测试（2026-10-01）

### 环境

- GPU：Tesla T4，15,360 MiB
- Python：3.13.15
- PyTorch：2.11.0+cu128
- CUDA runtime：12.8
- Transformers：4.57.6
- Datasets：3.6.0
- ModelScope：1.37.0
- MiniMind commit：`f659b55761b754d306bd140573493a6543cafd7f`

### 数据证据

```text
pretrain_t2t_mini.jsonl
count: 50000
bytes: 37132208
sha256: 48e39264bac8d98fb2a0dfc4be18eb612eb09431c68df79ce39cb92972e65044

sft_t2t_mini.jsonl
count: 50000
bytes: 143033221
sha256: 794686f2247a16e37c2a7e50629a51df6bfce351ff1857e8b52c92f4f13dd7c8
```

抽样方式为确定性前缀抽样，存在顺序偏差；这些哈希只证明本次输入一致，不代表完整数据集的官方版本标识。

### 训练结果

- 模型：hidden size 512、8 层，30.03M 参数
- BF16 预训练：3,125/3,125 mini-batch，1,255 秒，最后记录 loss 3.3587
- BF16 SFT：6,250/6,250 mini-batch，2,082 秒，最后记录 loss 2.3399
- BF16 总训练时间：3,337 秒，即 55 分 37 秒
- 对照 FP16：总训练 1,118 秒（18 分 38 秒），约快 2.98 倍；FP16 最终 loss 为预训练 3.3587、SFT 2.3290
- 退出码：0
- 成功标记：`TRAINING_COMPLETE`

训练时间是这一次会话的观测值，不是免费 T4 的性能保证。第一次复现尝试曾在 SFT 中途被 Colab 回收；第二个全新 T4 会话完整成功。这证明免费资源回收风险是真实存在的。

### 推理结果

CUDA 推理成功，模型参数量报告为 30.03M。固定的五组中文问题均完成生成，速度约 25–82 token/s。输出存在重复、事实错误和代码任务失败，符合本教程对小模型能力的警告。

### 最终模型

```text
pretrain_512.pth
bytes: 66633655
sha256: 8d43d9302266c1f140ca35e7ba6630341742139f201f471bbf91cad74ceb00c1

full_sft_512.pth
bytes: 66633655
sha256: 22bf8b9575fd9b9916a438d5ae7f7a9dd7261ec3dd7c704cf85935559faba256
```

远端校验通过，下载使用 `.part` 临时文件，下载后的本地 SHA-256 与远端一致。模型权重未提交到 Git。

### 复现中最后发现的缺陷

SSH 登录到 Colab VM 的普通 shell 可能看不到 CUDA，即使 Colab kernel 能正常使用 Tesla T4。因此原先通过 SSH 启动 CUDA 推理的脚本不可靠。交互测试已改为使用 `colab exec` 在 Colab kernel 内执行，并以 `INFERENCE_OK` 标记成功。
