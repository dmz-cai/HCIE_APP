@echo off
chcp 65001 >nul
title HCIE备考助手 一键打包工具
echo ========================================
echo 正在打包HCIE备考助手APP，请耐心等待...
echo ========================================
cd /d "%~dp0"
python -m python_for_android apk --name "HCIE备考助手" --package "org.hcie.hcietracker" --version "1.0" --requirements "kivy==2.3.0,kivymd==1.2.0,pillow" --arch "arm64-v8a" --icon "icon.png" --bootstrap "sdl2" --ndk-version "25.2.9519653" --api "33"
echo ========================================
echo 打包完成！按任意键退出...
echo ========================================
pause >nul