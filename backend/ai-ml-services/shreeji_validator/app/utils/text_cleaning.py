import re
import unicodedata

def clean_text(text):
    """
    Clean OCR extracted text.
    Steps:
    1. Normalize unicode characters
    2. Remove extra spaces and newlines
    3. Remove unwanted symbols
    4. Lowercase everything
    """

    if not text:
        return ""

    # Step 1: Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Step 2: Remove unwanted symbols (keep alphanumerics, basic punctuation)
    text = re.sub(r"[^a-zA-Z0-9\s.,/-]", "", text)

    # Step 3: Remove multiple spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()

    # Step 4: Lowercase
    text = text.lower()

    return text

# Example usage
if __name__ == "__main__":
    raw_text = """
        ANSHIKA PARIKH
        Completed Python Bootcamp, Date: 24-09-2025!
    """
    cleaned = clean_text(raw_text)
    print("=== Cleaned Text ===")
    print(cleaned)
