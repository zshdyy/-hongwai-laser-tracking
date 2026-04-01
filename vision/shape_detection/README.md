# 形状识别 | Shape Detection

## 原理

通过以下步骤识别图像中的几何形状：

1. **灰度化 + 高斯模糊** → 降低噪声
2. **Canny 边缘检测** → 提取边缘
3. **轮廓查找** (`findContours`) → 获取封闭区域
4. **多边形拟合** (`approxPolyDP`) → 判断边数（三角形=3，矩形=4，圆=5+）

---

## 示例代码

```python
import cv2
import numpy as np


def classify_shape(contour):
    """根据轮廓边数判断形状名称。"""
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    vertices = len(approx)

    if vertices == 3:
        return "Triangle", approx
    elif vertices == 4:
        # 区分矩形与正方形
        x, y, w, h = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = "Square" if 0.95 <= ar <= 1.05 else "Rectangle"
        return shape, approx
    elif vertices == 5:
        return "Pentagon", approx
    else:
        return "Circle", approx


def detect_shapes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 1000:  # 过滤小轮廓
            continue

        shape_name, approx = classify_shape(cnt)
        M = cv2.moments(cnt)
        if M['m00'] == 0:
            continue

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
        cv2.putText(frame, shape_name, (cx - 30, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    return frame


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result = detect_shapes(frame)
        cv2.imshow('Shape Detection', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
```

---

## 注意事项

- `approxPolyDP` 的第二个参数（精度）建议取轮廓周长的 2% ~ 5%
- 对于圆形识别，也可改用 `HoughCircles` 获得更好效果
- 光照不均匀时，可改用自适应阈值（`adaptiveThreshold`）代替 Canny
