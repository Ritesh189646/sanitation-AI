from ultralytics import YOLO
import os

# =========================================================
# PATHS
# =========================================================

# ---------------- SEGMENTATION DATASET ----------------
SEG_DATASET = r"yolo_dataset3"

SEG_MODEL_PATH = r"runs/segment/weights/segment.pt"

SEG_YAML = r"data.yaml"


# ---------------- CLASSIFICATION DATASET ----------------
CLS_DATASET = r"cleanliness_dataset_final"

CLS_MODEL_PATH = r"runs/classify/weights/classify.pt"


# =========================================================
# IMAGE COUNT FUNCTION
# =========================================================

def count_images(folder):

    if not os.path.exists(folder):
        return 0

    return len([
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])


# =========================================================
# FOLDER SIZE FUNCTION
# =========================================================

def get_folder_size(folder):

    total_size = 0

    for path, dirs, files in os.walk(folder):

        for file in files:

            fp = os.path.join(path, file)

            if os.path.exists(fp):
                total_size += os.path.getsize(fp)

    return total_size / (1024 * 1024)   # MB


# =========================================================
# FILE SIZE FUNCTION
# =========================================================

def get_file_size(file_path):

    if not os.path.exists(file_path):
        return 0

    return os.path.getsize(file_path) / (1024 * 1024)   # MB


# =========================================================
# SEGMENTATION DATASET COUNTS
# =========================================================

seg_train_images = count_images(
    os.path.join(SEG_DATASET, "images", "train")
)

seg_val_images = count_images(
    os.path.join(SEG_DATASET, "images", "val")
)

seg_train_labels = len(os.listdir(
    os.path.join(SEG_DATASET, "labels", "train")
))

seg_val_labels = len(os.listdir(
    os.path.join(SEG_DATASET, "labels", "val")
))

seg_total_images = seg_train_images + seg_val_images

seg_dataset_size = get_folder_size(SEG_DATASET)

seg_model_size = get_file_size(SEG_MODEL_PATH)


# =========================================================
# CLASSIFICATION DATASET COUNTS
# =========================================================

# ---------------- TRAIN ----------------

train_avg = count_images(
    os.path.join(CLS_DATASET, "train", "average")
)

train_bad = count_images(
    os.path.join(CLS_DATASET, "train", "bad")
)

train_good = count_images(
    os.path.join(CLS_DATASET, "train", "good")
)

# ---------------- VAL ----------------

val_avg = count_images(
    os.path.join(CLS_DATASET, "val", "average")
)

val_bad = count_images(
    os.path.join(CLS_DATASET, "val", "bad")
)

val_good = count_images(
    os.path.join(CLS_DATASET, "val", "good")
)

cls_train_total = train_avg + train_bad + train_good

cls_val_total = val_avg + val_bad + val_good

cls_total = cls_train_total + cls_val_total

cls_dataset_size = get_folder_size(CLS_DATASET)

cls_model_size = get_file_size(CLS_MODEL_PATH)


# =========================================================
# LOAD MODELS
# =========================================================

print("\nLoading Models...\n")

seg_model = YOLO(SEG_MODEL_PATH)

cls_model = YOLO(CLS_MODEL_PATH)


# =========================================================
# VALIDATE MODELS
# =========================================================

print("\nValidating Segmentation Model...\n")

seg_metrics = seg_model.val(
    data=SEG_YAML,
    verbose=False
)

print("\nValidating Classification Model...\n")

cls_metrics = cls_model.val(
    data=CLS_DATASET,
    verbose=False
)


# =========================================================
# FINAL PROFESSIONAL REPORT
# =========================================================

print("\n" + "=" * 80)
print(" SANITATION AI PROJECT REPORT ")
print("=" * 80)


# =========================================================
# MODEL 1 : OBJECT DETECTION & SEGMENTATION
# =========================================================

print("\n📌 MODEL 1 : OBJECT DETECTION & SEGMENTATION")
print("-" * 80)

print("\nModel Information")
print(f"YOLO Version                  : YOLOv8 Segmentation")
print(f"Model File                    : segment.pt")
print(f"Model Size                    : {seg_model_size:.2f} MB")

