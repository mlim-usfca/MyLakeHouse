from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_list_tables():
    response = client.get("/dashboard/list-tables")
    assert response.status_code == 422 #Unprocessable Entity

def test_get_snapshot():
    response = client.get("/dashboard/snapshot")
    assert response.status_code == 422  # Unprocessable Entity

def test_expire_snapshot():
    response = client.get("/dashboard/expire-snapshot")
    assert response.status_code == 422 # Unprocessable Entity

