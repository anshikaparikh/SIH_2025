from app.services.ocr_service import run_ocr
from app.services.anomaly_service import run_anomaly

def test_ocr_function():
    # Test OCR with dummy path
    result = run_ocr("dummy_path")
    # Will return real text later
    assert isinstance(result, str)

def test_anomaly_function():
    # Test anomaly detection with dummy text
    result = run_anomaly("dummy text")
    # Will return real result later
    assert isinstance(result, str)
