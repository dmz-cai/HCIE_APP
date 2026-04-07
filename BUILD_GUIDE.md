# HCIE 备考助手 - 构建说明

## 当前状态
- ✅ Python 3.10.11 已安装
- ✅ Kivy 2.3.1 已安装
- ✅ KivyMD 1.2.0 已安装
- ✅ Buildozer 1.5.0 已安装
- ✅ 应用在 Windows 上运行正常
- ❌ Docker Desktop 下载超时（网络太慢）
- ❌ WSL 不可用（Hyper-V 未启用）

## 当前状态（2026-04-07 晚）

网络仍然无法访问外网（GitHub、Google 都超时）。
所有代理端口（10800-10809, 7890-7891, 8080, 8118）测试均失败。

### 已完成
- ✅ Python 3.10.11 + Kivy + KivyMD + Buildozer 安装完成
- ✅ 应用在 Windows 运行正常
- ✅ buildozer.spec 修复完成

### 待完成（需要网络）
- ❌ GitHub 代码推送
- ❌ GitHub Actions 自动构建
- ❌ Docker 本地编译

---

## 🚀 立即可用方案：Kivy Launcher（无需网络）

不需要编译 APK，直接在手机上运行 Python 代码！

### 步骤：
1. 手机安装 **Kivy Launcher**（从 Google Play 或应用商店搜索）
   - 下载地址：https://play.google.com/store/apps/details?id=org.kivy.launcher
2. 电脑上把 `HCIE_APP` 文件夹复制到手机
   - 用数据线连接，复制到手机存储
   - 或者用微信/QQ传文件
3. 把文件夹放到手机：`/sdcard/kivy/HCIE_APP/`
4. 打开 Kivy Launcher，就能看到 HCIE_APP 并直接运行

### 注意：
- `main.py` 必须在文件夹根目录
- 文件夹路径必须是 `/sdcard/kivy/应用名/`

---

## 方案二：GitHub Actions 构建 APK（需要网络）

代码已推送到 GitHub。等网络恢复后：
1. 确保 `.github/workflows/build.yml` 已上传
2. 在 GitHub Actions 页面点击 Run workflow
3. 等待 15-20 分钟构建完成
4. 下载 APK

仓库地址：https://github.com/dmz-cai/HCIE_APP

---

## 方案三：本地 Docker 构建（等网络好时）

Docker Desktop 需要重新下载（590MB），下载好后：
1. 安装 Docker Desktop
2. 运行以下命令构建 APK：
```
docker run --rm -v "%cd%":/app kivy/buildozer android debug
```

---

## 方案四：WSL 构建（需要管理员权限）

需要以管理员身份运行以下命令启用 Hyper-V：
```
bcdedit /set hypervisorlaunchtype auto
wsl --update
# 重启电脑后
wsl -d Ubuntu
cd /mnt/c/Users/caiweinan/Desktop/HCIE_APP
pip install buildozer cython==0.29.36
buildozer android debug
```

---

## 推荐顺序
1. 🥇 **方案一（Kivy Launcher）** — 最快，现在就能用
2. 🥈 **方案二（GitHub Actions）** — 等网络恢复
3. 🥉 **方案三/四** — 需要 Docker 或 WSL
