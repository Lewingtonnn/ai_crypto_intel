from typing import List, Dict
from app.config_loader import load_config

class Embedder:
    """Handles embedding of articles and storing them in ChromaDB."""

    def __init__(self):
        cfg = load_config()
        self.model_name: str = cfg["embedding"]["model_name"]
        self.persist_directory: str = cfg["database"]["chroma_persist_dir"]
        self.collection_name: str = "crypto_articles"

        # TODO: initialize embedding model
        # TODO: initialize ChromaDB client and collection

    def embed_and_store(self, articles: List[Dict]):
        """
        Convert article contents to embeddings and store them in ChromaDB.

        Each article dict should contain:
        - id
        - title
        - slug
        - description
        - published_at
        - content (text to embed)
        """
        pass
