[app]

title = HCIE备考助手
package.name = hcie_tracker
package.domain = org.hcie
source = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.permissions = VIBRATE,INTERNET,WAKE_LOCK,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
