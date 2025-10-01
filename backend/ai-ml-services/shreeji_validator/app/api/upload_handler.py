import os
import shutil
import uuid
from fastapi import UploadFile, Form
from app.services.verification_pipeline import verify_certificate

UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))

async def save_upload(file: UploadFile, certificate_id: str = Form(...)):
    # Create uploads dir
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    
    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOADS_DIR, unique_name)
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Call main verification pipeline
    result = verify_certificate(file_path, certificate_id)
    return result
