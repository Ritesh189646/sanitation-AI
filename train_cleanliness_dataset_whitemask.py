from ultralytics import YOLO

model = YOLO("yolov8m-cls.pt")

model.train(
    data=r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/cleanliness_dataset_crops3",
    epochs=30,
    imgsz=320,
    batch=16,
    optimizer="AdamW",

    lr0=0.0003,
    lrf=0.01,
    weight_decay=0.001,
    dropout=0.4, 

    hsv_h=0.03,
    hsv_s=0.7,
    hsv_v=0.5,
    fliplr=0.5,
    translate=0.1,
    scale=0.3,

    patience=5,
    cache=True
)