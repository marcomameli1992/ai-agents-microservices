import pytest
import asyncio
import aiohttp
from unittest.mock import AsyncMock, patch
from analyzer_service import ContentAnalyzerService

@pytest.fixture
def content_analyzer_service():
    config = {
        'ai_models': {'max_concurrent_requests': 5},
        'services': {'content_analyzer_port': 8002}
    }
    return ContentAnalyzerService(config)

@pytest.mark.asyncio
async def test_analyze_pages(content_analyzer_service):
    urls = [{'href': 'http://example.com', 'affinity_score': 0.95}]
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = '<html><title>Test</title><body>Test content</body></html>'
        mock_get.return_value.__aenter__.return_value = mock_response
        
        results = await content_analyzer_service.analyze_pages(urls)
        assert isinstance(results, list)

@pytest.mark.asyncio
async def test_analyze_single_page(content_analyzer_service):
    url_data = {'href': 'http://example.com'}
    
    # Usa un context manager per ClientSession
    async with aiohttp.ClientSession() as session:
        with patch.object(session, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text.return_value = '<html><title>Test</title><body>Test content</body></html>'
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await content_analyzer_service._analyze_single_page(
                asyncio.Semaphore(5), 
                session, 
                url_data
            )
            assert result is not None
            assert result['url'] == 'http://example.com'
            assert 'title' in result