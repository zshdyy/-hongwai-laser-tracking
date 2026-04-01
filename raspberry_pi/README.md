# 树莓派模块 | Raspberry Pi

本模块涵盖 Raspberry Pi 的系统配置、硬件接口控制和摄像头使用，是视觉系统运行的硬件基础。

---

## 子模块概览

| 子模块 | 说明 |
|--------|------|
| [setup/](./setup/) | 系统镜像烧录、SSH 配置、软件环境安装 |
| [gpio_control/](./gpio_control/) | GPIO 引脚控制、PWM 输出、外设接口 |
| [camera/](./camera/) | CSI / USB 摄像头驱动与图像采集 |

---

## 推荐硬件配置

| 配件 | 型号建议 | 说明 |
|------|---------|------|
| 主板 | Raspberry Pi 4B (4GB) | 算力充足，适合视觉处理 |
| 摄像头 | Raspberry Pi Camera Module v2 | 8MP，支持 1080p@30fps |
| 存储卡 | SanDisk 32GB A1 Class10 | 高速读写，系统稳定 |
| 电源 | 5V 3A USB-C | 保证在满负载时供电稳定 |
| 散热 | 散热片 + 风扇 | 视觉处理时 CPU 发热量大 |

---

## 快速连接图

```
PC / 手机
   │
   │ SSH (局域网 / Wi-Fi)
   ▼
Raspberry Pi 4B
   ├── CSI 接口 ── Camera Module v2
   ├── GPIO 40pin ── 自定义硬件电路
   ├── USB ── 鼠标 / 键盘 / USB 摄像头
   └── HDMI ── 显示器（调试用）
```

---

## 常用命令速查

```bash
# 查看系统信息
uname -a
cat /proc/cpuinfo | grep Model

# 查看 CPU 温度
vcgencmd measure_temp

# 启用 / 禁用摄像头（raspi-config）
sudo raspi-config

# 拍一张照片测试摄像头
raspistill -o test.jpg

# 查看 GPIO 状态
gpio readall
```
