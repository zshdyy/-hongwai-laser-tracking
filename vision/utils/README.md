# 工具函数 | Utilities

公共辅助函数，供各视觉子模块调用。

---

## 图像预处理

```python
import cv2
import numpy as np


def preprocess(frame, width=640, height=480, blur_ksize=5):
    """
    标准图像预处理流程：缩放 → 高斯模糊。
    """
    resized = cv2.resize(frame, (width, height))
    blurred = cv2.GaussianBlur(resized, (blur_ksize, blur_ksize), 0)
    return blurred


def to_hsv(frame):
    """BGR 转 HSV 色彩空间。"""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


def draw_fps(frame, fps):
    """在图像左上角绘制帧率。"""
    cv2.putText(frame, f'FPS: {fps:.1f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    return frame
```

---

## FPS 计算器

```python
import time


class FPSCounter:
    """简单帧率计算器。"""

    def __init__(self, window=30):
        self.timestamps = []
        self.window = window

    def tick(self):
        self.timestamps.append(time.time())
        if len(self.timestamps) > self.window:
            self.timestamps.pop(0)

    @property
    def fps(self):
        if len(self.timestamps) < 2:
            return 0.0
        elapsed = self.timestamps[-1] - self.timestamps[0]
        return (len(self.timestamps) - 1) / elapsed if elapsed > 0 else 0.0
```

---

## HSV 阈值调参工具

```python
import cv2
import numpy as np


def nothing(x):
    pass


def hsv_tuner(source=0):
    """
    交互式 HSV 阈值调参工具。
    使用滑动条实时调整 H/S/V 上下限，方便确定颜色分割参数。
    """
    cap = cv2.VideoCapture(source)
    cv2.namedWindow('HSV Tuner')

    params = [('H_min', 0), ('H_max', 180),
              ('S_min', 0), ('S_max', 255),
              ('V_min', 0), ('V_max', 255)]
    for name, default in params:
        cv2.createTrackbar(name, 'HSV Tuner', default,
                           180 if 'H' in name else 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([
            cv2.getTrackbarPos('H_min', 'HSV Tuner'),
            cv2.getTrackbarPos('S_min', 'HSV Tuner'),
            cv2.getTrackbarPos('V_min', 'HSV Tuner'),
        ])
        upper = np.array([
            cv2.getTrackbarPos('H_max', 'HSV Tuner'),
            cv2.getTrackbarPos('S_max', 'HSV Tuner'),
            cv2.getTrackbarPos('V_max', 'HSV Tuner'),
        ])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('HSV Tuner', frame)
        cv2.imshow('Mask', mask)
        cv2.imshow('Result', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f'lower = np.array({lower.tolist()})')
            print(f'upper = np.array({upper.tolist()})')
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    hsv_tuner()
```
