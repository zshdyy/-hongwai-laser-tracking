# GPIO 控制与硬件接口 | GPIO Control

## Raspberry Pi 4B GPIO 引脚图

```
         3V3  (1) (2)  5V
       GPIO2  (3) (4)  5V
       GPIO3  (5) (6)  GND
       GPIO4  (7) (8)  GPIO14
         GND  (9) (10) GPIO15
      GPIO17 (11) (12) GPIO18
      GPIO27 (13) (14) GND
      GPIO22 (15) (16) GPIO23
         3V3 (17) (18) GPIO24
      GPIO10 (19) (20) GND
       GPIO9 (21) (22) GPIO25
      GPIO11 (23) (24) GPIO8
         GND (25) (26) GPIO7
       GPIO0 (27) (28) GPIO1
       GPIO5 (29) (30) GND
       GPIO6 (31) (32) GPIO12
      GPIO13 (33) (34) GND
      GPIO19 (35) (36) GPIO16
      GPIO26 (37) (38) GPIO20
         GND (39) (40) GPIO21
```

---

## LED 控制示例

```python
import RPi.GPIO as GPIO
import time

LED_PIN = 18  # BCM 编号

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

---

## PWM 控制电机 / 舵机

```python
import RPi.GPIO as GPIO

SERVO_PIN = 12  # 硬件 PWM 引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# 舵机：50Hz，占空比 2.5%~12.5% 对应 0°~180°
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(7.5)  # 初始 90°

def set_angle(angle):
    """设置舵机角度（0 ~ 180 度）。"""
    duty = 2.5 + (angle / 180.0) * 10.0
    pwm.ChangeDutyCycle(duty)

try:
    set_angle(0)
    import time; time.sleep(1)
    set_angle(90)
    time.sleep(1)
    set_angle(180)
    time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
```

---

## 串口通信（与单片机通信）

```python
import serial
import time

# 打开串口（树莓派默认串口 /dev/ttyS0，波特率 9600）
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

# 发送数据
ser.write(b'Hello MCU\n')

# 接收数据
line = ser.readline().decode('utf-8').strip()
print(f'Received: {line}')

ser.close()
```

> ⚠️ 使用串口前需在 `raspi-config` 中禁用串口控制台，仅保留串口硬件

---

## 注意事项

- GPIO 电平为 **3.3V**，直接连接 5V 设备会损坏树莓派
- 大功率设备（电机、继电器）须通过驱动电路（L298N、MOS管等）控制
- 程序结束前务必调用 `GPIO.cleanup()` 复位引脚状态
