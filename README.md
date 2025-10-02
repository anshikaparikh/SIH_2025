CertifyGuard — Academic Certificate Authenticity Validator
Problem Statement: SIH25029 (Authenticity Validator for Academia)  
Team: HackOps 

A role-based platform to verify academic certificates using OCR, text-anomaly detection, image-forgery detection and optional blockchain validation. The system supports both legacy scanned certificates and ERP-generated digital certificates (hash/QR validation), enabling fast, automated and tamper-proof verification.



  Key Features
- Bulk ingestion from university ERP or direct student/employer uploads  
- Image preprocessing + OCR (EasyOCR / Tesseract) for text extraction  
- Text anomaly detection (TF-IDF + Logistic Regression + Fuzzy Matching)  
- Image forgery detection (ResNet18 CNN — PyTorch)  
- Score fusion (text + image) → Verdict: **Genuine / Suspect / Forged**  
- Optional blockchain-backed certificate hash storage & verification (Web3.py)  
- Role-based UI (Students, Employers, Universities, Admins) built in React + Tailwind  
- Containerized deployment (Docker)

  Tech Stack
- Frontend: React.js, TailwindCSS  
- Backend: FastAPI (Python) — AI/ML integration; Golang + Gin — high-performance APIs & business logic  
- Database: PostgreSQL  
- AI / ML: EasyOCR, Tesseract, Scikit-learn (TF-IDF + LR), FuzzyWuzzy, PyTorch (ResNet18)  
- Blockchain: Web3.py, Cryptography  
- **Deployment:** Docker, Uvicorn

---
