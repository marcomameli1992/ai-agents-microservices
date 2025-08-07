import asyncio
import aiohttp
from duckduckgo_search import DDGS
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import logging

class WebSearchService:
    def __init__(self, config):
        self.config = config
        self.model = SentenceTransformer(config['ai_models']['search_model'])
        self.logger = logging.getLogger(__name__)
        
    async def search(self, keywords: List[str], max_results: int = 10) -> List[Dict]:
        """Esegue ricerca web con ranking per affinità"""
        query = " ".join(keywords)
        
        try:
            # Ricerca con DuckDuckGo
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            
            # Calcola affinità usando sentence transformers
            if results:
                results_with_affinity = await self._calculate_affinity(keywords, results)
                return sorted(results_with_affinity, key=lambda x: x['affinity_score'], reverse=True)
            
            return []
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            raise e
    
    async def _calculate_affinity(self, keywords: List[str], results: List[Dict]) -> List[Dict]:
        """Calcola score di affinità per ogni risultato"""
        query_embedding = self.model.encode(" ".join(keywords))
        
        enhanced_results = []
        for result in results:
            # Combina titolo e snippet per l'embedding
            text = f"{result.get('title', '')} {result.get('body', '')}"
            result_embedding = self.model.encode(text)
            
            # Calcola similarità coseno
            similarity = np.dot(query_embedding, result_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(result_embedding)
            )
            
            result['affinity_score'] = float(similarity)
            enhanced_results.append(result)
        
        return enhanced_results