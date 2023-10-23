import csv
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import json
import os
def extract_text_from_pdf(pdf_path, page_num):
    # Load the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Select the page to process (page_num is 0-based)
    page = pdf_document[page_num]
    
    # Convert the page to an image
    image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # 300 DPI for better OCR results
    image_bytes = image.samples
    
    # Convert the image to a PIL image
    pil_image = Image.frombytes("RGB", [image.width, image.height], image_bytes)
    
    # Perform OCR on the PIL image using Tesseract
    extracted_text = pytesseract.image_to_string(pil_image)
    
    return extracted_text

def process(pdf_path):

    # Specify the path to your PDF file
    # pdf_path = '315.pdf'
    # Specify the page number to process (0-based)
    page_number = 0

    # Extract text from the specified page
    invoice_text = extract_text_from_pdf(pdf_path, page_number)
    
    # Your input text
    text = invoice_text.split("\n")
    for i in text:
        if "PAN" in i:
            j = i.split(" ")
            pan_number = j[3]
        if "FSSAI_" in i:
            j = i.split(" ")
            fssai_number = j[2]
        if "Grand Total" in i:
            j = i.split(" ")
            grand_total = j[-1]
        if "Invoice No." in i:
            j = i.split(" ")
            invoice_number = j[3]
        if "GSTIN" in i:
            j = i.split(" ")
            gst = j[2]
        if "IFSC" in i:
            j = i.split(" ")
            k = j[2] + " "+ j[3] + " "+j[4]+" "+j[5]
            bank = k
            acno = j[8]
            ifsc = j[11]
    
    # Extract PAN details
    # pan_match = re.search(r'PAN NO : ([A-Z0-9]+)', text)
    # if pan_match:
    #     pan_number = pan_match.group(1)
    # else:
    #     pan_number = "Not found"

    # # Extract FSSAI
    # fssai_match = re.search(r'FSSAI_ =: ([0-9]+)', text)
    # if fssai_match:
    #     fssai_number = fssai_match.group(1)
    # else:
    #     fssai_number = "Not found"

    # Extract grand total amount
    # grand_total_match = re.search(r'Exempt.*?(\d{1,3}(,\d{3})*(\.\d+)?)', text)
    # if grand_total_match:
    #     grand_total = grand_total_match.group(1)
    # else:
    #     grand_total = "Not found"

    # Extract shipping address
    shipping_address_match = re.search(r'Shipped to :([\s\S]+?)FSSAI', invoice_text)
    if shipping_address_match:
        shipping_address = shipping_address_match.group(1).strip()
    else:
        shipping_address = "Not found"

    # Extract date of invoice
    date_of_invoice_match = re.search(r'Date of Invoice : ([\d-]+)', invoice_text)
    if date_of_invoice_match:
        date_of_invoice = date_of_invoice_match.group(1)
    else:
        date_of_invoice = "Not found"

    # # Extract invoice number
    # invoice_number_match = re.search(r'Invoice No\. > ([0-9]+)', invoice_text)
    # if invoice_number_match:
    #     invoice_number = invoice_number_match.group(1)
    # else:
    #     invoice_number = "Not found"

    # Print the extracted information
    # print("PAN Number:", pan_number)
    # print("FSSAI Number:", fssai_number)
    # print("Grand Total Amount:", grand_total)
    # print("Shipping Address:", shipping_address)
    # print("Date of Invoice:", date_of_invoice)
    # print("Invoice Number:", invoice_number)

    data = {}
    data["PAN Number"] = pan_number
    data["FSSAI Number"] = fssai_number
    data["Grand Total Amount"] = grand_total
    shipping_address = shipping_address.replace("\n"," ")
    data["Shipping Address"] = shipping_address
    data["Date of Invoice"] = date_of_invoice
    data["Invoice Number"] = invoice_number
    data["GSTIN"] = gst
    data["BANK"] = bank
    data["A/C NO"] = acno
    data["IFSC CODE"] = ifsc
    csv_file_name = 'output.csv'
    headers = data.keys()

    # Write the data to the CSV file
    csv_filename = "output.csv"

    # Check if the CSV file already exists
    file_exists = os.path.exists(csv_filename)

    with open(csv_file_name, mode='a' if file_exists else 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        if not file_exists:
            # If the file doesn't exist, write the header
            writer.writeheader()
        writer.writerow(data)

    print(f'CSV file "{csv_file_name}" created successfully.')
