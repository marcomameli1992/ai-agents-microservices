import httpx
from utils.logging_config import logger

class GatewayService:
    def __init__(self):
        self.ai_web_search_agent_url = "http://ai-web-search-agent:8001"
        self.ai_content_analyzer_agent_url = "http://ai-content-analyzer-agent:8002"
    
    async def search(self, query: str):
        """Effettua una ricerca usando l'agente di ricerca web"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ai_web_search_agent_url}/search", 
                    json={"keywords": [query], "max_results": 10}
                )
                response.raise_for_status()
                result = response.json()
                return result.get("urls", [])
        except Exception as e:
            logger.error(f"Errore durante la ricerca: {e}")
            return {"error": str(e)}
    
    async def analyze(self, search_results):
        """Analizza il contenuto usando l'agente di analisi"""
        try:
            # Adatta i risultati della ricerca al formato atteso dall'analyzer
            if isinstance(search_results, dict) and "error" in search_results:
                return search_results
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ai_content_analyzer_agent_url}/analyze",
                    json={"urls": search_results}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Errore durante l'analisi: {e}")
            return {"error": str(e)}