# app/api/models.py
from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    """
    The request model for a user's query.
    """
    query: str

class DocumentResponse(BaseModel):
    """
    The model for a single retrieved document.
    This must match the dictionary structure from your QueryEngine.
    """
    content: str
    slug: Optional[str] = None
    published_at: Optional[str] = None
    similarity_score: float

class QueryResponse(BaseModel):
    """
    The final response model containing all retrieved documents.
    """
    results: List[DocumentResponse]