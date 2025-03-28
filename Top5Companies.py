import os
import json
import shutil
from collections import Counter

# Paths to the original dataset
original_entities_folder = "../Dataset/SROIE2019/test/entities"
original_images_folder = "../Dataset/SROIE2019/test/img"
original_box_folder = "../Dataset/SROIE2019/test/box"

# Paths for the new filtered dataset
filtered_dataset_folder = "SROIE_filtered_dataset"
filtered_entities_folder = os.path.join(filtered_dataset_folder, "entities")
filtered_images_folder = os.path.join(filtered_dataset_folder, "img")
filtered_box_folder = os.path.join(filtered_dataset_folder, "box")

# Create directories
os.makedirs(filtered_entities_folder, exist_ok=True)
os.makedirs(filtered_images_folder, exist_ok=True)
os.makedirs(filtered_box_folder, exist_ok=True)

# Step 1: Collect all company names
company_counts = Counter()
entity_files = os.listdir(original_entities_folder)

for filename in entity_files:
    file_path = os.path.join(original_entities_folder, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            company_name = data.get("company", "Unknown")
            company_counts[company_name] += 1
        except json.JSONDecodeError:
            print(f"Skipping {filename}: Invalid JSON format")

# Step 2: Identify the top 5 companies
top_5_companies = [c[0] for c in company_counts.most_common(4)]
print("Top 5 Companies:", top_5_companies)

# Step 3: Copy only files related to the top 5 companies
for filename in entity_files:
    entity_path = os.path.join(original_entities_folder, filename)

    with open(entity_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            company_name = data.get("company", "Unknown")
            
            # If company is in the top 5, copy related files
            if company_name in top_5_companies:
                # Copy entity file
                shutil.copy(entity_path, os.path.join(filtered_entities_folder, filename))
                
                # Copy image file
                image_path = os.path.join(original_images_folder, filename.replace(".txt", ".jpg"))
                if os.path.exists(image_path):
                    shutil.copy(image_path, os.path.join(filtered_images_folder, os.path.basename(image_path)))
                
                # Copy box annotation file
                box_path = os.path.join(original_box_folder, filename)
                if os.path.exists(box_path):
                    shutil.copy(box_path, os.path.join(filtered_box_folder, os.path.basename(box_path)))

        except json.JSONDecodeError:
            print(f"Skipping {filename}: Invalid JSON format")

print(f"Filtered dataset created at: {filtered_dataset_folder}")
