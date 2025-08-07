from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    keywords: List[str]
    max_results: int = 10

class SearchResponse(BaseModel):
    urls: List[dict]
    total_results: int