# 调研与实测记录

- 官方 Colab CLI 包名：google-colab-cli，命令为 colab。
- T4 会话命令：colab new -s minimind-t4 --gpu T4。
- MiniMind 仓库：https://github.com/jingyaogong/minimind
- 实测 Colab 新运行时可能使用 Python 3.13，旧版 numpy/scikit-learn 会从源码编译；本项目只安装训练必要依赖，避免完整 requirements。
- 实测规模：hidden_size=512、8 层，约 30M 参数；权重约 64 MiB。
- 免费 GPU 可能被回收，必须及时下载 checkpoint。
- CLI 创建的运行时在网页中可能显示为“未知笔记本 GPU”。
