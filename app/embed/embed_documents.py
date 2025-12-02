from typing import List, Dict
from app.config_loader import load_config
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from ut1ls.logger import setup_logging
import json
from app.ingest.text_spllitter import split_article_content

logger = setup_logging()

class Embedder:
    """Handles embedding of articles and storing them in ChromaDB."""

    def __init__(self):
        cfg = load_config()

        self.persist_directory: str = cfg.database["chroma_persist_dir"]
        self.collection_name: str = cfg.database["chroma_collection_name"]
        self.model_name = cfg.embedding["model_name"]

        # Initialize Client
        self.client = chromadb.PersistentClient(path=self.persist_directory)

        # Explicitly define the embedding function
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.model_name
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def load_articles_from_json(self, filename="processed_articles.json"):
        """Load parsed articles from the processed directory."""
        cfg = load_config()
        # Resolve path relative to this file
        base_dir = Path(__file__).resolve().parents[2]
        processed_dir = base_dir / Path(cfg.paths["processed_data_dir"])
        filepath = processed_dir / filename

        if not filepath.exists():
            # Fallback for Docker environments where paths might be flattened
            fallback_path = Path("/app/data/processed") / filename
            if fallback_path.exists():
                filepath = fallback_path
            else:
                raise FileNotFoundError(f"❌ File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            articles = json.load(f)

        logger.info(f"📂 Loaded {len(articles)} articles from {filepath}")
        return articles

    def embed_and_store(self, articles: List[Dict]):
        """Embed articles and store them in ChromaDB."""
        if not articles:
            logger.warning("No articles provided...")
            raise ValueError("No articles provided to embed and store.")

        # --- USE CHUNKING LOGIC ---
        chunks = split_article_content(articles)

        ids = [str(chunk["id"]) for chunk in chunks]
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [
            {"slug": chunk["slug"], "published_at": chunk["published_at"], "parent_id": chunk["original_id"]}
            for chunk in chunks
        ]

        logger.info(f"Adding {len(documents)} chunks to collection...")

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        logger.info(f"Successfully embedded and stored {len(documents)} chunks...")