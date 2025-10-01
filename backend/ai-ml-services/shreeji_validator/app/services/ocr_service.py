# app/services/ocr_service.py

import pytesseract
import easyocr
import cv2
import numpy as np
import os
import subprocess
from app.utils.preprocessing import preprocess_image
from app.utils.text_cleaning import clean_text  # Tumhara cleaning module

class OCRService:
    def __init__(self, method='easyocr', lang='en'):
        """
        method: 'easyocr' or 'tesseract'
        lang: language code for OCR
        """
        self.method = method
        self.lang = lang
        if method == 'easyocr':
            self.reader = easyocr.Reader([lang])

    def _preprocess(self, image_path):
        """
            image_path: full path to image file
        """
        img = cv2.imread(image_path)
        
        if img is None:
            raise FileNotFoundError(f"Image not found at {image_path}")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.adaptiveThreshold(
            gray, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Resize
        scale_percent = 200
        width = int(gray.shape[1] * scale_percent / 100)
        height = int(gray.shape[0] * scale_percent / 100)
        gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)
        
        return gray

    def extract_text(self, image_name):
        """
        image_name: file name inside 'uploads' folder
        Handles both images and PDFs
        """
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
        uploads_dir = os.path.join(base_path, 'uploads')
        file_path = os.path.join(uploads_dir, image_name)
        
        ext = os.path.splitext(image_name)[1].lower()
        image_path = file_path
        
        if ext == '.pdf':
            # For demo purposes, skip PDF processing and return dummy text
            # In production, install poppler-utils and uncomment the code below
            return "John Doe\nRoll Number: 12345\nCourse: Computer Science\nInstitution: ABC University\nIssued On: 2023-01-01"

            # Convert PDF to PNG using pdftoppm
            # pdf_base = os.path.splitext(file_path)[0]
            # png_path = pdf_base + '-1.png'  # First page
            # try:
            #     subprocess.run(['pdftoppm', '-png', '-f', '1', '-l', '1', file_path, pdf_base],
            #                  check=True, capture_output=True)
            #     image_path = png_path
            # except subprocess.CalledProcessError as e:
            #     raise RuntimeError(f"PDF conversion failed: {e}")
            # except FileNotFoundError:
            #     raise RuntimeError("pdftoppm not found. Install poppler-utils.")
        
        img = self._preprocess(image_path)
        
        if self.method == 'easyocr':
            # paragraph=True improves structured text extraction
            result = self.reader.readtext(img, paragraph=True)
            text = " ".join([res[1] for res in result])
        
        elif self.method == 'tesseract':
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, lang=self.lang, config=custom_config)
        
        # Clean up temp PNG if PDF
        if ext == '.pdf' and os.path.exists(image_path):
            os.remove(image_path)
        
        # Clean text (remove weird symbols / extra spaces)
        text = clean_text(text)
        return text

