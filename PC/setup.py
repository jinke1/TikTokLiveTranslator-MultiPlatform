#!/usr/bin/env python3
"""
PC 端安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tiktok-live-translator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="TikTok Live Translator - Cross-Platform Real-Time Translation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinke1/TikTokLiveTranslator-MultiPlatform",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "openai-whisper>=20230314",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "PyQt5>=5.15.0",
        "fastapi>=0.100.0",
        "websockets>=11.0.0",
    ],
    entry_points={
        "console_scripts": [
            "tiktok-translator=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
