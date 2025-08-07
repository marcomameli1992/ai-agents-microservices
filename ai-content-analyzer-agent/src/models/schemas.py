from pydantic import BaseModel
from typing import List, Dict

class AnalysisRequest(BaseModel):
    urls: List[Dict]

class AnalysisResponse(BaseModel):
    pages: List[Dict]
    total_analyzed: int

class EntityClassificationRequest(BaseModel):
    content: List[Dict]

class EntityClassificationResponse(BaseModel):
    entities: List[Dict]
    total_entities: int