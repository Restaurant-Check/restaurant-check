import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# Open the PDF file
pdf_path = 'testpdf2.pdf'
doc = fitz.open(pdf_path)

complete_text = ""

# Iterate through each page
for page_number in range(len(doc)):
    page = doc.load_page(page_number)  # Load each page

    # Extract text
    complete_text += page.get_text()

    # Extract images and perform OCR
    image_list = page.get_images(full=True)
    for image in image_list:
        #print(image)
        pass

complete_text = complete_text.strip()
complete_text = complete_text.replace("\n", " ")
print("Extracted text of length:", len(complete_text))
print("\n\n\n" + complete_text)

doc.close()
