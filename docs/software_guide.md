# 软件环境配置指南 | Software Guide

## 开发环境概览

```
本地 PC（开发、调试）
 ├── VS Code + Remote SSH 插件（远程编辑树莓派代码）
 ├── Git（版本管理）
 └── LTspice / Multisim（电路仿真）

Raspberry Pi（运行环境）
 ├── Raspberry Pi OS 64-bit
 ├── Python 3.9+
 ├── OpenCV 4.x
 └── RPi.GPIO / pigpio
```

---

## 在树莓派上安装 OpenCV

### 方法一：pip 安装（推荐，最简单）

```bash
pip3 install opencv-python-headless numpy
```

### 方法二：apt 安装

```bash
sudo apt install python3-opencv
```

### 方法三：从源码编译（耗时 2~4小时，但性能最优）

```bash
# 安装依赖
sudo apt install -y build-essential cmake git
sudo apt install -y libgtk-3-dev libboost-all-dev
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev

# 克隆源码
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

# 编译（树莓派4B 约2小时）
cd opencv && mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D ENABLE_NEON=ON ..
make -j4
sudo make install
```

---

## VS Code 远程开发配置

1. 安装扩展：`Remote - SSH`
2. 按 `F1` → `Remote-SSH: Connect to Host`
3. 输入 `pi@raspberrypi.local`
4. 在树莓派上直接编写、运行 Python 代码

---

## Python 虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活
source venv/bin/activate   # Linux / macOS / Raspberry Pi

# 安装依赖
pip install opencv-python-headless numpy RPi.GPIO pyserial

# 导出依赖清单（方便团队复现）
pip freeze > requirements.txt

# 其他成员复现
pip install -r requirements.txt
```

---

## Git 工作流建议

```bash
# 克隆仓库
git clone https://github.com/zshdyy/-.git

# 新功能开发：建立功能分支
git checkout -b feature/color-detection

# 提交代码
git add .
git commit -m "feat: 添加绿色目标颜色识别功能"

# 推送并发起 PR
git push origin feature/color-detection
```

提交信息格式参考（[Conventional Commits](https://www.conventionalcommits.org/)）：

| 前缀 | 含义 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `refactor:` | 代码重构 |
| `test:` | 测试相关 |
