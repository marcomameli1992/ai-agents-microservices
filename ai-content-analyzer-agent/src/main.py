from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from analyzer_service import ContentAnalyzerService
from entity_classifier import EntityClassifier
import toml
import uvicorn
from typing import List, Dict

config = toml.load("./config/config.toml")

app = FastAPI(title="Content Analyzer Agent", version="1.0.0")
analyzer_service = ContentAnalyzerService(config)
entity_classifier = EntityClassifier(config)

class AnalysisRequest(BaseModel):
    urls: List[dict]

class AnalysisResponse(BaseModel):
    pages: List[Dict]
    total_analyzed: int

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_content(request: AnalysisRequest):
    try:
        results = await analyzer_service.analyze_pages(request.urls)
        classified_entities = await entity_classifier.classify_entities(results)
        return AnalysisResponse(
            pages=classified_entities,
            total_analyzed=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "content-analyzer"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config['services']['content_analyzer_port'])