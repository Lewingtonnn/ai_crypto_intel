from app.ingest.ingest_articles import NewsIngestor
from app.embed.embed_documents import Embedder
from chromadb import Client
from app.config_loader import load_config
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

    # Step 2: Load from processed JSON
    print("embedding began")
    embedder = Embedder()
    loaded_articles = embedder.load_articles_from_json()

    # Step 3: Embed and store in Chroma
    embedder.embed_and_store(loaded_articles)

    print("🚀 Pipeline completed successfully.")
    cfg = load_config()
    from chromadb import PersistentClient
    client = PersistentClient(path=cfg.database["chroma_persist_dir"])
    collection = client.get_or_create_collection(cfg.database["chroma_collection_name"])
    print(f"collection count : {collection.count()}")
    print("embedding function:", collection._embedding_function)
if __name__ == "__main__":
    main()
# import shutil
# from app.config_loader import load_config
#
# cfg = load_config()
# persist_dir = cfg.database["chroma_persist_dir"]
#
# shutil.rmtree(persist_dir, ignore_errors=True)
# print(f"✅ Deleted old persistent folder at {persist_dir}")
#
# from sentence_transformers import SentenceTransformer
#
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model = SentenceTransformer(model_name)  # this must succeed without timeout
# print("✅ SentenceTransformer loaded successfully")
#
# import chromadb
# from chromadb.utils import embedding_functions
#
# client = chromadb.PersistentClient(path=persist_dir)
#
# collection = client.create_collection(
#     name="crypto_articles",
#     embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name=model_name
#     ),
# )
# print("✅ Collection created with SentenceTransformerEmbeddingFunction")
