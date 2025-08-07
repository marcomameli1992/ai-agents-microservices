from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Agents Gateway!"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_missing_query():
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # Validation error per campo mancante