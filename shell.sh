#!/bin/bash
# 安装 Python 和 pip（如果尚未安装）
sudo apt update
sudo apt install python3 python3-pip -y

# 安装 Playwright
pip install playwright

# 运行 Playwright 安装脚本下载浏览器
playwright install
