from app.ingest.ingest_articles import NewsIngestor
from app.embed.embed_documents import Embedder
from chromadb import Client
from app.config_loader import load_config
import os
import dotenv
from ut1ls.logger import setup_logging
logger = setup_logging()

dotenv.load_dotenv()

def main():
    source_url = os.getenv("API_URL")
    if not source_url:
        raise ValueError("Missing API_URL environment variable.")

    # Step 1: Ingest and save
    logger.info("ingestion started")
    ingestor = NewsIngestor(source_url)
    logger.info('ingestion done, saving articles beginning')
    articles = ingestor.run()
    logger.info('articles collected and saved')
    
    if not articles:
        logger.warning("❌ No articles fetched. Exiting.")
        return

    # Step 2: Load from processed JSON
    logger.info("embedding began")
    embedder = Embedder()
    loaded_articles = embedder.load_articles_from_json()

    # Step 3: Embed and store in Chroma
    embedder.embed_and_store(loaded_articles)

    logger.info("🚀 Pipeline completed successfully.")
    cfg = load_config()
    from chromadb import PersistentClient
    client = PersistentClient(path=cfg.database["chroma_persist_dir"])
    collection = client.get_or_create_collection(cfg.database["chroma_collection_name"])
    logger.info(f"collection count : {collection.count()}")
    logger.info(f"embedding function:{collection._embedding_function}")


if __name__ == "__main__":
        main()
