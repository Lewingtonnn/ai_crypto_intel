# app/api/main.py

from fastapi import FastAPI, HTTPException
from app.api.models import QueryRequest, QueryResponse, DocumentResponse
from app.retrieve.query_engine import QueryEngine
from app.generation.generation_client import LLMEngine
from ut1ls.logger import setup_logging
logger = setup_logging()

app = FastAPI(title="AI-Enhanced Crypto Intelligence API", version="1.0.0")

# --- Global Objects ---
query_engine = None
llm_engine = None


@app.on_event("startup")
async def startup_event():
    global query_engine, llm_engine
    try:
        query_engine = QueryEngine()
        logger.info("✅ QueryEngine loaded.")

        # Initialize LLM Engine
        llm_engine = LLMEngine()
        print("✅ LLMEngine loaded.")

    except Exception as e:
        logger.warning(f"❌ FATAL: {e}")


@app.post("/api/v1/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    if not query_engine or not llm_engine:
        raise HTTPException(status_code=503, detail="System not initialized")

    try:

        retrieved_docs = query_engine.retrieve_similar(request.query, n_results=5)

        answer = llm_engine.generate_answer(request.query, retrieved_docs)

        return QueryResponse(
            query=request.query,
            answer=answer,
            sources=[
                DocumentResponse(
                    content=doc['content'],
                    slug=doc.get('slug'),
                    published_at=doc.get('published_at'),
                    similarity_score=doc['similarity_score']
                ) for doc in retrieved_docs
            ]
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))