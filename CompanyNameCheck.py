import os
import json
from collections import Counter
import pandas as pd

# Path to the entities folder
entities_folder = "../Dataset/SROIE2019/train/entities"

# Dictionary to store company name counts
company_counter = Counter()
data = []

# Iterate through all files in the entities folder
for filename in os.listdir(entities_folder):
    file_path = os.path.join(entities_folder, filename)
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)  # Parse JSON
            company_name = json_data.get("company", "Unknown")  # Get company name
            company_counter[company_name] += 1  # Count occurrences
            
            # Store the data for later use
            data.append((filename, company_name))
            
        except json.JSONDecodeError:
            print(f"Skipping {filename}: Invalid JSON format")

# Get the top 8 most frequent companies
top_8_companies = {company for company, _ in company_counter.most_common(10)}

# Create labeled data
df = pd.DataFrame(data, columns=["filename", "company"])
df["label"] = df["company"].apply(lambda x: x if x in top_8_companies else "Other")

# Print dataset summary
print(f"Total Unique Companies: {len(company_counter)}")
print(f"Top 8 Companies: {top_8_companies}")
print(df["label"].value_counts())

# Save to CSV for training
df.to_csv("receipt_company_labels.csv", index=False)
print("Saved labeled dataset to receipt_company_labels.csv")
