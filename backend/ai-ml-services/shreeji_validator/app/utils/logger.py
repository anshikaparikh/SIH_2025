import logging
import os
from logging.handlers import RotatingFileHandler
from app.utils.config import LOG_DIR


os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger("CertificateVerificationSystem")
logger.setLevel(logging.INFO)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)


file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
file_handler.setFormatter(file_format)


logger.addHandler(console_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    logger.info("Logger initialized successfully!")
    logger.warning("This is a warning example")
    logger.error("This is an error example")
