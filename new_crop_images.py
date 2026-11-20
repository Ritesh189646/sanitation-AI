import os
import cv2
import numpy as np
from collections import defaultdict

# ==================================================
# PATHS
# ==================================================

IMAGE_DIR = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\images"

LABEL_DIR = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\txt_files"

SAVE_DIR = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\cropped_objects"

os.makedirs(SAVE_DIR, exist_ok=True)

# ==================================================
# CLASS NAMES
# ==================================================

CLASS_NAMES = {
    0: "commode_cover",
    1: "commode_seat",
    2: "commode_floor",
    3: "commode_wall",

    4: "washbasin",
    5: "washbasin_wall",
    6: "washbasin_floor",
    7: "washbasin_soap_holder",
    8: "washbasin_tap",

    9: "dustbin",
    10: "dustbin_wall",
    11: "dustbin_floor",

    12: "aisle"
}

# ==================================================
# COUNTER
# ==================================================

counter = defaultdict(int)

# ==================================================
# PROCESS
# ==================================================

for txt_file in os.listdir(LABEL_DIR):

    if not txt_file.endswith(".txt"):
        continue

    base_name = os.path.splitext(txt_file)[0]

    image_path = None

    for ext in [".jpg", ".jpeg", ".png"]:

        temp = os.path.join(
            IMAGE_DIR,
            base_name + ext
        )

        if os.path.exists(temp):
            image_path = temp
            break

    if image_path is None:
        print(f"Image not found for {base_name}")
        continue

    image = cv2.imread(image_path)

    if image is None:
        continue

    h, w = image.shape[:2]

    txt_path = os.path.join(LABEL_DIR, txt_file)

    with open(txt_path, "r") as f:
        lines = f.readlines()

    for line in lines:

        data = line.strip().split()

        if len(data) < 7:
            continue

        cls_id = int(float(data[0]))

        cls_name = CLASS_NAMES.get(cls_id, f"class_{cls_id}")

        coords = list(map(float, data[1:]))

        points = []

        for i in range(0, len(coords), 2):

            x = int(coords[i] * w)
            y = int(coords[i + 1] * h)

            points.append([x, y])

        points = np.array(points, dtype=np.int32)

        # Bounding rectangle around polygon
        x, y, bw, bh = cv2.boundingRect(points)

        crop = image[y:y+bh, x:x+bw]

        if crop.size == 0:
            continue

        counter[cls_name] += 1

        save_name = (
            f"{cls_name}_{counter[cls_name]}.jpg"
        )

        save_path = os.path.join(
            SAVE_DIR,
            save_name
        )

        cv2.imwrite(save_path, crop)

print("\nDONE")
print(f"Saved in: {SAVE_DIR}")