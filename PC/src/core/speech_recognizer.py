#!/usr/bin/env python3
"""
语音识别模块 - 基于 OpenAI Whisper

支持:
  - 实时音频流处理
  - 多语言自动检测
  - GPU 加速
  - 5 种精度模型 (tiny → large)
"""

import logging
import numpy as np
from typing import Optional, Callable
import whisper
import torch


logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """Whisper 语音识别引擎"""
    
    # 支持的模型
    MODELS = ["tiny", "base", "small", "medium", "large"]
    
    # 模型信息
    MODEL_INFO = {
        "tiny": {"size": "39MB", "speed": "fastest", "accuracy": "low"},
        "base": {"size": "74MB", "speed": "fast", "accuracy": "medium"},
        "small": {"size": "244MB", "speed": "medium", "accuracy": "good"},
        "medium": {"size": "769MB", "speed": "slow", "accuracy": "high"},
        "large": {"size": "1.5GB", "speed": "slowest", "accuracy": "highest"},
    }
    
    def __init__(
        self,
        model_name: str = "base",
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        language: Optional[str] = None
    ):
        """
        初始化语音识别器
        
        Args:
            model_name: 模型名称 (tiny/base/small/medium/large)
            device: 计算设备 (cuda/cpu)
            language: 语言代码 (如 "zh", "en")，None 为自动检测
        """
        self.model_name = model_name
        self.device = device
        self.language = language
        self.model = None
        self.on_result: Optional[Callable] = None
        
        logger.info(f"初始化 Whisper 识别器: 模型={model_name}, 设备={device}")
        self._load_model()
    
    def _load_model(self):
        """加载 Whisper 模型"""
        try:
            logger.info(f"加载模型 {self.model_name}...")
            self.model = whisper.load_model(
                self.model_name,
                device=self.device
            )
            logger.info(f"模型加载成功")
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            raise
    
    def recognize_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> dict:
        """
        识别音频
        
        Args:
            audio_data: 音频数据 (numpy 数组)
            sample_rate: 采样率 (Hz)
        
        Returns:
            识别结果字典:
                {
                    "text": str,           # 识别的文本
                    "language": str,       # 检测到的语言
                    "confidence": float,   # 置信度
                    "segments": list       # 分段信息
                }
        """
        try:
            # 确保音频是单声道
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # 归一化音频
            audio_data = audio_data.astype(np.float32)
            audio_data = audio_data / (np.max(np.abs(audio_data)) + 1e-10)
            
            # 使用 Whisper 识别
            result = self.model.transcribe(
                audio=audio_data,
                language=self.language,
                verbose=False,
                fp16=torch.cuda.is_available()
            )
            
            logger.info(
                f"识别完成: "
                f"文本='{result['text'][:50]}...', "
                f"语言={result['language']}"
            )
            
            return {
                "text": result["text"],
                "language": result["language"],
                "confidence": self._calculate_confidence(result),
                "segments": result.get("segments", [])
            }
        
        except Exception as e:
            logger.error(f"语音识别失败: {e}")
            raise
    
    def recognize_file(self, file_path: str) -> dict:
        """
        识别音频文件
        
        Args:
            file_path: 音频文件路径
        
        Returns:
            识别结果
        """
        try:
            logger.info(f"读取音频文件: {file_path}")
            # Whisper 会自动处理音频加载
            result = self.model.transcribe(
                audio=file_path,
                language=self.language,
                verbose=False
            )
            
            return {
                "text": result["text"],
                "language": result["language"],
                "confidence": self._calculate_confidence(result),
                "segments": result.get("segments", [])
            }
        
        except Exception as e:
            logger.error(f"识别音频文件失败: {e}")
            raise
    
    def _calculate_confidence(self, result: dict) -> float:
        """
        计算识别置信度
        
        Args:
            result: Whisper 识别结果
        
        Returns:
            置信度 (0-1)
        """
        if not result.get("segments"):
            return 0.0
        
        # 基于分段数量和文本长度的简单置信度计算
        segments = result["segments"]
        avg_no_speech_prob = np.mean([
            s.get("no_speech_prob", 0) for s in segments
        ])
        
        return max(0.0, 1.0 - avg_no_speech_prob)
    
    def set_language(self, language_code: str):
        """设置识别语言"""
        self.language = language_code
        logger.info(f"设置语言: {language_code}")
    
    def get_model_info(self) -> dict:
        """获取当前模型信息"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "language": self.language or "auto",
            "info": self.MODEL_INFO.get(self.model_name, {})
        }
    
    def release(self):
        """释放资源"""
        try:
            if self.model is not None:
                del self.model
            logger.info("语音识别器已释放")
        except Exception as e:
            logger.error(f"释放资源失败: {e}")
