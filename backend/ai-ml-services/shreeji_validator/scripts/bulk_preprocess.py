"""
bulk_preprocess.py
Automation script to preprocess raw data in bulk (images, PDFs, text)
"""

import os
from app.utils.preprocessing import clean_image
from app.utils.text_cleaning import clean_text

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def process_all_files():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    for filename in os.listdir(RAW_DIR):
        file_path = os.path.join(RAW_DIR, filename)
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            cleaned = clean_image(file_path)
            out_path = os.path.join(PROCESSED_DIR, filename)
            cleaned.save(out_path)
            print(f"Processed image: {filename}")
        elif filename.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            cleaned = clean_text(text)
            out_path = os.path.join(PROCESSED_DIR, filename)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Processed text: {filename}")
        else:
            print(f"Skipped unsupported file: {filename}")

if __name__ == "__main__":
    process_all_files()
