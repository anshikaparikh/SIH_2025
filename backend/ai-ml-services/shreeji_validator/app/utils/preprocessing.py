# app/utils/preprocessing.py
import cv2
import numpy as np

def load_image(img_path):
    """Load image from file"""
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {img_path}")
    return img

def resize_image(img, width=1024, height=768):
    """Resize image to standard dimensions"""
    return cv2.resize(img, (width, height))

def to_grayscale(img):
    """Convert image to grayscale"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def denoise_image(img):
    """Remove noise using Gaussian and median blur"""
    blur = cv2.GaussianBlur(img, (3,3), 0)
    denoised = cv2.medianBlur(blur, 3)
    return denoised

def adaptive_threshold(img):
    """Apply adaptive thresholding for better OCR"""
    return cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

def deskew_image(img):
    """Correct skew of image using moments"""
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), 
                             flags=cv2.INTER_CUBIC, 
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated

def enhance_edges(img):
    """Optional: enhance edges for OCR"""
    return cv2.Canny(img, 100, 200)

def preprocess_image(img_path, resize_dim=(1024,768), enhance=False):
    """Full preprocessing pipeline"""
    img = load_image(img_path)
    img = resize_image(img, *resize_dim)
    gray = to_grayscale(img)
    denoised = denoise_image(gray)
    thresh = adaptive_threshold(denoised)
    deskewed = deskew_image(thresh)
    if enhance:
        deskewed = enhance_edges(deskewed)
    return deskewed

# Example usage
if __name__ == "__main__":
    img_path = "data/raw/sample_certificate.jpg"
    processed_img = preprocess_image(img_path, enhance=True)
    cv2.imwrite("data/processed/sample_certificate_processed.jpg", processed_img)
    print("Preprocessing done. Saved to processed folder.")
