from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str

class DocumentResponse(BaseModel):
    content: str
    slug: Optional[str] = None
    published_at: Optional[str] = None
    similarity_score: float

class QueryResponse(BaseModel):
    query: str
    answer: str  # <--- NEW FIELD
    sources: List[DocumentResponse]