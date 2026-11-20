import os
import cv2
import numpy as np

# ==========================================
# CONFIG
# ==========================================
DATASET_DIR = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/cleanliness_dataset_crops3"


# ==========================================
# FIX BACKGROUND TO WHITE
# ==========================================
def convert_to_white_background(folder_path):
    converted = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_path = os.path.join(root, file)

            # read with alpha support
            image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

            if image is None:
                continue

            # -------------------------
            # PNG with alpha channel
            # -------------------------
            if len(image.shape) == 3 and image.shape[2] == 4:
                b, g, r, a = cv2.split(image)

                # create white background
                white = np.ones((image.shape[0], image.shape[1], 3), dtype=np.uint8) * 255

                # alpha normalize
                alpha = a / 255.0

                # blend object with white bg
                for c, channel in enumerate([b, g, r]):
                    white[:, :, c] = (channel * alpha + 255 * (1 - alpha)).astype(np.uint8)

                output = white

            else:
                # RGB image → replace black with white
                output = image.copy()
                black_mask = np.all(output < 10, axis=2)
                output[black_mask] = [255, 255, 255]

            cv2.imwrite(img_path, output)
            converted += 1

    print(f"✅ Converted {converted} images successfully")


# ==========================================
# RUN
# ==========================================
convert_to_white_background(DATASET_DIR)

print("🎉 Background fixed to white in same folders!")