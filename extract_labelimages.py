import os
import shutil

image_folder = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/rating_image_2/bad_images"
json_folder = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/labelme_jsons1"
output_folder = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/images_of_json"

os.makedirs(output_folder, exist_ok=True)

# get list of all images
images = os.listdir(image_folder)

for json_file in os.listdir(json_folder):

    if json_file.endswith(".json"):

        base_name = os.path.splitext(json_file)[0]   # remove .json

        for img in images:
            img_base = os.path.splitext(img)[0]      # remove image extension

            if img_base == base_name:

                src = os.path.join(image_folder, img)
                dst = os.path.join(output_folder, img)

                shutil.copy(src, dst)
                print("Copied:", img)

print("Done! Labeled images copied.")