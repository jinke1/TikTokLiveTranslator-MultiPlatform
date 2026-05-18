#!/usr/bin/env python3
"""
日志配置模块
"""

import logging
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = "TikTokTranslator",
    log_dir: str = "logs",
    level: int = logging.INFO
) -> logging.Logger:
    """
    配置日志
    
    Args:
        name: 日志名称
        log_dir: 日志目录
        level: 日志级别
    
    Returns:
        日志记录器
    """
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 文件处理器
    log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
