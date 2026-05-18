#!/usr/bin/env python3
"""
TikTok Live Translator - PC 端主程序

功能:
  - 语音识别 (Whisper)
  - 文本翻译 (M2M-100)
  - 实时弹幕翻译
  - WebSocket 通信
  - PyQt5 GUI 界面
"""

import sys
import logging
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from PyQt5.QtWidgets import QApplication
from core.model_manager import ModelManager
from ui.gui import MainWindow
from utils.logger import setup_logger


def main():
    """主函数 - 应用入口"""
    
    # 设置日志
    logger = setup_logger()
    logger.info("=" * 50)
    logger.info("TikTok Live Translator - PC 端启动")
    logger.info("=" * 50)
    
    try:
        # 检查并下载模型
        logger.info("检查模型...")
        model_manager = ModelManager()
        
        if not model_manager.check_models():
            logger.warning("检测到模型缺失，正在下载...")
            model_manager.download_all_models()
        
        logger.info("模型检查完成")
        
        # 创建 PyQt5 应用
        app = QApplication(sys.argv)
        app.setApplicationName("TikTok Live Translator")
        app.setApplicationVersion("1.0.0")
        
        # 创建主窗口
        logger.info("创建主窗口...")
        window = MainWindow()
        window.show()
        
        logger.info("应用已启动，窗口已显示")
        
        # 运行应用
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"应用启动失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
