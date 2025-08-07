from pydantic import BaseModel
from typing import List, Optional, Any

class SearchRequest(BaseModel):
    query: str
    filters: Optional[dict] = None

class SearchResponse(BaseModel):
    results: List[dict]
    total_results: int

class ContentAnalysisRequest(BaseModel):
    content: str
    analysis_type: str

class ContentAnalysisResponse(BaseModel):
    analysis_results: dict
    summary: str

class AnalyzeRequest(BaseModel):
    query: str

class AnalyzeResponse(BaseModel):
    query: str
    search_results: Any
    analysis: Any