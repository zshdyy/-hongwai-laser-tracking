# Hongwai Laser Tracking（红外/激光视觉追踪）

南科大模电实验 / DIY 电赛题目相关：基于 **摄像头输入（OpenCV）** 的视觉检测与跟踪，并在树莓派上结合 **舵机云台（yaw/pitch）** 实现目标点（红点）对准/追踪控制。

> 仓库代码以 Python 为主，包含：
> - 摄像头采集与截图保存（`shot.py`）
> - 棋盘格相机标定（`calibrate.py`）
> - 树莓派 pigpio 舵机控制 + 视觉检测闭环（`home/analog/workspace/lab_code/controller.py`）

---

## 功能概览

- **摄像头实时采集**（OpenCV `VideoCapture`）
- **截图采集数据集**（按键保存到 `img/`）
- **棋盘格标定相机**（从 `./img/*.png` 读取棋盘格图像进行标定）
- **目标检测与闭环控制**（检测红点位置，计算误差，驱动 yaw/pitch 舵机调整）

---

## 目录结构（当前仓库）

- `home/analog/workspace/shot.py`  
  摄像头预览 + 按键截图保存到 `img/`
- `home/analog/workspace/calibrate.py`  
  从 `./img/*.png` 读取棋盘格图片并标定相机（打印相机内参、畸变等）
- `home/analog/workspace/lab_code/controller.py`  
  树莓派上运行的控制程序：调用摄像头取图、检测角点/矩形/红点，驱动 pigpio 控制舵机

---

## 环境与依赖

- Python 3（仓库依赖见 `requirements.txt`）
- OpenCV（`cv2`）
- NumPy
- 树莓派控制部分需要：
  - `pigpio`（并需要 pigpio daemon 正常运行）
  - 舵机接线到对应 GPIO（代码里 yaw=23, pitch=24）

---

## 快速开始（摄像头预览/截图）

进入项目目录（注意当前脚本使用相对路径保存 `img/`，建议在脚本所在目录运行）：

```bash
cd home/analog/workspace
python shot.py
```

按键说明（来自 `shot.py`）：
- `s`：保存当前帧到 `img/{idx}.png`
- `q`：退出

> 如果运行报“找不到摄像头/打不开摄像头”，请确认设备存在并尝试把 `VideoCapture(0)` 改成 `1` 或其他索引。

---

## 相机标定（棋盘格）

1. 先用 `shot.py` 拍摄棋盘格图像，存到 `home/analog/workspace/img/`
2. 运行标定脚本：

```bash
cd home/analog/workspace
python calibrate.py
```

说明：
- 标定脚本会读取 `./img/*.png`
- 棋盘格角点数量当前设定为：`CHECKERBOARD = (8, 11)`
- 程序会逐张显示检测到的角点，并最终输出：
  - Camera matrix（相机内参）
  - Distortion coefficient（畸变参数）
  - Rotation/Translation vectors（外参）

---

## 树莓派舵机控制与视觉闭环（controller）

入口：

```bash
cd home/analog/workspace/lab_code
python controller.py
```

你将看到交互输入（来自 `controller.py`）：
- 输入 `1`：reset（将舵机回到默认角度）
- 输入 `2`：big（执行一段预设“大范围”运动）
- 输入 `3`：small（执行基于检测结果的运动流程）
- 其他输入：退出

核心逻辑简述：
- `Camera()` 获取图像
- 检测矩形/角点并计算透视变换矩阵（`rectangle` / `corner`）
- 在 ROI/区域内检测红点（`red_point`），得到当前坐标 `(Mx, My)`
- 计算误差并迭代更新 yaw/pitch 角度，通过 `pigpio` 输出 PWM 脉宽控制舵机

> 注意：`controller.py` 依赖 `detector` 模块与 `camera` 封装（位于 `home/analog/workspace/lab_code/detector/`）。如果你在非树莓派环境运行，`pigpio` 可能不可用。

---

## 常见问题（FAQ）

### 1. 摄像头打不开（`VideoCapture(0)` 失败）
- 尝试更换索引：`VideoCapture(1)` / `VideoCapture(2)`
- 确认系统没有被其它程序占用摄像头
- 在树莓派上确认摄像头已启用并能被系统识别

### 2. `img/` 目录不存在导致保存失败
在 `home/analog/workspace` 下新建 `img` 目录：
```bash
mkdir -p img
```

### 3. 树莓派 pigpio 相关
- 确认已安装并启动 pigpio daemon（不同系统命令可能不同）
- 确认 GPIO 引脚号与接线一致（代码中 yaw=23, pitch=24）

---

## 许可证
当前仓库未添加 LICENSE。如需开源发布，建议补充 MIT 或 Apache-2.0。