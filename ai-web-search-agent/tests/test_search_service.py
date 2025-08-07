import pytest
from src.search_service import WebSearchService

class MockConfig(dict):
    def __init__(self):
        super().__init__()
        self['ai_models'] = {'search_model': 'all-MiniLM-L6-v2'}
        self['services'] = {'web_search_port': 8000}

@pytest.fixture
def web_search_service():
    config = MockConfig()
    service = WebSearchService(config)
    return service

@pytest.mark.asyncio
async def test_search(web_search_service):
    keywords = ["Python", "AI"]
    results = await web_search_service.search(keywords, max_results=5)
    assert isinstance(results, list)
    assert len(results) <= 5

@pytest.mark.asyncio
async def test_search_no_results(web_search_service):
    keywords = ["nonexistentkeyword"]
    results = await web_search_service.search(keywords, max_results=5)
    # Verifico che il risultato sia una lista ed eventualmente altre proprietà
    assert isinstance(results, list)
    # Se la logica dovesse restituire sempre una lista, potresti controllare ad esempio che il numero di risultati
    # non superi il massimo specificato
    assert len(results) <= 5