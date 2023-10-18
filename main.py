
import requests
import json
import csv
import os.path
import os
url = 'https://app.nanonets.com/api/v2/OCR/Model/54a46a9f-afcb-4f95-93fe-290684559102/LabelFile/?async=false'

import tkinter as tk
from tkinter import filedialog

# Create the root window
root = tk.Tk()

# Hide the root window
root.withdraw()

# Open the file dialog and get the filename
filename = filedialog.askopenfilename()

data = {'file': open(filename, 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('3eae95f7-6d30-11ee-8668-da444e89fb68', ''), files=data)

json_string = response.text
json_data = json.loads(json_string)

print(type(json_data))
# CSV filename
csv_filename = "prediction_data.csv"

# Extract the prediction data from the JSON
prediction_data = json_data["result"][0]["prediction"]

# Check if the CSV file already exists
file_exists = os.path.exists(csv_filename)

# Open the CSV file in append or write mode, depending on whether it exists
with open(csv_filename, mode='a' if file_exists else 'w', newline='') as csv_file:
    fieldnames = prediction_data[0].keys()

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not file_exists:
        # If the file doesn't exist, write the header
        writer.writeheader()

    # Write the prediction data to the CSV file
    writer.writerows(prediction_data)

print(f"Prediction data has been successfully {'appended to' if file_exists else 'written to'} '{csv_filename}'.")
