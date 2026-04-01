# 目标追踪 | Target Tracking

## 追踪算法对比

| 算法 | 速度 | 精度 | 适用场景 |
|------|------|------|---------|
| CSRT | 慢 | 高 | 精度要求高，目标变形 |
| KCF | 快 | 中 | 实时追踪，目标匀速运动 |
| MOSSE | 极快 | 低 | 资源受限嵌入式场景 |
| MIL | 中 | 中 | 目标有遮挡 |

> 树莓派上推荐使用 **MOSSE** 或 **KCF** 以保证帧率

---

## 示例代码

```python
import cv2


def init_tracker(frame, bbox, tracker_type='KCF'):
    """
    初始化追踪器。
    bbox: (x, y, w, h) 初始目标框
    tracker_type: 'KCF', 'CSRT', 'MOSSE' 等
    """
    trackers = {
        'KCF': cv2.TrackerKCF_create,
        'CSRT': cv2.TrackerCSRT_create,
        'MOSSE': cv2.legacy.TrackerMOSSE_create,
    }
    tracker = trackers.get(tracker_type, cv2.TrackerKCF_create)()
    tracker.init(frame, bbox)
    return tracker


def run_tracking(tracker_type='KCF'):
    cap = cv2.VideoCapture(0)
    tracker = None
    bbox = None

    print("按空格键选择目标区域，按 'q' 退出，按 'r' 重新选择")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if tracker is not None:
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (0, 255, 0), 2)
                cv2.putText(frame, 'Tracking', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Lost', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Target Tracking', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord(' ') or key == ord('r'):
            # 手动框选目标
            bbox = cv2.selectROI('Target Tracking', frame, False)
            if bbox[2] > 0 and bbox[3] > 0:
                tracker = init_tracker(frame, bbox, tracker_type)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run_tracking('KCF')
```

---

## 与颜色识别联合使用

1. 第一帧用颜色识别定位目标，获取 bounding box
2. 后续帧用追踪器持续跟踪，避免每帧重新检测（节省算力）
3. 每隔 N 帧重新用颜色识别校正追踪框，防止漂移
