from ultralytics import YOLO

model = YOLO("C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/weights/segment.pt")

print("Task:", model.task)
print("Names:", model.names)

result = model("test_images/4588.jpeg")[0]

print(result.boxes.xyxy)
print(result.boxes.conf)
print(result.boxes.cls)