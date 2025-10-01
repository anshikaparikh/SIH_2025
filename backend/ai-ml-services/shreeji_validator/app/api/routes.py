from fastapi import APIRouter, UploadFile, File, Form
from app.api.upload_handler import save_upload

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), certificate_id: str = Form(...)):
    """
    Upload certificate and get verification result
    """
    result = await save_upload(file, certificate_id)
    return result
