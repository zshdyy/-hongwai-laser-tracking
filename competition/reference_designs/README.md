# 参考设计 | Reference Designs

## 视觉循迹小车参考方案

### 硬件清单

| 元件 | 规格 | 数量 |
|------|------|------|
| Raspberry Pi 4B | 4GB RAM | 1 |
| CSI 摄像头 | Camera Module v2 | 1 |
| 电机驱动 | L298N 双路 | 1 |
| 直流减速电机 | 12V / 100RPM | 2 |
| 锂电池 | 11.1V 2200mAh | 1 |
| 降压模块 | XL4016 12V→5V 3A | 1 |
| 小车底盘 | 两轮差速 | 1 |

---

### 软件框架

```python
# main.py - 视觉循迹小车主程序框架

import cv2
import RPi.GPIO as GPIO
from camera_thread import CameraThread      # 见 raspberry_pi/camera/
from color_detection import detect_color    # 见 vision/color_detection/


# --- GPIO 配置 ---
IN1, IN2 = 17, 18   # 左电机
IN3, IN4 = 22, 23   # 右电机
ENA, ENB = 12, 13   # PWM 使能

GPIO.setmode(GPIO.BCM)
for pin in [IN1, IN2, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)
left_pwm  = GPIO.PWM(ENA, 1000)
right_pwm = GPIO.PWM(ENB, 1000)
left_pwm.start(0)
right_pwm.start(0)


def set_motors(left_speed, right_speed):
    """
    设置左右电机速度。
    speed 范围：-100 ~ +100（负数为反转）
    """
    def drive(in_a, in_b, pwm_ctrl, speed):
        if speed >= 0:
            GPIO.output(in_a, GPIO.HIGH)
            GPIO.output(in_b, GPIO.LOW)
        else:
            GPIO.output(in_a, GPIO.LOW)
            GPIO.output(in_b, GPIO.HIGH)
        pwm_ctrl.ChangeDutyCycle(abs(speed))

    drive(IN1, IN2, left_pwm,  left_speed)
    drive(IN3, IN4, right_pwm, right_speed)


# --- 主循环 ---
import numpy as np
LOWER_RED = np.array([0,   100, 100])
UPPER_RED = np.array([10,  255, 255])
IMAGE_W   = 640

cam = CameraThread(src=0)

try:
    while True:
        frame = cam.read()
        if frame is None:
            continue

        _, center = detect_color(frame, LOWER_RED, UPPER_RED)

        if center is None:
            set_motors(0, 0)    # 未检测到目标，停车
            continue

        cx, _ = center
        error = cx - IMAGE_W // 2   # 正：目标在右，负：目标在左

        # 简单比例控制（可替换为 PID）
        Kp    = 0.3
        base  = 60
        turn  = Kp * error
        left  = base + turn
        right = base - turn

        set_motors(
            max(-100, min(100, left)),
            max(-100, min(100, right))
        )

except KeyboardInterrupt:
    pass
finally:
    set_motors(0, 0)
    cam.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()
```

---

## 信号发生器参考方案

使用 **AD9833** DDS 芯片配合树莓派 SPI 接口，生成 1Hz ~ 1MHz 的正弦波、方波、三角波。

| 特性 | 参数 |
|------|------|
| 频率精度 | 0.1Hz 分辨率 |
| 输出波形 | 正弦 / 方波 / 三角波 |
| 输出幅度 | 0.6Vpp（可接外部放大） |
| 接口 | SPI（SCLK / FSYNC / SDATA） |

> 详细 SPI 驱动代码见厂商 datasheet 参考例程
