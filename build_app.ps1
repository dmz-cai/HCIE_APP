# 一键打包 HCIE 备考助手 APP - PowerShell 原生脚本
Write-Host "开始打包 HCIE 备考助手 APP..." -ForegroundColor Green

# 执行打包命令（PowerShell 原生兼容版）
python -m python_for_android apk `
--name "HCIE备考助手" `
--package "org.hcie.hcietracker" `
--version "1.0" `
--requirements "kivy==2.3.0,kivymd==1.2.0,pillow" `
--arch "arm64-v8a" `
--icon "icon.png" `
--bootstrap "sdl2" `
--ndk-version "25.2.9519653" `
--api "33"

Write-Host "打包完成！APK 已生成在 .buildozer 目录下" -ForegroundColor Green
Pause