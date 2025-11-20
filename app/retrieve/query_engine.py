from app.config_loader import load_config
import chromadb
from chromadb.utils import embedding_functions
from chromadb import PersistentClient
from typing import List, Dict

from pathlib import Path




class QueryEngine:
    """Handles semantic retrieval from ChromaDB."""

    def __init__(self):
        cfg = load_config()
        self.persist_directory: str = cfg.database["chroma_persist_dir"]
        self.collection_name: str = cfg.database["chroma_collection_name"]
        self.model_name_for_function : str = cfg.embedding["model_name"]

        self.client = PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.model_name_for_function
            ),
        )

    def retrieve_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """Retrieve the most semantically similar documents."""
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        # Clean and format results
        formatted_results = []
        for doc, meta, score in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            formatted_results.append({
                "content": doc,
                "slug": meta.get("slug"),
                "published_at": meta.get("published_at"),
                "similarity_score": 1 - score  # Chroma returns distance, convert to similarity
            })

        return formatted_results
