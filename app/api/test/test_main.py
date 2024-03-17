from fastapi.testclient import TestClient

from api.main import app

def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"success": "Hello World"}