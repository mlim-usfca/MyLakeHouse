from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"success": "Hello World"}

def test_list_tables():
    response = client.get("/dashboard/list-tables")
    assert response.status_code == 422 #Unprocessable Entity