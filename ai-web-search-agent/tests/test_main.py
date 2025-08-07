from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "web-search"}

def test_search_web():
    response = client.post("/search", json={"keywords": ["Python", "AI"], "max_results": 5})
    assert response.status_code == 200
    assert "urls" in response.json()
    assert "total_results" in response.json()