from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class StoreRequest(BaseModel):
    certificate_id: str
    hash: str

blockchain_storage = {}  # replace with real blockchain logic

@app.post("/store")
def store(req: StoreRequest):
    blockchain_storage[req.certificate_id] = req.hash
    return {"status": "stored"}

@app.post("/verify")
def verify(req: StoreRequest):
    stored = blockchain_storage.get(req.certificate_id)
    return {"exists": stored == req.hash}
