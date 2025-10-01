from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os, uuid, json
from ml_models.blockchain_integration.hash_generator import generate_hash_from_file
from ml_models.blockchain_integration.qr_utils import generate_qr
from app.services.blockchain_service import register_hash, is_registered

app = FastAPI(title='Certificate Verification API')

UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'data/raw')

@app.post('/register')
async def register(file: UploadFile = File(...), issuer: str = Form(...)):
    # Save file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, 'wb') as f:
        f.write(await file.read())

    cert_hash = generate_hash_from_file(path)
    # NOTE: in production, use secure key management (not env var)
    private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
    if not private_key:
        raise HTTPException(status_code=500, detail='Private key not configured on server')
    tx = register_hash(cert_hash, private_key)
    # generate QR payload (verification URL)
    verify_url = f"/verify?hash={cert_hash}&tx={tx['tx_hash']}"
    qr_path = f"data/processed/{filename}.qr.png"
    os.makedirs('data/processed', exist_ok=True)
    generate_qr(verify_url, qr_path)

    return JSONResponse({'hash': cert_hash, 'tx': tx['tx_hash'], 'qr': qr_path})

@app.get('/verify')
async def verify(hash: str, tx: str = None):
    registered = is_registered(hash)
    return JSONResponse({'hash': hash, 'registered': registered, 'tx': tx})
