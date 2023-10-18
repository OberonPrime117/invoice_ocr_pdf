import requests
import json
import csv
import os.path
import os
import tkinter as tk
from tkinter import filedialog

url = 'https://app.nanonets.com/api/v2/OCR/Model/54a46a9f-afcb-4f95-93fe-290684559102/LabelFile/?async=false'

# Create the root window
root = tk.Tk()

# Hide the root window
root.withdraw()

# Open the file dialog and get the filename
filename = filedialog.askopenfilename()

data = {'file': open(filename, 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('3eae95f7-6d30-11ee-8668-da444e89fb68', ''), files=data)

json_data = json.loads(response.text)

# Extract the prediction data from the JSON
prediction_data = json_data["result"][0]["prediction"]

# Create a dictionary to store data for each label
data_dict = {}

# Iterate through the prediction data and organize it by labels
for item in prediction_data:
    label = item["label"]
    ocr_text = item["ocr_text"]
    if label not in data_dict:
        data_dict[label] = [ocr_text]
    else:
        data_dict[label].append(ocr_text)

# CSV filename
csv_filename = "prediction_data.csv"

# Check if the CSV file already exists
file_exists = os.path.exists(csv_filename)

# Open the CSV file in append or write mode, depending on whether it exists
with open(csv_filename, mode='a' if file_exists else 'w', newline='') as csv_file:
    fieldnames = list(data_dict.keys())

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not file_exists:
        # If the file doesn't exist, write the header
        writer.writeheader()

    # Create a dictionary with labels as keys and OCR text as values
    row_data = {label: data_dict[label][0] if label in data_dict else "" for label in fieldnames}

    # Write the row data to the CSV file
    writer.writerow(row_data)

print(f"Prediction data has been successfully {'appended to' if file_exists else 'written to'} '{csv_filename}'.")
