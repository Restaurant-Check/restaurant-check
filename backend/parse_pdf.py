import io

import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Open the PDF file
pdf_path = 'levespemenu.pdf'
doc = fitz.open(pdf_path)

OCR = True

complete_text = ""

# Iterate through each page
n_pages = len(doc)
for page_number in range(n_pages):
    print("Processing page", page_number + 1, "of", n_pages)

    page = doc.load_page(page_number)  # Load each page

    # Extract text
    complete_text += page.get_text().strip() + " "

    # Extract images and perform OCR
    if OCR:
        image_list = page.get_images(full=True)
        for img_ref in image_list:
            xref = img_ref[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            extracted_image_text = pytesseract.image_to_string(image, lang='eng')
            complete_text += extracted_image_text

complete_text = complete_text.strip()
complete_text = complete_text.replace("\n", " ")
print("Extracted text of length:", len(complete_text))
print("\n\n--- START OF EXTRACTED TEXT ---\n" + complete_text)

doc.close()
