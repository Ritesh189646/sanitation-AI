import os

# =========================================================
# DATASET PATH
# =========================================================

DATASET_PATH = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\cleanliness_dataset_classwise"

# =========================================================
# COUNT FUNCTION
# =========================================================

def count_images(folder):

    if not os.path.exists(folder):
        return 0

    return len([
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

# =========================================================
# MAIN
# =========================================================

print("\n" + "=" * 80)
print(" OBJECT-WISE CLEANLINESS DATASET REPORT ")
print("=" * 80)

total_images = 0

# =========================================================
# LOOP TRAIN + VAL
# =========================================================

for split in ["train", "val"]:

    split_path = os.path.join(DATASET_PATH, split)

    if not os.path.exists(split_path):
        continue

    print(f"\n📂 {split.upper()} DATASET")
    print("-" * 80)

    split_total = 0

    object_folders = sorted(os.listdir(split_path))

    for obj_name in object_folders:

        obj_path = os.path.join(split_path, obj_name)

        if not os.path.isdir(obj_path):
            continue

        print(f"\n🔹 {obj_name}")

        obj_total = 0

        for clean_class in ["good", "average", "bad"]:

            class_path = os.path.join(
                obj_path,
                clean_class
            )

            count = count_images(class_path)

            obj_total += count

            print(f"   {clean_class:<10}: {count}")

        print(f"   TOTAL      : {obj_total}")

        split_total += obj_total

    print("\n" + "-" * 80)
    print(f"TOTAL {split.upper()} IMAGES : {split_total}")

    total_images += split_total

# =========================================================
# FINAL TOTAL
# =========================================================

print("\n" + "=" * 80)
print(f" OVERALL DATASET IMAGES : {total_images}")
print("=" * 80)