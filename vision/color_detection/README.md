# 颜色识别 | Color Detection

## 原理

在 **HSV 色彩空间**（Hue 色相、Saturation 饱和度、Value 明度）中进行颜色分割，相比 RGB 对光照变化更鲁棒。

---

## HSV 阈值参考表

| 颜色 | H 下限 | H 上限 | S 下限 | S 上限 | V 下限 | V 上限 |
|------|--------|--------|--------|--------|--------|--------|
| 红色（低） | 0 | 10 | 100 | 255 | 100 | 255 |
| 红色（高） | 160 | 180 | 100 | 255 | 100 | 255 |
| 绿色 | 40 | 80 | 50 | 255 | 50 | 255 |
| 蓝色 | 100 | 130 | 50 | 255 | 50 | 255 |
| 黄色 | 20 | 40 | 100 | 255 | 100 | 255 |

> ⚠️ 实际阈值受光照影响，建议使用调参脚本现场校准

---

## 示例代码

```python
import cv2
import numpy as np

def detect_color(frame, lower_hsv, upper_hsv):
    """
    在给定帧中检测指定颜色区域，返回掩码和目标中心坐标。
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # 形态学处理去噪
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # 找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return mask, None

    # 取面积最大的轮廓
    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 500:  # 过滤小噪声
        return mask, None

    M = cv2.moments(largest)
    if M['m00'] == 0:
        return mask, None

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return mask, (cx, cy)


# 使用示例：检测绿色目标
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mask, center = detect_color(frame, lower_green, upper_green)

        if center:
            cv2.circle(frame, center, 10, (0, 255, 0), -1)
            cv2.putText(frame, f'({center[0]}, {center[1]})',
                        (center[0] + 15, center[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Color Detection', frame)
        cv2.imshow('Mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

---

## 调参技巧

1. 在目标颜色上取样，用 `print(hsv[y, x])` 获取 HSV 值
2. 预留 ±10~20 的阈值余量
3. 在不同光照条件下多次测试，选取稳健的阈值范围
