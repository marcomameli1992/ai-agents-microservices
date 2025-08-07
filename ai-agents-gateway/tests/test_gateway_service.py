import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.main import app

client = TestClient(app)

@patch('src.gateway_service.httpx.AsyncClient')
def test_search_endpoint(mock_client_class):
    # Mock del client HTTP
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": ["test result"]}
    mock_response.raise_for_status.return_value = None
    
    mock_client.post.return_value = mock_response
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    response = client.get("/search?query=test")
    assert response.status_code == 200
    assert "results" in response.json()

@patch('src.gateway_service.httpx.AsyncClient')
def test_analyze_endpoint(mock_client_class):
    # Mock delle risposte HTTP
    mock_client = MagicMock()
    
    mock_search_response = MagicMock()
    mock_search_response.json.return_value = {"results": ["search result"]}
    mock_search_response.raise_for_status.return_value = None
    
    mock_analysis_response = MagicMock()
    mock_analysis_response.json.return_value = {"analysis": "test analysis"}
    mock_analysis_response.raise_for_status.return_value = None
    
    mock_client.post.side_effect = [mock_search_response, mock_analysis_response]
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    response = client.post("/analyze", json={"query": "test"})
    assert response.status_code == 200
    assert "query" in response.json()
    assert "search_results" in response.json()
    assert "analysis" in response.json()