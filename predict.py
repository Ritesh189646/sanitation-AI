import os
import shutil

# ======================================
# PATHS
# ======================================

RAW_IMAGES = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\raw_images"

TXT_FOLDER = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\yolo_dataset3\labels\all"

SAVE_FOLDER = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\new"

os.makedirs(SAVE_FOLDER, exist_ok=True)

# ======================================
# GET TXT NAMES
# ======================================

txt_names = set()

for file in os.listdir(TXT_FOLDER):

    if file.endswith(".txt"):

        txt_names.add(
            os.path.splitext(file)[0]
        )

print(f"TXT Files Found : {len(txt_names)}")

# ======================================
# COPY MATCHING IMAGES
# ======================================

copied = 0
missing = 0

for name in txt_names:

    found = False

    for ext in [".jpg", ".jpeg", ".png"]:

        img_path = os.path.join(
            RAW_IMAGES,
            name + ext
        )

        if os.path.exists(img_path):

            shutil.copy(
                img_path,
                os.path.join(
                    SAVE_FOLDER,
                    name + ext
                )
            )

            copied += 1
            found = True
            break

    if not found:
        missing += 1

# ======================================
# REPORT
# ======================================

print("\n" + "=" * 50)
print("DONE")
print("=" * 50)

print(f"Copied Images : {copied}")
print(f"Missing Images: {missing}")
print(f"Output Folder : {SAVE_FOLDER}")