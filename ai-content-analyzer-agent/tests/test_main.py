from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "content-analyzer"}

def test_analyze_content():
    response = client.post("/analyze", json={"urls": [{"href": "http://example.com", "affinity_score": 0.95}]})
    assert response.status_code == 200
    assert "pages" in response.json()
    assert "total_analyzed" in response.json()