# from ultralytics import YOLO

# model = YOLO("yolov8n-cls.pt")

# model.train(
#     data="cleanliness_dataset_crops",
#     epochs=60,
#     imgsz=224
# )

from ultralytics import YOLO
model = YOLO("yolov8n-cls.pt")

model.train(
    data="C:/Users/Ayushi/Desktop/sanitation_yolo_project/cleanliness_dataset_crops1",
    epochs=80,
    imgsz=224,
    batch=16,
    optimizer="AdamW",

    lr0=0.0008,
    lrf=0.01,
    weight_decay=0.0005,

    hsv_h=0.015,
    hsv_s=0.5,
    hsv_v=0.3,
    fliplr=0.5,
    translate=0.05,
    scale=0.2,

    patience=15,
    workers=2,
    cache=True
)