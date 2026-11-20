import os
import shutil

# =========================
# CONFIG
# =========================
BASE_DIR = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project"

RAW_IMAGES = os.path.join(BASE_DIR, "raw_images")
LABELS_ALL = os.path.join(BASE_DIR, "yolo_dataset3", "labels", "all")

TRAIN_IMG = os.path.join(BASE_DIR, "yolo_dataset3", "images", "train")
VAL_IMG = os.path.join(BASE_DIR, "yolo_dataset3", "images", "val")

TRAIN_LBL = os.path.join(BASE_DIR, "yolo_dataset3", "labels", "train")
VAL_LBL = os.path.join(BASE_DIR, "yolo_dataset3", "labels", "val")

SPLIT_RATIO = 0.8   # 80% train, 20% val

# =========================
# CREATE FOLDERS
# =========================
for folder in [TRAIN_IMG, VAL_IMG, TRAIN_LBL, VAL_LBL]:
    os.makedirs(folder, exist_ok=True)

# =========================
# GET ONLY LABELED FILES
# =========================
label_files = sorted([
    f for f in os.listdir(LABELS_ALL)
    if f.endswith(".txt")
])

total = len(label_files)
split_index = int(total * SPLIT_RATIO)

train_files = label_files[:split_index]
val_files = label_files[split_index:]

print(f"Total labeled images: {total}")
print(f"Train: {len(train_files)}")
print(f"Val: {len(val_files)}")

# =========================
# COPY FILES
# =========================
def copy_files(file_list, img_dest, lbl_dest):
    for txt_file in file_list:
        base_name = os.path.splitext(txt_file)[0]

        # label file
        src_label = os.path.join(LABELS_ALL, txt_file)
        dst_label = os.path.join(lbl_dest, txt_file)
        shutil.copy(src_label, dst_label)

        # find matching image
        found = False
        for ext in [".jpg", ".jpeg", ".png"]:
            img_name = base_name + ext
            src_img = os.path.join(RAW_IMAGES, img_name)

            if os.path.exists(src_img):
                dst_img = os.path.join(img_dest, img_name)
                shutil.copy(src_img, dst_img)
                found = True
                break

        if not found:
            print(f"⚠ Image not found for: {txt_file}")

# copy train
copy_files(train_files, TRAIN_IMG, TRAIN_LBL)

# copy val
copy_files(val_files, VAL_IMG, VAL_LBL)

print("✅ Serial-wise dataset split completed successfully!")