from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from storage_service import DataStorageService
import toml
import uvicorn
from typing import Dict, Any

config = toml.load("../config/config.toml")

app = FastAPI(title="Data Storage Agent", version="1.0.0")
storage_service = DataStorageService(config)

class StorageRequest(BaseModel):
    task_id: str
    search_results: Dict[str, Any]
    analyzed_content: Dict[str, Any]

class StorageResponse(BaseModel):
    success: bool
    file_path: str
    records_count: int

@app.post("/store", response_model=StorageResponse)
async def store_data(request: StorageRequest):
    try:
        result = await storage_service.store_analysis(
            request.task_id,
            request.search_results,
            request.analyzed_content
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/{task_id}")
async def get_data(task_id: str):
    try:
        data = await storage_service.get_task_data(task_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "data-storage"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config['services']['data_storage_port'])