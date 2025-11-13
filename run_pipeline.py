from app.ingest.ingest_articles import NewsIngestor
from app.embed.embed_documents import Embedder
import os
import dotenv

dotenv.load_dotenv()

def main():
    source_url = os.getenv("API_URL")
    if not source_url:
        raise ValueError("Missing API_URL environment variable.")

    # Step 1: Ingest and save
    print("ingestion started")
    ingestor = NewsIngestor(source_url)
    print('ingestion done, saving articles beginning')
    articles = ingestor.run()
    print('articles collected and saved')

    if not articles:
        print("❌ No articles fetched. Exiting.")
        return

    # Step 2: Load from processed JSON (optional step if you're chaining modules)
    print("embedding began")
    embedder = Embedder()
    loaded_articles = embedder.load_articles_from_json()

    # Step 3: Embed and store in Chroma
    embedder.embed_and_store(loaded_articles)

    print("🚀 Pipeline completed successfully.")

if __name__ == "__main__":
    main()
