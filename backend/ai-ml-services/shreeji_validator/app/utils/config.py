import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
LABELS_DIR = os.path.join(DATA_DIR, "labels")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

ML_MODELS_DIR = os.path.join(BASE_DIR, "ml_models")
OCR_MODEL_PATH = os.path.join(ML_MODELS_DIR, "ocr", "ocr_cnn.pth")
FORGERY_MODEL_PATH = os.path.join(ML_MODELS_DIR, "forgery_detection", "image_forgery_cnn.pth")
TEXT_ANOMALY_MODEL_PATH = os.path.join(ML_MODELS_DIR, "text_anomaly", "text_anomaly_model.pkl")


OCR_METHOD = "easyocr"   # 'easyocr' or 'tesseract'
OCR_LANG = "en"


TEXT_WEIGHT = 0.6
IMAGE_WEIGHT = 0.4


API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = True


DB_URI = os.getenv("DB_URI", "sqlite:///" + os.path.join(DATA_DIR, "certificates.db"))


LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


BACKUP_INTERVAL_MIN = 60  # in minutes
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
