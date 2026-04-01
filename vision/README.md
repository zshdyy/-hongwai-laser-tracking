# 计算机视觉模块 | Computer Vision

本模块基于 **OpenCV** 实现图像识别与目标检测功能，运行在 Raspberry Pi 平台上，主要用于电赛中需要视觉感知的应用场景。

---

## 模块概览

| 子模块 | 功能描述 | 典型应用 |
|--------|---------|---------|
| [颜色识别](./color_detection/) | HSV 色彩空间分割 | 循迹、色标检测 |
| [形状识别](./shape_detection/) | 轮廓提取与多边形拟合 | 几何目标定位 |
| [目标追踪](./target_tracking/) | 帧间目标持续跟踪 | 运动物体追踪 |
| [工具函数](./utils/) | 图像预处理、调试辅助 | 公共依赖 |

---

## 环境依赖

```bash
# Python 3.7+
pip install opencv-python numpy
# 或在树莓派上
pip3 install opencv-python-headless numpy
```

验证安装：
```python
import cv2
print(cv2.__version__)  # 应输出 4.x.x
```

---

## 快速示例：打开摄像头并显示画面

```python
import cv2

cap = cv2.VideoCapture(0)  # 0 = 默认摄像头

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 处理流程

```
摄像头采集
    │
    ▼
图像预处理（缩放、去噪、色彩空间转换）
    │
    ▼
特征提取（颜色 / 边缘 / 轮廓）
    │
    ▼
目标识别与定位
    │
    ▼
输出控制信号（GPIO / 串口）
```

---

## 推荐学习资源

- OpenCV 官方文档：https://docs.opencv.org/4.x/
- 《Learning OpenCV 4》—— Adrian Kaehler & Gary Bradski
- [PyImageSearch 博客](https://pyimagesearch.com/)（英文，实战案例丰富）
- [OpenCV 中文文档](https://www.woshicver.com/)
