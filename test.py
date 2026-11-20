# from ultralytics import YOLO
# import cv2
# import os

# # =============================
# # PATHS (EDIT ONLY THESE)
# # =============================

# MODEL_PATH = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/runs/segment/sanitation_seg/weights/best.pt"
# SOURCE = "test_images"
# SAVE_DIR = "results"

# # =============================

# os.makedirs(SAVE_DIR, exist_ok=True)

# model = YOLO(MODEL_PATH)

# # defect classes based on your data.yaml
# defect_classes = [
#     "commode_blokage",
#     "commode_stain",
#     "commode_floor_stain",
#     "commode_wall_stain",
#     "washbasin_stain",
#     "washbasin_wall_stain",
#     "washbasin_floor_stain",
#     "dustbin_overflow",
#     "dustbin_outside_stain",
#     "aisle_litter_small",
#     "aisle_stain"
# ]

# for img_name in os.listdir(SOURCE):

#     img_path = os.path.join(SOURCE, img_name)

#     results = model(img_path)

#     result = results[0]

#     annotated = result.plot()

#     defect_count = 0
#     detected_classes = []

#     if result.boxes is not None:

#         for box in result.boxes:

#             cls_id = int(box.cls[0])
#             conf = float(box.conf[0])
#             cls_name = model.names[cls_id]

#             if cls_name in defect_classes and conf > 0.4:
#                 defect_count += 1
#                 detected_classes.append(cls_name)

#     # =============================
#     # RULE BASED CLEANLINESS LOGIC
#     # =============================

#     if "dustbin_overflow" in detected_classes or "commode_blokage" in detected_classes:
#         status = "BAD"

#     elif defect_count >= 3:
#         status = "BAD"

#     elif defect_count > 0:
#         status = "AVERAGE"

#     else:
#         status = "GOOD"

#     print(img_name, "→", status)

#     cv2.putText(
#         annotated,
#         f"Status: {status}",
#         (20,50),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         1,
#         (0,0,255),
#         3
#     )

#     save_path = os.path.join(SAVE_DIR, img_name)

#     cv2.imwrite(save_path, annotated)

# print("Processing complete!")

# from ultralytics import YOLO
# import cv2
# import os

# # =============================
# # PATHS (EDIT ONLY THESE)
# # =============================

# MODEL_PATH = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/runs/segment/sanitation_seg/weights/best.pt"
# SOURCE = "test_images"
# SAVE_DIR = "results"

# # =============================

# os.makedirs(SAVE_DIR, exist_ok=True)

# model = YOLO(MODEL_PATH)

# # defect classes based on your data.yaml
# defect_classes = [
#     "commode_blokage",
#     "commode_stain",
#     "commode_floor_stain",
#     "commode_wall_stain",
#     "washbasin_stain",
#     "washbasin_wall_stain",
#     "washbasin_floor_stain",
#     "dustbin_overflow",
#     "dustbin_outside_stain",
#     "aisle_litter_small",
#     "aisle_stain"
# ]

# image_ext = [".jpg",".jpeg",".png"]
# video_ext = [".mp4",".avi",".mov",".mkv"]

# for file_name in os.listdir(SOURCE):

#     file_path = os.path.join(SOURCE,file_name)
#     ext = os.path.splitext(file_name)[1].lower()

#     # =============================
#     # IMAGE PROCESSING
#     # =============================

#     if ext in image_ext:

#         results = model(file_path)
#         result = results[0]

#         annotated = result.plot()

#         defect_count = 0
#         detected_classes = []

#         if result.boxes is not None:

#             for box in result.boxes:

#                 cls_id = int(box.cls[0])
#                 conf = float(box.conf[0])
#                 cls_name = model.names[cls_id]

#                 if cls_name in defect_classes and conf > 0.4:
#                     defect_count += 1
#                     detected_classes.append(cls_name)

#         if "dustbin_overflow" in detected_classes or "commode_blokage" in detected_classes:
#             status = "BAD"
#         elif defect_count >= 3:
#             status = "BAD"
#         elif defect_count > 0:
#             status = "AVERAGE"
#         else:
#             status = "GOOD"

#         cv2.putText(annotated,f"Status: {status}",(20,50),
#                     cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

#         save_path = os.path.join(SAVE_DIR,file_name)
#         cv2.imwrite(save_path,annotated)

#         print(file_name,"→",status)

#     # =============================
#     # VIDEO PROCESSING
#     # =============================

#     elif ext in video_ext:

#         cap = cv2.VideoCapture(file_path)

#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fps = int(cap.get(cv2.CAP_PROP_FPS))

#         output_video = os.path.join(SAVE_DIR,file_name)

#         writer = cv2.VideoWriter(
#             output_video,
#             cv2.VideoWriter_fourcc(*'mp4v'),
#             fps,
#             (width,height)
#         )

#         while True:

#             ret, frame = cap.read()
#             if not ret:
#                 break

#             results = model(frame)
#             result = results[0]

#             annotated = result.plot()

#             defect_count = 0
#             detected_classes = []

#             if result.boxes is not None:

#                 for box in result.boxes:

#                     cls_id = int(box.cls[0])
#                     conf = float(box.conf[0])
#                     cls_name = model.names[cls_id]

#                     if cls_name in defect_classes and conf > 0.4:
#                         defect_count += 1
#                         detected_classes.append(cls_name)

#             if "dustbin_overflow" in detected_classes or "commode_blokage" in detected_classes:
#                 status = "BAD"
#             elif defect_count >= 3:
#                 status = "BAD"
#             elif defect_count > 0:
#                 status = "AVERAGE"
#             else:
#                 status = "GOOD"

#             cv2.putText(annotated,f"Status: {status}",(20,50),
#                         cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

#             writer.write(annotated)

#         cap.release()
#         writer.release()

#         print(file_name,"→ video processed")

# print("Processing complete!")


import os
import shutil

# =========================
# PATHS (EDIT THESE)
# =========================

BASE_PATH = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/yolo_dataset1"
ALL_LABELS = os.path.join(BASE_PATH, "labels/all")

TRAIN_IMAGES = os.path.join(BASE_PATH, "images/train")
VAL_IMAGES = os.path.join(BASE_PATH, "images/val")

TRAIN_LABELS = os.path.join(BASE_PATH, "labels/train")
VAL_LABELS = os.path.join(BASE_PATH, "labels/val")

# =========================

os.makedirs(TRAIN_LABELS, exist_ok=True)
os.makedirs(VAL_LABELS, exist_ok=True)

# -------- TRAIN --------
for img in os.listdir(TRAIN_IMAGES):
    name = os.path.splitext(img)[0]
    txt_file = name + ".txt"

    src = os.path.join(ALL_LABELS, txt_file)
    dst = os.path.join(TRAIN_LABELS, txt_file)

    if os.path.exists(src):
        shutil.copy(src, dst)

# -------- VAL --------
for img in os.listdir(VAL_IMAGES):
    name = os.path.splitext(img)[0]
    txt_file = name + ".txt"

    src = os.path.join(ALL_LABELS, txt_file)
    dst = os.path.join(VAL_LABELS, txt_file)

    if os.path.exists(src):
        shutil.copy(src, dst)

print("✅ Labels copied successfully!")