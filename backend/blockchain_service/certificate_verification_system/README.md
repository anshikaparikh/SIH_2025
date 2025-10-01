# Certificate Verification System (SIH25029)
This repository skeleton contains the core files for the Certificate Verification System described in your uploaded "Certificate Verification Structure.pdf". fileciteturn1file0

## High-level flow
1. Upload certificate (ERP / Web UI) → saved to `data/raw/`
2. `scripts/bulk_preprocess.py` cleans and stores to `data/processed/`
3. `ml_models/*` contains model helpers (OCR, forgery detection, blockchain helpers)
4. `app/` contains the API (FastAPI) and services (blockchain, OCR)
5. Register certificate hash on blockchain and return QR code / tx-hash for verification
6. Users can verify using `/verify` endpoint or by scanning the QR code

## Quick start (local, without Docker)
```bash
# 1. clone repo
git clone <your-repo-url>
cd certificate_verification_system

# 2. create venv and install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run local ganache (or use testnet)
# install ganache-cli or use Ganache GUI
ganache-cli -p 8545

# 4. Deploy contract (see contracts/README in this skeleton)
# 5. Start API
export WEB3_PROVIDER=http://127.0.0.1:8545
export CONTRACT_ADDRESS=<deployed_contract_address>
uvicorn app.api.routes:app --reload --port 8000
```

## Team tasks suggestions
- Backend (Vansh): API endpoints in `app/api/routes.py`, DB integration
- AI/ML (Anshika): OCR, forgery detection under `ml_models/` and `app/services/ocr_service.py`
- Blockchain & Deployment (Abhishek): blockchain helpers in `ml_models/blockchain_integration/`, `app/services/blockchain_service.py`, Dockerfile, CI/CD

## Files created by this skeleton
- `ml_models/blockchain_integration/hash_generator.py`
- `ml_models/blockchain_integration/hash_validator.py`
- `ml_models/blockchain_integration/qr_utils.py`
- `app/services/blockchain_service.py`
- `app/api/routes.py`
- `scripts/bulk_preprocess.py`
- `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `tests/test_blockchain.py`

See other files and the examples below for code you can paste into these files.
