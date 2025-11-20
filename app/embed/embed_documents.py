from typing import List, Dict
from app.config_loader import load_config
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from ut1ls.logger import setup_logging
logger = setup_logging()
import json
from app.ingest.text_spllitter import split_article_content

class Embedder:
    """Handles embedding of articles and storing them in ChromaDB."""

    def __init__(self):
        cfg = load_config()

        # Initialize Chroma client with persistence
        self.persist_directory: str = cfg.database["chroma_persist_dir"]
        self.collection_name: str = cfg.database["chroma_collection_name"]

        base_directory = Path(__file__).resolve().parents[2]
        directory_path = base_directory/self.persist_directory
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name)

        self.model_name_for_function: str = cfg.embedding["model_name"]

        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.model_name_for_function
            ),
        )

    def load_articles_from_json(self, filename="processed_articles.json"):
        """Load parsed articles from the processed directory."""
        cfg = load_config()
        base_dir= Path(__file__).resolve().parents[2]
        processed_dir = Path(cfg.paths["processed_data_dir"])
        processed_dir = base_dir/processed_dir
        filepath = processed_dir / filename

        if not filepath.exists():
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


        chunks = split_article_content(articles)

        ids = [str(chunk["id"]) for chunk in chunks]
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [
            {"slug": chunk["slug"], "published_at": chunk["published_at"], "parent_id": chunk["original_id"]}
            for chunk in chunks
        ]

        logger.info(f"Adding {len(documents)} chunks to collection...")


        return articles

    def embed_and_store(self, articles: List[Dict]):
        """Embed articles and store them in ChromaDB."""
        if not articles:
            raise ValueError("No articles provided to embed and store.")

        ids = [str(article["id"]) for article in articles]
        documents = [article["content"] for article in articles]
        metadatas = [
            {"slug": article["slug"], "published_at": article["published_at"]}
            for article in articles
        ]


        # Store in Chroma

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )


        logger.info(f"Successfully embedded and stored {len(documents)} chunks...")
