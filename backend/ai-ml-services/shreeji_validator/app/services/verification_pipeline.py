from app.services.ocr_service import OCRService
from app.services.text_anomaly_service import TextAnomalyService
from ml_models.forgery_detection.forgery_service import ForgeryDetectionService
import re
import json
from datetime import datetime
import os

def extract_fields_from_text(text):
    """Extract structured fields from OCR text using regex patterns"""
    extracted = {}

    # Student Name - look for "name" followed by text
    name_match = re.search(r'(?i)name[:\s]*([a-zA-Z\s]+?)(?=\n|$)', text)
    if name_match:
        extracted['student_name'] = name_match.group(1).strip().title()  # Title case for proper name

    # Roll Number
    roll_match = re.search(r'(?i)(roll|id|reg|matric)[:\s]*(\w+)', text)
    if roll_match:
        extracted['roll_number'] = roll_match.group(2).strip()

    # Course/Degree
    course_match = re.search(r'(?i)(course|degree|program)[:\s]*([a-zA-Z\s]+?)(?=\n|$)', text)
    if course_match:
        extracted['course'] = course_match.group(2).strip().title()  # Title case for course

    # Issued On
    date_match = re.search(r'(?i)(issued|date|on)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
    if date_match:
        extracted['issued_on'] = date_match.group(2).strip()

    return extracted

def verify_certificate(file_path, certificate_id):
    """Full verification pipeline"""
    checks = []
    scores = []
    
    # 1. OCR Extraction
    ocr = OCRService()
    filename = os.path.basename(file_path)  # Extract just the filename
    ocr_text = ocr.extract_text(filename)
    extracted_data = extract_fields_from_text(ocr_text)
    
    checks.append({
        "check": "OCR Extraction",
        "passed": len(extracted_data) > 0,
        "details": f"Extracted {len(extracted_data)} fields: {list(extracted_data.keys())}"
    })
    scores.append(0.25 if len(extracted_data) > 0 else 0.0)
    
    # 2. Text Anomaly Detection
    if ocr_text:
        text_anomaly = TextAnomalyService()
        anomaly_score = text_anomaly.detect_anomalies(ocr_text)
        checks.append({
            "check": "Text Anomaly Detection",
            "passed": anomaly_score < 0.5,  # Threshold for anomaly
            "details": f"Anomaly score: {anomaly_score:.2f}"
        })
        scores.append(1.0 - anomaly_score)
    else:
        checks.append({"check": "Text Anomaly Detection", "passed": False, "details": "No text for analysis"})
        scores.append(0.0)
    
    # 3. Forgery Detection (Image-based)
    forgery_service = ForgeryDetectionService()
    forgery_score = forgery_service.detect_forgery(file_path)
    checks.append({
        "check": "Forgery Detection",
        "passed": forgery_score < 0.3,  # Low forgery probability
        "details": f"Forgery probability: {forgery_score:.2f}"
    })
    scores.append(1.0 - forgery_score)
    
    # 4. Overall Score (average of all checks)
    overall_score = sum(scores) / len(scores)
    
    result = {
        "certificate_id": certificate_id,
        "extracted_data": extracted_data,
        "checks": checks,
        "score": round(overall_score, 2),
        "status": "verified" if overall_score > 0.7 else "suspicious"
    }
    
    return result
