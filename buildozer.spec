[app]

# (str) Title of your application
title = HCIE备考助手

# (str) Package name
package.name = hcie_tracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.hcie

# (str) Source code where the main.py live
source = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd,pillow

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = VIBRATE,INTERNET,WAKE_LOCK,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25.2.9519653

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = error, info, 2 = error, info, debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
