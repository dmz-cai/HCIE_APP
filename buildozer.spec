[app]
title = HCIETracker
package.name = hcietracker
package.domain = org.hcie
source.dir = .
source.include_exts = py,png,jpg
version = 1.0
# 核心：指定稳定的依赖版本，避免编译冲突
requirements = python3==3.11.4,kivy==2.3.0,kivymd==1.2.0,pillow==10.2.0
orientation = portrait
fullscreen = 0
# Android 编译配置（稳定版，避免兼容性问题）
android.api = 33
android.ndk = 25.1.9470188
android.sdk = 24
android.accept_sdk_license = True
android.enable_androidx = True
android.archs = arm64-v8a
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = ~/.buildozer/android/platform/android-sdk
