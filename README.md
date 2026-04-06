# HCIE 备考助手 APP

一个用于记录开销、学习打卡、任务管理的手机应用。

## 功能

- 💰 **记账** - 记录日常开销和 HCIE 备考费用
- 🧠 **学习打卡** - 记录学习时长，追踪备考进度
- ✅ **任务管理** - 添加自定义任务，完成打卡
- 📊 **数据统计** - 查看总支出、学习时长、任务完成情况

## 如何编译 APK

### 方法一：GitHub Actions（推荐）

1. 在 GitHub 创建新仓库 `HCIE_APP`
2. 上传这个文件夹的所有文件到仓库
3. GitHub 会自动运行构建
4. 构建完成后，在 Actions → Build HCIE APK → Artifacts 下载 APK

### 方法二：本地编译（需要 Linux）

```bash
# 安装依赖
pip install buildozer cython==0.29.36
sudo apt install -y git zip unzip openjdk-17-jdk wget

# 编译
cd HCIE_APP
buildozer init
# 修改 buildozer.spec 配置
buildozer android debug
```

### 方法三：使用 Docker

```bash
docker pull kivy/buildozer
docker run --rm -v "$PWD":/app kivy/buildozer android debug
```

## 安装到手机

编译成功后，将 APK 文件传输到手机，直接安装即可。

## 自定义任务

在应用内点击「任务管理」→「添加任务」，输入任务名称和描述即可创建自定义打卡任务。
