from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from search_service import WebSearchService
import toml
import uvicorn
from typing import List

config = toml.load("./config/config.toml")

app = FastAPI(title="Web Search Agent", version="1.0.0")
search_service = WebSearchService(config)

class SearchRequest(BaseModel):
    keywords: List[str]
    max_results: int = 10

class SearchResponse(BaseModel):
    urls: List[dict]
    total_results: int

@app.post("/search", response_model=SearchResponse)
async def search_web(request: SearchRequest):
    try:
        results = await search_service.search(request.keywords, request.max_results)
        return SearchResponse(
            urls=results,
            total_results=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "web-search"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config['services']['web_search_port'])