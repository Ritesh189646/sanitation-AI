from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")

model.train(
    data="data.yaml",
    epochs=60,          # reduced from 100
    imgsz=512,          # faster than 640, still accurate
    batch=8,
    optimizer="AdamW",

    lr0=0.001,
    lrf=0.01,
    weight_decay=0.0005,

    warmup_epochs=3,

    box=7.5,
    cls=0.5,
    dfl=1.5,

    # light augmentations only
    hsv_h=0.015,
    hsv_s=0.5,
    hsv_v=0.3,
    translate=0.05,
    scale=0.3,
    fliplr=0.5,

    # disable expensive ones
    mosaic=0.0,
    mixup=0.0,
    copy_paste=0.0,

    patience=15,
    workers=2,
    cache=True,

    project="runs/segment",
    name="sanitation_seg"
)