print("\nDataset Information")
print(f"Dataset Name                  : yolo_dataset3")
print(f"Dataset Size                  : {seg_dataset_size:.2f} MB")

print("\nDataset Structure")

print("""
images/
   ├── train
   └── val

labels/
   ├── train
   └── val
""")

print("Segmentation Dataset Details")

print(f"Train Images                  : {seg_train_images}")
print(f"Validation Images             : {seg_val_images}")

print(f"Train Labels                  : {seg_train_labels}")
print(f"Validation Labels             : {seg_val_labels}")

print(f"Total Segmentation Images     : {seg_total_images}")

print("\nPurpose")

print("• Detect sanitation objects")
print("• Perform object segmentation")
print("• Generate object crops")
print("• Prepare crops for cleanliness classification")

print("\nSegmentation Accuracy")

print(f"Box mAP50                     : {seg_metrics.box.map50 * 100:.2f}%")
print(f"Box mAP50-95                  : {seg_metrics.box.map * 100:.2f}%")

print(f"Mask mAP50                    : {seg_metrics.seg.map50 * 100:.2f}%")
print(f"Mask mAP50-95                 : {seg_metrics.seg.map * 100:.2f}%")


# =========================================================
# MODEL 2 : CLEANLINESS CLASSIFICATION
# =========================================================

print("\n" + "=" * 80)
print("📌 MODEL 2 : CLEANLINESS CLASSIFICATION")
print("=" * 80)

print("\nModel Information")

print(f"YOLO Version                  : YOLOv8 Classification")
print(f"Model File                    : classify.pt")
print(f"Model Size                    : {cls_model_size:.2f} MB")

print("\nDataset Information")

print(f"Dataset Name                  : cleanliness_dataset_final")
print(f"Dataset Size                  : {cls_dataset_size:.2f} MB")

print("\nDataset Structure")

print("""
train/
   ├── average
   ├── bad
   └── good

val/
   ├── average
   ├── bad
   └── good
""")

print("Training Dataset")

print(f"average                       : {train_avg}")
print(f"bad                           : {train_bad}")
print(f"good                          : {train_good}")

print(f"Total Train Images            : {cls_train_total}")

print("\nValidation Dataset")

print(f"average                       : {val_avg}")
print(f"bad                           : {val_bad}")
print(f"good                          : {val_good}")

print(f"Total Validation Images       : {cls_val_total}")

print(f"\nOverall Classification Images : {cls_total}")

print("\nPurpose")

print("• Predict cleanliness level")
print("• Categorize sanitation crops")
print("• Detect cleanliness status")

print("\nClasses")

print("""
• good
• average
• bad
""")

print("Classification Accuracy")

print(f"Top-1 Accuracy                : {cls_metrics.top1 * 100:.2f}%")
print(f"Top-5 Accuracy                : {cls_metrics.top5 * 100:.2f}%")


# =========================================================
# FINAL PIPELINE
# =========================================================

print("\n" + "=" * 80)
print("📌 FINAL PIPELINE")
print("=" * 80)

print("""

STEP 1
YOLOv8 Segmentation model detects sanitation objects.

STEP 2
Detected objects are segmented and cropped.

STEP 3
YOLOv8 Classification model predicts:
    • good
    • average
    • bad

STEP 4
Final cleanliness status is generated automatically.

STEP 5
Filtered results can be used for:
    • Live monitoring
    • Video analysis
    • Maintenance alerts
    • Smart sanitation systems

""")


# =========================================================
# FINAL RESULT
# =========================================================

print("=" * 80)
print(" FINAL RESULT ")
print("=" * 80)

print(f"""

✅ Segmentation Dataset Images      : {seg_total_images}

✅ Classification Dataset Images    : {cls_total}

✅ Segmentation Dataset Size        : {seg_dataset_size:.2f} MB

✅ Classification Dataset Size      : {cls_dataset_size:.2f} MB

✅ Segmentation Model Size          : {seg_model_size:.2f} MB

✅ Classification Model Size        : {cls_model_size:.2f} MB

✅ Segmentation Accuracy (mAP50)    : {seg_metrics.seg.map50 * 100:.2f}%

✅ Classification Accuracy          : {cls_metrics.top1 * 100:.2f}%

✅ Project Status                   : Successfully Trained & Ready for Deployment

""")