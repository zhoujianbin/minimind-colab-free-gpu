# 用 Google Colab 免费 T4 从零训练一个语言模型

> 面向第一次接触大模型训练的学习者：使用 **Colab CLI + MiniMind**，从随机权重开始完成预训练、监督微调（SFT）、中文对话测试和模型下载。

本仓库记录了一次真实可复现的实践：在免费 Tesla T4 上训练约 **30M 参数**的 MiniMind。教学配置使用 5 万条预训练样本和 5 万条 SFT 样本，最终权重约 64 MiB。它适合学习完整链路，不应期待达到商业聊天模型的能力。

## 你会学到什么

- 预训练、SFT、checkpoint 和推理分别是什么
- 如何用 Colab CLI 创建和操作免费 T4
- 如何下载 MiniMind 和官方数据集
- 如何把大数据裁成适合教学的规模
- 如何处理 Colab Python 版本、断线和 GPU 回收
- 如何下载模型并进行交互测试

## 架构

`本地 Mac/Linux 终端 → Colab CLI → 免费 T4 VM → MiniMind → Pretrain → SFT → .pth 模型`

## 前置条件

- macOS 或 Linux（官方 Colab CLI 暂不支持 Windows）
- Google 账号，可使用 Colab
- Git、curl 和稳定网络
- 不需要 GCP 项目，不需要信用卡，不需要本地 NVIDIA GPU

## 快速启动（首次完整运行通常约 1–2 小时）

```bash
git clone https://github.com/zhoujianbin/minimind-colab-free-gpu.git
cd minimind-colab-free-gpu
bash scripts/00_install_colab_cli.sh
bash scripts/01_create_t4_session.sh
SAMPLE_COUNT=50000 bash scripts/02_prepare_data.sh
bash scripts/03_train.sh
bash scripts/04_status.sh
```

首次执行 `colab new` 会打印 Google OAuth 地址。用准备使用 Colab 的账号授权，并把页面给出的代码粘贴回终端。上述命令只需几分钟即可启动，但下载数据和完整训练实测接近 1 小时，网络、T4 排队和免费配额会让总时间变化。若新 shell 找不到 `colab`，先执行 `export PATH="$HOME/.local/bin:$PATH"`。免费 T4 可能暂时申请失败，此时请稍后重试，而不要把 CPU 会话误当成 T4。

训练结束后：

```bash
bash scripts/06_download_models.sh
```

确认模型已经下载到本地后再释放会话：

```bash
bash scripts/07_stop_session.sh
```

## 第一步：安装 Colab CLI

