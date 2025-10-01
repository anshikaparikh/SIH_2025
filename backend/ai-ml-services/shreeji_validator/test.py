# test_ocr.py

from app.services.ocr_service import OCRService

# 1. Initialize OCR service (easyocr ya tesseract)
ocr = OCRService(method='easyocr', lang='en')

# 2. Image path (uploaded certificate)
image_path = "data/raw/abc.jpg"

# 3. Extract text
extracted_text = ocr.extract_text(image_path)

# 4. Print results
print("----- Extracted Text -----")
print(extracted_text)




