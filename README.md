# 南科大电赛项目 · SUSTech Electronics Competition Project

> **关键词**: 模拟电路实验 · 全国大学生电子设计竞赛 · 计算机视觉 · 树莓派  
> **Keywords**: Analog Electronics · NUEDC · Computer Vision · Raspberry Pi

---

## 📖 项目简介 | Project Overview

本项目面向**南方科技大学（SUSTech）**参加**全国大学生电子设计竞赛（电赛）**的学生及对以下方向感兴趣的学习者：

- 🔌 **模拟电路 DIY 实验**：从基础运放电路到综合信号处理系统的搭建与测试
- 🏆 **电赛备赛**：历届经典题目分析、解题思路与参考实现
- 👁️ **计算机视觉**：基于 OpenCV 的图像识别与目标检测
- 🍓 **树莓派应用**：在 Raspberry Pi 上部署视觉算法，实现嵌入式智能系统

---

## 📁 项目结构 | Repository Structure

```
.
├── README.md                   # 项目总览（本文件）
│
├── analog_experiments/         # 模拟电路实验 (Analog Electronics Experiments)
│   ├── README.md               # 实验模块总览
│   ├── 01_op_amp_basics/       # 运算放大器基础
│   ├── 02_filters/             # 滤波器设计
│   ├── 03_oscillators/         # 振荡电路
│   └── 04_power_supply/        # 电源电路设计
│
├── vision/                     # 计算机视觉模块 (Computer Vision)
│   ├── README.md               # 视觉模块总览
│   ├── color_detection/        # 颜色识别
│   ├── shape_detection/        # 形状识别
│   ├── target_tracking/        # 目标追踪
│   └── utils/                  # 公共工具函数
│
├── raspberry_pi/               # 树莓派部署 (Raspberry Pi Deployment)
│   ├── README.md               # 树莓派模块总览
│   ├── setup/                  # 系统配置与环境搭建
│   ├── gpio_control/           # GPIO 控制与硬件接口
│   └── camera/                 # 摄像头驱动与采集
│
├── competition/                # 电赛题目与解析 (Competition Topics)
│   ├── README.md               # 电赛模块总览
│   ├── problem_analysis/       # 题目分析
│   └── reference_designs/      # 参考设计
│
└── docs/                       # 文档与学习资料 (Documentation)
    ├── hardware_guide.md       # 硬件选型与接线指南
    ├── software_guide.md       # 软件环境配置指南
    └── references.md           # 参考资料与延伸阅读
```

---

## 🚀 快速开始 | Quick Start

### 1. 克隆仓库

```bash
git clone https://github.com/zshdyy/-.git
cd -
```

### 2. 查阅各模块文档

每个子目录下均有独立的 `README.md`，建议按以下顺序阅读：

| 顺序 | 模块 | 说明 |
|------|------|------|
| 1 | [`docs/`](./docs/) | 整体学习路线与环境配置 |
| 2 | [`analog_experiments/`](./analog_experiments/) | 模拟电路基础实验 |
| 3 | [`raspberry_pi/`](./raspberry_pi/) | 树莓派硬件平台搭建 |
| 4 | [`vision/`](./vision/) | 计算机视觉算法 |
| 5 | [`competition/`](./competition/) | 电赛综合实战 |

---

## 🔧 技术栈 | Tech Stack

| 类别 | 工具 / 技术 |
|------|------------|
| 硬件平台 | Raspberry Pi 4B / 3B+ |
| 操作系统 | Raspberry Pi OS (Debian-based) |
| 编程语言 | Python 3 / C |
| 视觉库 | OpenCV 4.x |
| 硬件接口 | RPi.GPIO / pigpio |
| 电路仿真 | LTspice / Multisim |
| 版本管理 | Git / GitHub |

---

## 📚 学习路线 | Learning Path

```
基础准备
 ├── 复习模拟电路基础（运放、滤波器、振荡器）
 └── 了解树莓派硬件及 Linux 基础操作

环境搭建
 ├── 刷写 Raspberry Pi OS
 ├── 安装 OpenCV（见 docs/software_guide.md）
 └── 验证摄像头工作正常

视觉算法学习
 ├── 颜色空间与颜色识别（HSV 色彩模型）
 ├── 形状识别（Canny 边缘检测 + 霍夫变换）
 └── 目标追踪（KCF / CSRT 追踪器）

电赛综合实战
 ├── 读懂历届题目（见 competition/problem_analysis/）
 ├── 设计硬件方案（模拟+数字混合信号）
 └── 软硬件联调
```

---

## 📝 注意事项 | Notes

- 本项目代码与文档持续更新，欢迎提 Issue 或 PR 参与共建
- 模电实验部分建议在有示波器、信号发生器等仪器的实验室环境下进行
- 视觉模块已在 Raspberry Pi 4B + CSI 摄像头上测试通过
- 电赛相关设计仅供参考，请遵守竞赛规则独立完成作品

---

## 🤝 贡献 | Contributing

欢迎同学一起完善本项目：

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 提交 Pull Request

---

## 📄 许可证 | License

本项目采用 [MIT License](LICENSE) 开源协议。

---

*南方科技大学 · 电子系 · 制作 with ❤️ for SUSTech EE students*

