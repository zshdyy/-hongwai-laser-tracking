# 模拟电路实验 | Analog Electronics Experiments

本模块包含南科大模拟电路课程相关的 DIY 实验，覆盖从基础运放到综合信号处理系统的完整实验链路。

---

## 实验列表

| 编号 | 实验名称 | 核心知识点 | 难度 |
|------|---------|-----------|------|
| 01 | [运算放大器基础](./01_op_amp_basics/) | 同相/反相放大、虚短虚断 | ⭐ |
| 02 | [滤波器设计](./02_filters/) | RC / LC / 有源滤波器、截止频率 | ⭐⭐ |
| 03 | [振荡电路](./03_oscillators/) | RC 振荡、LC 振荡、晶振 | ⭐⭐⭐ |
| 04 | [电源电路设计](./04_power_supply/) | 线性稳压、开关电源（Buck/Boost） | ⭐⭐⭐ |

---

## 所需仪器与器件

| 仪器 | 用途 |
|------|------|
| 示波器 | 观测波形、测量频率与幅度 |
| 信号发生器 | 提供测试激励信号 |
| 直流电源 | 为电路供电（±15V 等） |
| 万用表 | 静态工作点测量 |
| 面包板 / PCB | 电路搭建与焊接 |

常用芯片：`LM358`、`TL072`、`NE555`、`LM7805`、`LM317`

---

## 实验步骤（通用流程）

1. **理论分析**：推导电路传递函数，计算预期输出
2. **仿真验证**：使用 LTspice 或 Multisim 进行仿真
3. **实物搭建**：在面包板上按原理图连接电路
4. **测试调试**：用示波器观测输出，对比理论值
5. **总结记录**：填写实验报告，分析误差来源

---

## 快速仿真示例（LTspice）

```spice
* 反相放大器示例
V1 in 0 AC 1
R1 in inv 10k
R2 inv out 100k
XU1 0 inv out LM358
.op
.ac dec 100 1 1Meg
.backanno
.end
```

---

## 参考资料

- 《模拟电子技术基础》（第六版）—— 童诗白、华成英
- [All About Circuits – Op-Amp Tutorial](https://www.allaboutcircuits.com/textbook/semiconductors/chpt-8/)
- LTspice 官方教程：https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html
