# 摄像头驱动与采集 | Camera

## 支持的摄像头类型

| 类型 | 接口 | 推荐型号 | 备注 |
|------|------|---------|------|
| CSI 摄像头 | CSI FPC 排线 | Raspberry Pi Camera Module v2 / v3 | 官方推荐，延迟低 |
| USB 摄像头 | USB-A | 罗技 C270 / C920 | 兼容性好，即插即用 |

---

## CSI 摄像头使用

### 检查摄像头是否被识别

```bash
vcgencmd get_camera
# 输出应为：supported=1 detected=1
```

### 拍照测试

```bash
raspistill -o photo.jpg -w 1280 -h 720
```

### 在 Python / OpenCV 中使用

```python
import cv2

# 对于 CSI 摄像头（Raspberry Pi OS 新版本）
cap = cv2.VideoCapture(0)

# 设置分辨率（可选，降低分辨率提升帧率）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print(f"分辨率: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x"
      f"{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"帧率: {cap.get(cv2.CAP_PROP_FPS)} fps")
```

---

## 使用 picamera2（新版系统推荐）

```bash
pip3 install picamera2
```

```python
from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))
picam2.start()

while True:
    frame = picam2.capture_array()
    # picamera2 返回 RGB，OpenCV 使用 BGR
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('Camera', frame_bgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
```

---

## 性能调优

| 方法 | 效果 |
|------|------|
| 降低分辨率至 480p | 帧率提升约 2x |
| 关闭图像显示（`imshow`） | 减少 CPU 占用 |
| 使用 `cv2.resize` 在采集后缩放 | 避免高分辨率采集开销 |
| 多线程采集与处理分离 | 避免 I/O 阻塞处理线程 |

---

## 多线程采集示例框架

```python
import cv2
import threading


class CameraThread:
    """后台线程持续采集，主线程只取最新帧。"""

    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.frame = None
        self.running = True
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()
```
