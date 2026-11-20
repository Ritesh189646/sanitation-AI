import os
import json

# =====================================================
# PATHS
# =====================================================

JSON_FOLDER = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\json_files"

OUTPUT_FOLDER = r"C:\Users\Ayushi\Desktop\sanitation_yolo_project\txt_files"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================================
# CLASS IDS
# =====================================================

CLASS_MAP = {
    "commode_cover": 0,
    "commode_seat": 1,
    "commode_floor": 2,
    "commode_wall": 3,

    "washbasin": 4,
    "washbasin_wall": 5,
    "washbasin_floor": 6,
    "washbasin_soap_holder": 7,
    "washbasin_tap": 8,

    "dustbin": 9,
    "dustbin_wall": 10,
    "dustbin_floor": 11,

    "aisle": 12
}

# =====================================================
# CONVERT
# =====================================================

json_files = [
    f for f in os.listdir(JSON_FOLDER)
    if f.endswith(".json")
]

print(f"\nFound {len(json_files)} JSON files")

converted = 0

for json_file in json_files:

    json_path = os.path.join(JSON_FOLDER, json_file)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    img_w = data["imageWidth"]
    img_h = data["imageHeight"]

    txt_lines = []

    for shape in data["shapes"]:

        label = shape["label"]

        if label not in CLASS_MAP:
            print(f"Skipping unknown class: {label}")
            continue

        cls_id = CLASS_MAP[label]

        points = shape["points"]

        yolo_line = [str(cls_id)]

        for x, y in points:

            x_norm = x / img_w
            y_norm = y / img_h

            yolo_line.append(f"{x_norm:.6f}")
            yolo_line.append(f"{y_norm:.6f}")

        txt_lines.append(" ".join(yolo_line))

    txt_name = os.path.splitext(json_file)[0] + ".txt"

    txt_path = os.path.join(
        OUTPUT_FOLDER,
        txt_name
    )

    with open(txt_path, "w") as f:
        f.write("\n".join(txt_lines))

    converted += 1

print("\n=================================")
print(f"Converted : {converted}")
print(f"Saved To  : {OUTPUT_FOLDER}")
print("=================================")