from typing import List, Dict
from app.config_loader import load_config
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions



class Embedder:
    """Handles embedding of articles and storing them in ChromaDB."""

    def __init__(self):
        cfg = load_config()
        self.model_name: str = cfg.embedding["model_name"]
        self.model = SentenceTransformer(self.model_name)
        self.persist_directory: str = cfg.database["chroma_persist_dir"]
        self.collection_name: str = cfg.database["chroma_collection_name"]
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.model_name
            ),
        )


    def embed_and_store(self, articles: List[Dict]):
        """Embed articles and store them in ChromaDB."""
        if not articles:
            raise ValueError("No articles provided to embed and store.")
        ids, documents, metadatas = [], [], []
        for article in articles:
            ids.append(article["id"])
            documents.append(article["content"])
            metadatas.append({
                "slug": article["slug"],
                "published_at": article["published_at"],
            })

            embeddings = self.model.encode(documents, show_progress_bar=True)
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings.tolist()
            )
            print(f"✅ Successfully embedded and stored {len(documents)} articles in collection '{self.collection_name}'.")



        pass
