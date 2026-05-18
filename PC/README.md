# TikTok Live Translator - PC 端

PC 端是整个系统的核心翻译引擎，负责语音识别和文本翻译。

## 功能特性

✅ OpenAI Whisper 语音识别  
✅ Meta M2M-100 多语言翻译  
✅ PyQt5 图形界面  
✅ GPU 加速处理  
✅ WebSocket 实时通信  
✅ 翻译历史记录  

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 首次运行

```bash
python src/main.py
```

首次运行会自动下载模型（约 1.5GB），请确保网络连接良好。

### 3. 使用应用

- **翻译文本**: 输入文本后点击"翻译"按钮
- **选择语言**: 在"设置"选项卡中选择源语言和目标语言
- **查看历史**: 在"历史"选项卡中查看翻译记录

## 系统要求

- Python 3.8+
- 4GB+ RAM
- 2GB+ GPU 显存 (可选)
- 2GB+ 磁盘空间 (模型存储)

## 目录结构

```
PC/
├── src/
│   ├── main.py                  # 主程序
│   ├── core/                    # 核心模块
│   │   ├── speech_recognizer.py # 语音识别
│   │   ├── translator.py        # 文本翻译
│   │   └── model_manager.py     # 模型管理
│   ├── ui/                      # 用户界面
│   │   └── gui.py               # PyQt5 主窗口
│   └── utils/                   # 工具类
│       ├── logger.py            # 日志记录
│       └── config.py            # 配置管理
├── requirements.txt             # Python 依赖
├── setup.py                     # 安装脚本
└── README.md                    # 本文件
```

## 常见问题

**Q: 为什么启动这么慢？**
A: 首次启动需要加载 Whisper 和 M2M-100 模型，这可能需要几分钟。

**Q: 翻译质量如何？**
A: 使用 Meta 的 M2M-100 模型，质量优于免费在线翻译。

**Q: 如何加速推理？**
A: 使用 GPU 加速。确保安装了 CUDA 和 cuDNN，设置会自动检测 GPU。
