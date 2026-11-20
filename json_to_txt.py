import os
import json

# ==========================================
# CONFIG
# ==========================================
JSON_FOLDER = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/new_json"
SAVE_DIR = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/average_txt"

os.makedirs(SAVE_DIR, exist_ok=True)

# ==========================================
# CLASS MAP
# ==========================================
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

# ==========================================
# CONVERTER
# ==========================================
def convert_json_to_txt(json_folder, save_dir):
    json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]

    print(f"\n📂 Processing folder: {json_folder}")
    print(f"📄 JSON files found: {len(json_files)}")

    converted = 0
    skipped = 0

    for file_name in json_files:
        json_path = os.path.join(json_folder, file_name)

        try:
            # ✅ skip empty file
            if os.path.getsize(json_path) == 0:
                print(f"❌ Empty JSON: {file_name}")
                skipped += 1
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            img_w = data.get("imageWidth")
            img_h = data.get("imageHeight")

            if not img_w or not img_h:
                print(f"⚠ Missing image size: {file_name}")
                skipped += 1
                continue

            lines = []

            for shape in data.get("shapes", []):
                label = shape.get("label")
                points = shape.get("points", [])

                if label not in CLASS_MAP:
                    continue

                if len(points) < 3:
                    continue

                class_id = CLASS_MAP[label]

                polygon = []
                for x, y in points:
                    polygon.append(f"{x / img_w:.6f}")
                    polygon.append(f"{y / img_h:.6f}")

                line = f"{class_id} " + " ".join(polygon)
                lines.append(line)

            if not lines:
                print(f"⚠ No valid labels: {file_name}")
                skipped += 1
                continue

            txt_name = os.path.splitext(file_name)[0] + ".txt"
            txt_path = os.path.join(save_dir, txt_name)

            with open(txt_path, "w") as f:
                f.write("\n".join(lines))

            converted += 1
            print(f"✅ Converted: {file_name}")

        except json.JSONDecodeError:
            print(f"❌ Invalid JSON: {file_name}")
            skipped += 1

        except Exception as e:
            print(f"❌ Error in {file_name}: {e}")
            skipped += 1

    print("\n🎉 Conversion completed!")
    print(f"✅ Converted: {converted}")
    print(f"⚠ Skipped: {skipped}")


# ==========================================
# RUN
# ==========================================
convert_json_to_txt(JSON_FOLDER, SAVE_DIR)