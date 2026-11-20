import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

# ---------------- FILE PATHS ----------------
rating_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_rating_202602111506.csv"
details_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_details_202602111506.csv"
journey_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_current_assigned_journey_details_202602231216.csv"

bad_images_folder = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/rating_image_1/bad_images"
output_excel = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/bad_images_report.xlsx"

# ---------------- LOAD CSV ----------------
rating_df = pd.read_csv(rating_csv, low_memory=False)
details_df = pd.read_csv(details_csv, low_memory=False)
journey_df = pd.read_csv(journey_csv, low_memory=False)

# Clean column names
rating_df.columns = rating_df.columns.str.strip()
details_df.columns = details_df.columns.str.strip()
journey_df.columns = journey_df.columns.str.strip()

# Normalize rating text
rating_df["rating_value"] = rating_df["rating_value"].astype(str).str.lower().str.strip()
rating_df["rating_value_ai"] = rating_df["rating_value_ai"].astype(str).str.lower().str.strip()

# ---------------- MERGE STEP 1 ----------------
merged_df = pd.merge(
    rating_df,
    details_df,
    on=["inspection_id", "journey_id"],
    how="inner"
)

# ---------------- MERGE STEP 2 ----------------
merged_df = pd.merge(
    merged_df,
    journey_df,
    on="journey_id",
    how="left"
)

# ---------------- FIX DUPLICATE staff_id ----------------
merged_df = merged_df.rename(columns={
    "staff_id_x": "inspection_staff_id",
    "staff_id_y": "journey_staff_id"
})

merged_df["staff_id"] = merged_df["journey_staff_id"]

# ---------------- FILTER ONLY POOR + BAD ----------------
bad_df = merged_df[
    (merged_df["rating_value"] == "poor") &
    (merged_df["rating_value_ai"] == "bad")
]

# Keep only downloaded images
downloaded_images = os.listdir(bad_images_folder)
bad_df = bad_df[bad_df["image_id"].isin(downloaded_images)]

# Limit to 100 images
bad_df = bad_df.head(100)

# ---------------- CREATE EXCEL ----------------
wb = Workbook()
ws = wb.active
ws.title = "Bad Images Report"

headers = [
    "Image",
    "Location",
    "Rating_Value",
    "Rating_AI",
    "Rating_My",
    "Train_Number",
    "Coach_Number",
    "Depot",
    "Division",
    "Staff_ID",
    "Staff_Name",
    "Updated_By",
    "Journey_ID",
    "Inspection_ID",
    "Image_ID"
]

ws.append(headers)

row_num = 2

for index, row in bad_df.iterrows():

    image_path = os.path.join(bad_images_folder, row["image_id"])

    # Insert text data
    ws.cell(row=row_num, column=2, value=row.get("location", ""))
    ws.cell(row=row_num, column=3, value=row.get("rating_value", ""))
    ws.cell(row=row_num, column=4, value=row.get("rating_value_ai", ""))
    ws.cell(row=row_num, column=5, value="")  # Editable column
    ws.cell(row=row_num, column=6, value=row.get("train_number", ""))
    ws.cell(row=row_num, column=7, value=row.get("prs_coach_no", ""))
    ws.cell(row=row_num, column=8, value=row.get("depot", ""))
    ws.cell(row=row_num, column=9, value=row.get("division", ""))
    ws.cell(row=row_num, column=10, value=row.get("staff_id", ""))
    ws.cell(row=row_num, column=11, value=row.get("staff_name", ""))
    ws.cell(row=row_num, column=12, value=row.get("updated_by", ""))
    ws.cell(row=row_num, column=13, value=row.get("journey_id", ""))
    ws.cell(row=row_num, column=14, value=row.get("inspection_id", ""))
    ws.cell(row=row_num, column=15, value=row.get("image_id", ""))

    # Insert LARGE Image
    if os.path.exists(image_path):
        img = XLImage(image_path)
        img.width = 665      # Bigger image
        img.height = 560
        ws.add_image(img, f"A{row_num}")
        ws.row_dimensions[row_num].height = 420  # Larger row height

    row_num += 1

# ---------------- FORMAT COLUMNS ----------------
column_widths = [95, 25, 15, 15, 15, 18, 18, 20, 20, 18, 25, 25, 25, 25, 25]

for i, width in enumerate(column_widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = width

# Wrap and center align text
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical='center')

# Freeze header
ws.freeze_panes = "A2"

# Save file
wb.save(output_excel)

print("✅ Professional Excel created successfully")
print("Saved at:", output_excel)