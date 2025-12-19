from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    
def test_detect_image_no_file():
    resp = client.post("/detect-image", files={})
    assert resp.status_code == 422
