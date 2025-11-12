from typing import List, Dict
from app.config_loader import load_config
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions


class Embedder:
    """Handles embedding of articles and storing them in ChromaDB."""

    def __init__(self):
        cfg = load_config()
        self.model_name: str = cfg["embedding"]["model_name"]
        self.model = SentenceTransformer(self.model_name)
        self.persist_directory: str = cfg["database"]["chroma_persist_dir"]
        self.collection_name: str = cfg["database"]["chroma_collection_name"]
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.model_name
            ),
        )


    def embed_and_store(self, articles: List[Dict]):
        """Embed articles and store them in ChromaDB."""



        pass
