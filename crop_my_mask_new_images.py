import os
import cv2
from ultralytics import YOLO

# ======================================
# PATHS
# ======================================

MODEL_PATH = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/weights/segment.pt"

IMG_DIR = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/FINAL_FILTERED"

SAVE_DIR = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/crop_images3"

os.makedirs(SAVE_DIR, exist_ok=True)

# ======================================
# SETTINGS
# ======================================

PADDING = 20
CONFIDENCE = 0.5

# ======================================
# LOAD MODEL
# ======================================

model = YOLO(MODEL_PATH)

# ======================================
# VALID CLASSES
# ======================================

VALID_CLASSES = [
    "commode_cover",
    "commode_seat",
    "commode_floor",
    "commode_wall",

    "washbasin",
    "washbasin_wall",
    "washbasin_floor",
    "washbasin_soap_holder",
    "washbasin_tap",

    "dustbin",
    "dustbin_wall",
    "dustbin_floor",

    "aisle"
]

# ======================================
# MAIN FUNCTION
# ======================================

def crop_objects():

    image_files = [
        f for f in os.listdir(IMG_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    saved = 0
    skipped = 0

    print(f"\n📂 Images found: {len(image_files)}")

    for img_name in image_files:

        img_path = os.path.join(IMG_DIR, img_name)

        image = cv2.imread(img_path)

        if image is None:
            skipped += 1
            continue

        h, w = image.shape[:2]

        # ======================================
        # DETECTION
        # ======================================

        results = model(image, conf=CONFIDENCE)

        if len(results) == 0:
            skipped += 1
            continue

        result = results[0]

        if result.boxes is None:
            skipped += 1
            continue

        # ======================================
        # LOOP THROUGH DETECTIONS
        # ======================================

        for i, box in enumerate(result.boxes):

            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]

            if cls_name not in VALID_CLASSES:
                continue

            conf = float(box.conf[0])

            if conf < CONFIDENCE:
                continue

            # ======================================
            # BOUNDING BOX
            # ======================================

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # add padding
            x1 = max(0, x1 - PADDING)
            y1 = max(0, y1 - PADDING)

            x2 = min(w, x2 + PADDING)
            y2 = min(h, y2 + PADDING)

            # ======================================
            # CROP
            # ======================================

            crop = image[y1:y2, x1:x2]

            if crop.size == 0:
                continue

            # ======================================
            # DRAW BOUNDING BOX
            # ======================================

            draw_img = image.copy()

            color = (0, 255, 0)

            cv2.rectangle(
                draw_img,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

            label = f"{cls_name} {conf:.2f}"

            cv2.putText(
                draw_img,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            # ======================================
            # SAVE CROPPED IMAGE
            # ======================================

            base_name = os.path.splitext(img_name)[0]

            crop_name = f"{base_name}_{cls_name}_{i}.jpg"

            crop_path = os.path.join(
                SAVE_DIR,
                crop_name
            )

            cv2.imwrite(crop_path, crop)

            # ======================================
            # SAVE BOUNDING BOX IMAGE
            # ======================================

            bbox_name = f"{base_name}_bbox.jpg"

            bbox_path = os.path.join(
                SAVE_DIR,
                bbox_name
            )

            cv2.imwrite(bbox_path, draw_img)

            saved += 1

    print("\n🎉 DONE")
    print(f"✅ Saved Crops : {saved}")
    print(f"❌ Skipped     : {skipped}")
    print(f"📁 Output      : {SAVE_DIR}")

# ======================================
# RUN
# ======================================

crop_objects()