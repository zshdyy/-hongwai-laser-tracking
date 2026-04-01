# 系统配置与环境搭建 | Setup Guide

## 第一步：烧录系统镜像

1. 下载 [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. 选择 **Raspberry Pi OS (64-bit)** 镜像
3. 在高级设置中配置：
   - 主机名（如 `raspberrypi.local`）
   - Wi-Fi SSID 和密码
   - 启用 SSH，设置用户名/密码
4. 烧录到 SD 卡，插入树莓派上电

---

## 第二步：首次连接

```bash
# 通过 SSH 连接（确保与树莓派在同一局域网）
ssh pi@raspberrypi.local
# 或使用 IP 地址
ssh pi@192.168.x.x
```

---

## 第三步：系统更新

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

---

## 第四步：安装 Python 依赖

```bash
# 安装 pip
sudo apt install python3-pip -y

# 安装 OpenCV（headless 版本，适合无图形界面环境）
pip3 install opencv-python-headless numpy

# 安装 GPIO 库
pip3 install RPi.GPIO pigpio

# 安装其他常用库
pip3 install pyserial Pillow
```

验证 OpenCV：

```python
python3 -c "import cv2; print('OpenCV', cv2.__version__)"
```

---

## 第五步：启用摄像头

```bash
sudo raspi-config
# 进入 Interface Options → Camera → Enable
# 重启后生效
sudo reboot
```

---

## 第六步：配置无密码 SSH（可选，方便开发）

```bash
# 在本机生成密钥对（若已有可跳过）
ssh-keygen -t ed25519

# 将公钥复制到树莓派
ssh-copy-id pi@raspberrypi.local
```

---

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| SSH 连接超时 | 确认 Wi-Fi 配置正确，尝试用 IP 而非域名 |
| OpenCV 安装慢 | 换国内镜像源：`pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python-headless` |
| 摄像头不识别 | 运行 `vcgencmd get_camera` 检查；确认排线方向正确 |
| 程序运行卡顿 | 降低分辨率（480p）或启用 GPU 加速 |
