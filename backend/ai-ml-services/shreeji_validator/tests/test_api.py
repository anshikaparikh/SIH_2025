from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_verify_endpoint():
    # Temporary dummy file (will be replaced by real certificate later)
    from io import BytesIO
    file = BytesIO(b"dummy file content")
    
    response = client.post(
        "/api/v1/verify", 
        files={"file": ("dummy_certificate.png", file, "image/png")}
    )
    
    # Check response structure
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "anomaly_result" in data
    assert "blockchain_valid" in data
