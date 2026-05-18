#!/usr/bin/env python3
"""
配置管理模块
"""

import json
from pathlib import Path
from typing import Any, Dict


class Config:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        "speech_recognition": {
            "model": "base",
            "language": "auto",
            "device": "cuda"
        },
        "translation": {
            "source_lang": "zh_CN",
            "target_lang": "en_XX",
            "device": "cuda"
        },
        "websocket": {
            "server_url": "ws://localhost:8000",
            "reconnect_interval": 5,
            "max_retries": 3
        },
        "logging": {
            "level": "INFO",
            "output": "logs/translator.log"
        }
    }
    
    def __init__(self, config_file: str = "config.json"):
        """初始化配置"""
        self.config_file = Path(config_file)
        self.config = self.DEFAULT_CONFIG.copy()
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config.update(json.load(f))
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value or default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
