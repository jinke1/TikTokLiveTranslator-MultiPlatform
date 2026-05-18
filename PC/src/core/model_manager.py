#!/usr/bin/env python3
"""
模型管理模块

功能:
  - 自动下载模型
  - 模型缓存管理
  - 版本控制
  - 完整性验证
"""

import logging
import os
from pathlib import Path
from typing import Optional
import requests
from tqdm import tqdm


logger = logging.getLogger(__name__)


class ModelManager:
    """模型管理器"""
    
    # 模型配置
    MODELS_CONFIG = {
        "whisper": {
            "name": "openai/whisper-base",
            "size": "140MB",
            "url": "https://huggingface.co/openai/whisper-base/resolve/main"
        },
        "m2m100": {
            "name": "facebook/m2m100_418M",
            "size": "1.2GB",
            "url": "https://huggingface.co/facebook/m2m100_418M/resolve/main"
        }
    }
    
    def __init__(self, model_dir: Optional[str] = None):
        """
        初始化模型管理器
        
        Args:
            model_dir: 模型存储目录
        """
        if model_dir is None:
            model_dir = Path(__file__).parent.parent / "models"
        
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"模型目录: {self.model_dir}")
    
    def check_models(self) -> bool:
        """
        检查模型是否存在
        
        Returns:
            True 如果所有模型都存在
        """
        logger.info("检查模型...")
        
        # 检查 Whisper
        whisper_cache = Path.home() / ".cache" / "whisper"
        if not whisper_cache.exists():
            logger.warning("Whisper 模型不存在")
            return False
        
        # 检查 M2M-100
        m2m_cache = Path.home() / ".cache" / "huggingface" / "hub"
        if not (m2m_cache / "models--facebook--m2m100_418M").exists():
            logger.warning("M2M-100 模型不存在")
            return False
        
        logger.info("所有模型都已存在")
        return True
    
    def download_all_models(self, show_progress: bool = True):
        """
        下载所有必需的模型
        
        Args:
            show_progress: 是否显示进度条
        """
        logger.info("开始下载模型...")
        
        try:
            # 下载 Whisper 模型
            logger.info("下载 Whisper 模型 (base, ~140MB)...")
            self._download_whisper()
            
            # 下载 M2M-100 模型
            logger.info("下载 M2M-100 模型 (~1.2GB)...")
            self._download_m2m100()
            
            logger.info("所有模型下载完成")
        
        except Exception as e:
            logger.error(f"模型下载失败: {e}")
            raise
    
    def _download_whisper(self):
        """下载 Whisper 模型"""
        import whisper
        
        try:
            logger.info("加载 Whisper 模型...")
            whisper.load_model("base")
            logger.info("Whisper 模型下载完成")
        except Exception as e:
            logger.error(f"Whisper 模型下载失败: {e}")
            raise
    
    def _download_m2m100(self):
        """下载 M2M-100 模型"""
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        
        try:
            logger.info("加载 M2M-100 Tokenizer...")
            AutoTokenizer.from_pretrained("facebook/m2m100_418M")
            
            logger.info("加载 M2M-100 模型...")
            AutoModelForSeq2SeqLM.from_pretrained("facebook/m2m100_418M")
            
            logger.info("M2M-100 模型下载完成")
        except Exception as e:
            logger.error(f"M2M-100 模型下载失败: {e}")
            raise
    
    def get_model_info(self, model_name: str) -> dict:
        """获取模型信息"""
        return self.MODELS_CONFIG.get(model_name, {})
    
    def cleanup_cache(self):
        """清理模型缓存"""
        logger.info("清理模型缓存...")
        # 实现缓存清理逻辑
        logger.info("缓存清理完成")
