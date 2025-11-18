# app/api/main.py
from fastapi import FastAPI, HTTPException
from app.api.models import QueryRequest, QueryResponse
from app.retrieve.query_engine import QueryEngine
from typing import Dict, Any

# --- Application Setup ---
app = FastAPI(
    title="AI-Enhanced Crypto Intelligence API",
    description="API for querying ingested crypto news articles.",
    version="1.0.0"
)

# --- Global Objects ---
try:
    query_engine = QueryEngine()
    print("✅ QueryEngine loaded successfully.")
except Exception as e:
    print(f"❌ FATAL ERROR: Could not initialize QueryEngine: {e}")
    query_engine = None

# --- API Endpoints ---
@app.get("/", tags=["Monitoring"])
async def get_health_status() -> Dict[str, str]:
    """
    Simple health check endpoint.
    """
    if query_engine is None:
        raise HTTPException(status_code=503, detail="Service Unavailable: Query Engine failed to load.")
    return {"status": "ok"}

@app.post("/api/v1/query", response_model=QueryResponse, tags=["RAG"])
async def execute_query(request: QueryRequest) -> QueryResponse:
    """
    Accepts a user query and returns semantically similar documents.
    """
    if query_engine is None:
        raise HTTPException(status_code=503, detail="Service Unavailable: Query Engine is not initialized.")

    try:
        # 1. Use the engine to get results
        retrieved_docs = query_engine.retrieve_similar(
            query=request.query,
            n_results=5  #standardize on 5 results
        )

        # 2. Format the response using our Pydantic model
        return QueryResponse(results=retrieved_docs)

    except ValueError as ve:
        print(f"Validation Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # General catch-all for unexpected errors
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")