本项目使用 Google 官方 [google-colab-cli](https://github.com/googlecolab/google-colab-cli)。脚本通过 uv 安装：

```bash
bash scripts/00_install_colab_cli.sh
colab version
```

若新终端提示找不到命令：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 第二步：申请 T4

```bash
bash scripts/01_create_t4_session.sh minimind-t4
colab sessions
colab status -s minimind-t4
```

免费 GPU 不保证随时可用。创建成功后应看到 `Hardware: T4` 和 `Tesla T4`。网页和 CLI 可能同时存在 CPU/GPU 两个会话；请以 `colab sessions` 为准。

常用命令：

```bash
colab ssh -s minimind-t4
colab url -s minimind-t4 --open
colab exec -s minimind-t4 -f your_script.py
colab stop -s minimind-t4
```

## 第三步：MiniMind 与数据

[MiniMind](https://github.com/jingyaogong/minimind) 是一个从零实现的小语言模型教学项目。本仓库不复制其源码，而是在运行时克隆官方仓库。

`scripts/02_prepare_data.sh` 会：

1. 克隆 MiniMind；
2. 只安装训练必需依赖；
3. 从 ModelScope 下载官方 mini 数据；
4. 从完整数据中截取指定条数，生成教学子集。

```bash
SAMPLE_COUNT=50000 bash scripts/02_prepare_data.sh
```

本次下载时完整预训练文件约 1.16GB；远端文件可能更新，请至少预留数 GB 磁盘和足够下载时间。降低到 1 万条适合验证流程；提高到 10 万条会增加覆盖量和训练时间，但是否改善效果必须通过固定评测验证。当前脚本为了精确复现实测结果，确定性地取文件前 N 行，而不是随机抽样，因此存在顺序偏差，并会生成包含样本数、版本和 SHA-256 的 manifest。

数据配比是训练超参数：本次预训练子集以创作生成（18.53%）和知识解释（18.21%）为主，代码技术仅约 3.67%；SFT 按 user 消息估算，身份与日常对话约 30.64%、知识解释约 26.55%、代码技术不足 1%。这与本次模型更容易自我介绍、但代码测试表现较弱的观察相关；由于没有对照实验，不能据此断言单一因果关系。由于原数据没有官方类别标签，这些比例是透明关键词规则的弱监督估算。长度方面，预训练样本平均约 203.5 token，27.3% 超过 256 token；5 万条 SFT 对话共约 35.5 万条消息。完整方法、局限、数据混合建议见 [数据配比、T4 性能与参数选择](docs/data-performance-hyperparameters.md)。可在 Colab 中运行：

```bash
python /content/tutorial/remote/analyze_data_mix.py
python /content/tutorial/remote/analyze_dataset.py
```

## 第四步：从零预训练

“从零”表示模型参数由随机数初始化，而不是下载一个现成模型再微调。预训练让模型学习文本的统计规律和“预测下一个 token”。

默认参数：

| 参数 | 值 |
|---|---:|
| hidden size | 512 |
| Transformer 层数 | 8 |
| 参数量 | 约 30M |
| 序列长度 | 256 |
| epoch | 1 |
| 有效 batch | 64 |

选择 512 hidden size 和 8 层，是为了把模型控制在约 30M 参数：能在 T4 16GB 上从零训练，又能比极小玩具模型展示更明显的学习过程。预训练使用 batch 16 × 梯度累积 4，兼顾显存和梯度稳定性。各参数的选择逻辑、OOM 时如何调整以及实验设计方法见 [参数详解](docs/data-performance-hyperparameters.md#5-参数为什么这样选)。

## 第五步：SFT

SFT 使用“用户问题—助手回答”数据，让完成预训练的模型学会遵循指令。脚本会自动在预训练结束后执行 SFT：

```bash
bash scripts/03_train.sh
watch -n 20 'bash scripts/04_status.sh'
```

输出：

```text
/content/minimind/out/pretrain_512.pth
/content/minimind/out/full_sft_512.pth
```

## 第六步：对话测试

进入远端：

```bash
bash scripts/05_chat.sh
```

脚本会通过 `colab exec` 在能访问 CUDA 的 Colab kernel 内执行推理；输入问题，输入 `exit` 结束。每次问题都会重新加载约 64 MiB 的教学模型，可能需要等待十几秒。普通 SSH shell 在部分 Colab 运行时看不到 CUDA，因此不用于启动 GPU 推理。也可以执行批量测试：

```bash
colab exec -s minimind-t4 -f remote/test_prompts.py --timeout 600
```

30M 模型 + 5 万条数据只能证明链路跑通。它可能出现事实错误、重复、病句或无法写代码，这不是训练失败，而是模型和数据规模的能力上限。

## 第七步：保存模型

Colab VM 是临时机器。**训练完成后第一件事就是下载权重：**

```bash
bash scripts/06_download_models.sh outputs
```

脚本会下载两个权重并计算 SHA-256。也可在 Notebook 中挂载 Drive 后运行 `remote/save_to_drive.py`。

## Notebook 备用路线

CLI 是主路线；如果想在网页理解每一步，可打开 [notebooks/colab_minimind_from_scratch.ipynb](notebooks/colab_minimind_from_scratch.ipynb)。Notebook 不会替代 CLI 会话管理。

## 发布前复现状态

每次发布前验证的环境、配置、耗时、哈希和已知限制记录在 [发布前复现报告](docs/reproducibility-report.md)。只有报告明确写明 T4 完整测试通过，才表示当前 commit 已在全新 T4 环境中端到端验证。

## 实测结果

一次实测配置：5 万条预训练 + 5 万条 SFT，Tesla T4：

- 模型参数：30.03M
- 两个权重各约 64 MiB
- 最新发布前复现：预训练 3125 个 DataLoader mini-batch step，393 秒
- 最新发布前复现：SFT 6250 个 DataLoader mini-batch step，725 秒
- 两阶段合计：1118 秒，即 18 分 38 秒
- 最终记录：预训练 loss 3.3587，SFT loss 2.3290
- optimizer update 数还要除以梯度累积步数，不能把日志 step 直接当作参数更新次数
- 另一历史会话曾用约 58 分钟；免费 T4 性能和资源回收时间并不稳定
- 推理速度：约 35–79 token/s
- 新版训练脚本会自动记录 `PRETRAIN_SECONDS`、`SFT_SECONDS` 和 `TOTAL_SECONDS`，方便比较不同 T4 会话和参数配置

结果能进行简单中文生成，但质量有限。要改善效果，可逐步增加数据量、epoch、上下文长度和模型尺寸，每次只改一个变量。

## 常见问题

详见 [docs/troubleshooting.md](docs/troubleshooting.md)。最重要的三条：

1. `nvidia-smi: command not found`：连到了 CPU 会话；检查 `colab sessions`。
2. `libnvidia-ml.so` 不存在：免费 GPU 可能已被收回，先下载模型。
3. pip 长时间编译 sklearn/numpy：不要安装完整 requirements，使用本项目的最小依赖方案。

## 成本与限制

Colab 免费资源不保证，可能限时、断线或回收 GPU。禁止挖矿、绕过限制、长期后台服务等违反 Colab 政策的行为。本项目仅用于学习和研究。

## 致谢与许可

- 模型与训练代码来自 [jingyaogong/minimind](https://github.com/jingyaogong/minimind)，Apache-2.0。
- Colab CLI 来自 [googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)。
- 本仓库原创内容使用 Apache-2.0。第三方版本、署名和许可证边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
- 教学数据集页面标示为 CC BY-NC 4.0，禁止未经许可的商业用途；数据和训练权重的使用权不由本仓库授予。
