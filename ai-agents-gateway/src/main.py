from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from gateway_service import GatewayService
from models.schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="AI Agents Gateway", version="1.0.0")

# Aggiungi CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gateway_service = GatewayService()

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Agents Gateway!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/search")
async def search(query: str):
    results = await gateway_service.search(query)
    return {"results": results}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    # Prima effettua la ricerca
    search_results = await gateway_service.search(request.query)
    
    # Poi applica l'analisi sui risultati della ricerca
    analysis = await gateway_service.analyze(search_results)
    
    return AnalyzeResponse(
        query=request.query,
        search_results=search_results,
        analysis=analysis
    )