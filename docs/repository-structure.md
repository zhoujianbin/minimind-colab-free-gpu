# 仓库结构

```text
.
├── README.md                  # 主教程
├── scripts/                   # 本地执行的 Colab CLI 命令
├── remote/                    # 上传到 Colab VM 的代码
├── notebooks/                # 网页备用路线
├── docs/                      # 概念、实测记录、故障排查
├── data/README.md             # 数据说明
├── Makefile                   # 静态检查
└── LICENSE
```

本地脚本只负责会话管理和文件传输；真正的数据处理与训练发生在 Colab VM 的 `/content`。模型权重被 .gitignore 排除，避免误提交大文件。
