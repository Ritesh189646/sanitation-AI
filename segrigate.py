from ultralytics import YOLO
import os
import shutil
import cv2
from tqdm import tqdm

# =============================
# PATHS
# =============================
DETECTION_MODEL = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/weights/segment.pt"

SOURCE_DIR = r"D:/railmadad_photos"

SAVE_DIR = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/FINAL_FILTERED"

os.makedirs(SAVE_DIR, exist_ok=True)

# =============================
# SETTINGS
# =============================

START_AFTER = 2025121100265
TARGET_IMAGES = 500

# detection confidence
DETECTION_CONF = 0.50

# =============================
# LOAD MODEL
# =============================

detector = YOLO(DETECTION_MODEL)

# =============================
# ONLY COMMODE CLASSES
# =============================

VALID_CLASSES = [
    "commode_cover",
    "commode_seat",
    "commode_floor",
    "commode_wall"
]

# =============================
# FILTER IMAGES AFTER NUMBER
# =============================

all_images = []

for file in os.listdir(SOURCE_DIR):

    if not file.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    try:
        num = int(os.path.splitext(file)[0])

        if num > START_AFTER:
            all_images.append(file)

    except:
        continue

# serial-wise sorting
all_images = sorted(
    all_images,
    key=lambda x: int(os.path.splitext(x)[0])
)

print(f"\n📂 Images found after {START_AFTER}: {len(all_images)}")

# =============================
# PROCESS
# =============================

saved = 0
skipped = 0

for img_name in tqdm(all_images):

    # stop after target images
    if saved >= TARGET_IMAGES:
        break

    img_path = os.path.join(SOURCE_DIR, img_name)

    image = cv2.imread(img_path)

    if image is None:
        skipped += 1
        continue

    # =============================
    # DETECTION
    # =============================

    results = detector(image, conf=DETECTION_CONF)

    if len(results) == 0:
        skipped += 1
        continue

    result = results[0]

    if result.boxes is None or len(result.boxes) == 0:
        skipped += 1
        continue

    found_commode = False

    # =============================
    # CHECK DETECTED CLASSES
    # =============================

    for i, cls_id in enumerate(result.boxes.cls):

        cls_name = detector.names[int(cls_id)]

        conf = float(result.boxes.conf[i])

        # =============================
        # ONLY COMMODE OBJECTS
        # =============================

        if cls_name not in VALID_CLASSES:
            continue

        # confidence check
        if conf < 0.50:
            continue

        # =============================
        # OPTIONAL SIZE FILTER
        # =============================

        x1, y1, x2, y2 = map(int, result.boxes.xyxy[i])

        box_w = x2 - x1
        box_h = y2 - y1

        area = box_w * box_h

        img_h, img_w = image.shape[:2]
        img_area = img_h * img_w

        # reject too small objects
        if area < img_area * 0.01:
            continue

        # reject too huge objects
        if area > img_area * 0.80:
            continue

        found_commode = True
        break

    # =============================
    # SAVE IMAGE
    # =============================

    if found_commode:

        save_path = os.path.join(
            SAVE_DIR,
            img_name
        )

        shutil.copy(img_path, save_path)

        saved += 1

    else:
        skipped += 1

# =============================
# FINAL RESULT
# =============================

print("\n🎉 DONE")
print(f"✅ Saved Images   : {saved}")
print(f"❌ Skipped Images : {skipped}")
print(f"📁 Output Folder  : {SAVE_DIR}")