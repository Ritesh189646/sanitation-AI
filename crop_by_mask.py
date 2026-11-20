# from ultralytics import YOLO
# import cv2
# import os
# import numpy as np

# # =============================
# # PATHS (EDIT ONLY THESE)
# # =============================

# DETECTION_MODEL = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/runs/segment/sanitation_seg/weights/object_model.pt"

# INPUT_DATASET = "cleanliness_dataset"         # original dataset
# OUTPUT_DATASET = "cleanliness_dataset_crops"  # new dataset

# # =============================

# model = YOLO(DETECTION_MODEL)

# splits = ["train", "val"]
# labels = ["good", "average", "bad"]

# for split in splits:
#     for label in labels:

#         input_folder = os.path.join(INPUT_DATASET, split, label)
#         output_folder = os.path.join(OUTPUT_DATASET, split, label)

#         os.makedirs(output_folder, exist_ok=True)

#         print(f"\nProcessing: {split}/{label}")

#         for img_name in os.listdir(input_folder):

#             img_path = os.path.join(input_folder, img_name)
#             image = cv2.imread(img_path)

#             if image is None:
#                 continue

#             results = model(image)
#             result = results[0]

#             # Skip if no masks
#             if result.masks is None:
#                 continue

#             masks = result.masks.data

#             for i, mask in enumerate(masks):

#                 # Get class name
#                 cls_id = int(result.boxes.cls[i])
#                 cls_name = model.names[cls_id]

#                 # Convert mask to numpy
#                 mask_np = mask.cpu().numpy()

#                 # Resize mask to match image
#                 mask_np = cv2.resize(mask_np, (image.shape[1], image.shape[0]))
#                 mask_np = (mask_np > 0.5).astype("uint8") * 255

#                 # Apply mask
#                 masked = cv2.bitwise_and(image, image, mask=mask_np)

#                 # Get bounding box from mask
#                 ys, xs = np.where(mask_np > 0)

#                 if len(xs) == 0 or len(ys) == 0:
#                     continue

#                 x1, x2 = xs.min(), xs.max()
#                 y1, y2 = ys.min(), ys.max()

#                 crop = masked[y1:y2, x1:x2]

#                 if crop.size == 0:
#                     continue

#                 # Resize for classification model
#                 crop = cv2.resize(crop, (224, 224))

#                 # Create unique filename
#                 base_name = os.path.splitext(img_name)[0]
#                 save_name = f"{base_name}_{i}.jpg"

#                 save_path = os.path.join(output_folder, save_name)

#                 cv2.imwrite(save_path, crop)

# print("\n✅ Crop dataset created successfully!")



import os
import cv2
import numpy as np
from ultralytics import YOLO

# ======================================
# CONFIG
# ======================================
MODEL_PATH = r"runs/segment/sanitation_train/weights/best.pt"

TRAIN_SOURCE = r"yolo_dataset3/images/train"
VAL_SOURCE = r"yolo_dataset3/images/val"

SAVE_BASE = r"cleanliness_dataset_crops1"

TRAIN_SAVE = os.path.join(SAVE_BASE, "train")
VAL_SAVE = os.path.join(SAVE_BASE, "val")

CONF = 0.25

# ======================================
# LOAD MODEL
# ======================================
model = YOLO(MODEL_PATH)

os.makedirs(TRAIN_SAVE, exist_ok=True)
os.makedirs(VAL_SAVE, exist_ok=True)


# ======================================
# FUNCTION TO CROP OBJECTS
# ======================================
def crop_from_folder(source_folder, save_folder):
    results = model.predict(
        source=source_folder,
        conf=CONF,
        save=False
    )

    total_saved = 0

    for result in results:
        image = result.orig_img.copy()
        img_name = os.path.splitext(os.path.basename(result.path))[0]

        if result.masks is None:
            continue

        masks = result.masks.data.cpu().numpy()

        for i, mask in enumerate(masks):
            # resize mask to original image size
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

            binary_mask = (mask > 0.5).astype(np.uint8) * 255

            # apply segmentation mask
            masked = cv2.bitwise_and(image, image, mask=binary_mask)

            # bounding box around segmented mask
            x, y, w, h = cv2.boundingRect(binary_mask)

            # crop object
            crop = masked[y:y+h, x:x+w]

            # skip tiny false crops
            if crop.shape[0] < 20 or crop.shape[1] < 20:
                continue

            save_path = os.path.join(save_folder, f"{img_name}_obj{i}.png")
            cv2.imwrite(save_path, crop)

            total_saved += 1

    print(f"✅ Saved {total_saved} crops in {save_folder}")


# ======================================
# RUN FOR TRAIN AND VAL
# ======================================
crop_from_folder(TRAIN_SOURCE, TRAIN_SAVE)
crop_from_folder(VAL_SOURCE, VAL_SAVE)

print("🎉 Cleanliness crop dataset created successfully!")