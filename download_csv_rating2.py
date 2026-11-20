# import pandas as pd
# import os
# import requests
# from tqdm import tqdm
# import time
# import random
# import cv2
# import numpy as np
# from PIL import Image
# from io import BytesIO

# # ---------------- FILE PATHS ----------------
# rating_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_rating_202602111506.csv"
# details_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_details_202602111506.csv"

# save_base = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/rating_image_2"
# os.makedirs(save_base, exist_ok=True)

# # ---------------- LOAD CSV ----------------
# rating_df = pd.read_csv(rating_csv, low_memory=False)
# details_df = pd.read_csv(details_csv, low_memory=False)

# # ---------------- CLEAN TEXT ----------------
# rating_df["rating_value"] = rating_df["rating_value"].astype(str).str.lower().str.strip()
# rating_df["rating_value_ai"] = rating_df["rating_value_ai"].astype(str).str.lower().str.strip()

# # ---------------- JOIN USING inspection_id ----------------
# merged_df = pd.merge(
#     rating_df,
#     details_df,
#     on="inspection_id",
#     how="inner"
# )

# print("Total merged rows:", len(merged_df))

# # ---------------- FILTER COMMON AGREEMENT ----------------
# bad_df = merged_df[
#     (merged_df["rating_value"] == "poor") &
#     (merged_df["rating_value_ai"] == "bad")
# ]

# avg_df = merged_df[
#     (merged_df["rating_value"] == "average") &
#     (merged_df["rating_value_ai"] == "medium")
# ]

# good_df = merged_df[
#     (merged_df["rating_value"] == "good") &
#     (merged_df["rating_value_ai"] == "good")
# ]

# print("Available BAD:", len(bad_df))
# print("Available AVERAGE:", len(avg_df))
# print("Available GOOD:", len(good_df))


# # ---------------- IMAGE QUALITY CHECK FUNCTION ----------------
# def is_image_valid(image_bytes,
#                    min_width=400,
#                    min_height=400,
#                    blur_threshold=100):

#     try:
#         image = Image.open(BytesIO(image_bytes)).convert("RGB")
#         width, height = image.size

#         # Reject small / cropped images
#         if width < min_width or height < min_height:
#             return False

#         # Convert to OpenCV
#         open_cv_image = np.array(image)
#         gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

#         # Blur detection
#         blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

#         if blur_score < blur_threshold:
#             return False

#         return True

#     except:
#         return False


# # ---------------- DOWNLOAD FUNCTION ----------------
# def download_category(df, folder_name, target_limit=500):

#     save_dir = os.path.join(save_base, folder_name)
#     os.makedirs(save_dir, exist_ok=True)

#     image_ids = df["image_id"].dropna().astype(str).unique()
#     image_ids = list(image_ids)

#     random.shuffle(image_ids)

#     session = requests.Session()
#     session.headers.update({"User-Agent": "Mozilla/5.0"})

#     count = 0
#     attempted = 0
#     rejected_quality = 0

#     for img_name in tqdm(image_ids, desc=f"Downloading {folder_name}"):

#         if count >= target_limit:
#             break

#         img_name = img_name.strip()
#         url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_name}"

#         attempted += 1

#         try:
#             r = session.get(url, timeout=25)

#             if (
#                 r.status_code == 200
#                 and "image" in r.headers.get("Content-Type", "")
#                 and len(r.content) > 5000
#             ):

#                 # 🔎 Check blur + size before saving
#                 if is_image_valid(r.content):

#                     file_path = os.path.join(save_dir, img_name)

#                     if not os.path.exists(file_path):
#                         with open(file_path, "wb") as f:
#                             f.write(r.content)

#                         count += 1
#                 else:
#                     rejected_quality += 1

#         except:
#             pass

#         time.sleep(0.05)

#     print(f"\n✅ {folder_name} successfully downloaded: {count}")
#     print(f"📦 Total attempted: {attempted}")
#     print(f"❌ Rejected (blur/small): {rejected_quality}\n")


# # ---------------- DOWNLOAD 1000 EACH ----------------
# download_category(bad_df, "bad_images", 1500)
# download_category(avg_df, "average_images", 500)
# download_category(good_df, "good_images", 200)

# print("🎉 DONE — Download process completed.")

import pandas as pd
import os
import requests
from tqdm import tqdm
import time
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

# ---------------- FILE PATHS ----------------
rating_csv = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_rating_202602111506.csv"
details_csv = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_details_202602111506.csv"

json_folder = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/labelme_json3"
save_base = r"C:/Users/Ayushi/Desktop/sanitation_yolo_project/rating_image_3"

os.makedirs(save_base, exist_ok=True)

# ---------------- LOAD CSV ----------------
rating_df = pd.read_csv(rating_csv, low_memory=False)
details_df = pd.read_csv(details_csv, low_memory=False)

rating_df["rating_value"] = rating_df["rating_value"].astype(str).str.lower().str.strip()
rating_df["rating_value_ai"] = rating_df["rating_value_ai"].astype(str).str.lower().str.strip()

merged_df = pd.merge(
    rating_df,
    details_df,
    on="inspection_id",
    how="inner"
)

# ---------------- FILTER LABEL AGREEMENT ----------------
bad_df = merged_df[
    (merged_df["rating_value"] == "poor") &
    (merged_df["rating_value_ai"] == "bad")
]

avg_df = merged_df[
    (merged_df["rating_value"] == "average") &
    (merged_df["rating_value_ai"] == "medium")
]

# ---------------- READ EXISTING JSON IDS ----------------
existing_ids = set()

for file in os.listdir(json_folder):
    if file.endswith(".json"):
        existing_ids.add(os.path.splitext(file)[0] + ".jpg")

print(f"✅ Existing labeled images to skip: {len(existing_ids)}")


# ---------------- IMAGE QUALITY CHECK ----------------
def is_image_valid(image_bytes,
                   min_width=400,
                   min_height=400,
                   blur_threshold=100):

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        width, height = image.size

        if width < min_width or height < min_height:
            return False

        open_cv_image = np.array(image)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        return blur_score >= blur_threshold

    except:
        return False


# ---------------- DOWNLOAD FUNCTION ----------------
def download_category(df, folder_name, target_limit=1000):

    save_dir = os.path.join(save_base, folder_name)
    os.makedirs(save_dir, exist_ok=True)

    image_ids = df["image_id"].dropna().astype(str).unique()

    # skip already labeled json images
    image_ids = [img for img in image_ids if img not in existing_ids]

    print(f"\n📌 Fresh {folder_name} images available: {len(image_ids)}")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    count = 0
    rejected = 0

    for img_name in tqdm(image_ids, desc=f"Downloading {folder_name}"):

        if count >= target_limit:
            break

        url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_name}"

        try:
            r = session.get(url, timeout=25)

            if (
                r.status_code == 200
                and "image" in r.headers.get("Content-Type", "")
                and len(r.content) > 5000
            ):

                if is_image_valid(r.content):
                    file_path = os.path.join(save_dir, img_name)

                    with open(file_path, "wb") as f:
                        f.write(r.content)

                    count += 1
                else:
                    rejected += 1

        except:
            pass

        time.sleep(0.05)

    print(f"✅ {folder_name} downloaded: {count}")
    print(f"❌ Rejected: {rejected}")


# ---------------- RUN ----------------
download_category(bad_df, "bad_images", 1000)
download_category(avg_df, "average_images", 1000)

print("🎉 DONE — 1000 bad + 1000 average new images downloaded.")