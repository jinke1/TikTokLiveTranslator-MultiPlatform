#!/usr/bin/env python3
"""
PyQt5 图形用户界面

主窗口包含:
  - 翻译引擎控制
  - 实时翻译显示
  - 设置面板
  - 翻译历史
"""

import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTextEdit,
    QTabWidget, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

from core.speech_recognizer import SpeechRecognizer
from core.translator import Translator


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TikTok Live Translator - PC 端")
        self.setGeometry(100, 100, 1000, 700)
        
        # 初始化翻译引擎
        try:
            self.speech_recognizer = SpeechRecognizer(model_name="base")
            self.translator = Translator()
            logger.info("翻译引擎初始化成功")
        except Exception as e:
            logger.error(f"翻译引擎初始化失败: {e}")
            QMessageBox.critical(self, "错误", f"初始化失败: {e}")
            return
        
        # 创建 UI
        self._create_ui()
    
    def _create_ui(self):
        """创建用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel("TikTok 直播实时翻译")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 创建选项卡
        tabs = QTabWidget()
        
        # 翻译选项卡
        tabs.addTab(self._create_translation_tab(), "翻译")
        
        # 设置选项卡
        tabs.addTab(self._create_settings_tab(), "设置")
        
        # 历史记录选项卡
        tabs.addTab(self._create_history_tab(), "历史")
        
        layout.addWidget(tabs)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        central_widget.setLayout(layout)
    
    def _create_translation_tab(self) -> QWidget:
        """创建翻译选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 原文显示
        layout.addWidget(QLabel("原文:"))
        self.original_text = QTextEdit()
        self.original_text.setPlaceholderText("输入要翻译的文本或点击开始录音")
        layout.addWidget(self.original_text)
        
        # 翻译结果
        layout.addWidget(QLabel("翻译结果:"))
        self.translated_text = QTextEdit()
        self.translated_text.setReadOnly(True)
        self.translated_text.setPlaceholderText("翻译结果将显示在这里")
        layout.addWidget(self.translated_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.translate_btn = QPushButton("翻译")
        self.translate_btn.clicked.connect(self._on_translate)
        button_layout.addWidget(self.translate_btn)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self._on_clear)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        widget.setLayout(layout)
        return widget
    
    def _create_settings_tab(self) -> QWidget:
        """创建设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 源语言选择
        layout.addWidget(QLabel("源语言:"))
        self.source_lang = QComboBox()
        self.source_lang.addItems(["中文 (Chinese)", "英文 (English)", "日文 (Japanese)"])
        layout.addWidget(self.source_lang)
        
        # 目标语言选择
        layout.addWidget(QLabel("目标语言:"))
        self.target_lang = QComboBox()
        self.target_lang.addItems(["英文 (English)", "中文 (Chinese)", "日文 (Japanese)"])
        layout.addWidget(self.target_lang)
        
        # Whisper 模型选择
        layout.addWidget(QLabel("Whisper 模型:"))
        self.whisper_model = QComboBox()
        self.whisper_model.addItems(["tiny", "base", "small", "medium", "large"])
        self.whisper_model.setCurrentText("base")
        layout.addWidget(self.whisper_model)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_history_tab(self) -> QWidget:
        """创建历史记录选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setPlaceholderText("翻译历史将显示在这里")
        layout.addWidget(self.history_text)
        
        # 清除历史按钮
        clear_history_btn = QPushButton("清除历史")
        clear_history_btn.clicked.connect(self._on_clear_history)
        layout.addWidget(clear_history_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _on_translate(self):
        """翻译按钮点击事件"""
        text = self.original_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "警告", "请输入要翻译的文本")
            return
        
        try:
            self.status_bar.showMessage("翻译中...")
            
            result = self.translator.translate(
                text,
                source_lang="zh_CN",
                target_lang="en_XX"
            )
            
            self.translated_text.setText(result["translated"])
            self.status_bar.showMessage(f"翻译完成 (置信度: {result['confidence']:.2%})")
            
            # 添加到历史
            self._add_to_history(text, result["translated"])
        
        except Exception as e:
            logger.error(f"翻译错误: {e}")
            QMessageBox.critical(self, "错误", f"翻译失败: {e}")
            self.status_bar.showMessage("翻译失败")
    
    def _on_clear(self):
        """清空按钮点击事件"""
        self.original_text.clear()
        self.translated_text.clear()
        self.status_bar.showMessage("已清空")
    
    def _on_clear_history(self):
        """清除历史按钮点击事件"""
        self.history_text.clear()
        self.status_bar.showMessage("历史记录已清除")
    
    def _add_to_history(self, original: str, translated: str):
        """添加翻译到历史"""
        history = self.history_text.toPlainText()
        new_entry = f"原文: {original}\n译文: {translated}\n---\n"
        self.history_text.setText(new_entry + history)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        try:
            self.speech_recognizer.release()
            self.translator.release()
            logger.info("资源已释放")
        except Exception as e:
            logger.error(f"释放资源时出错: {e}")
        event.accept()
