import shutil
from app.config_loader import load_config

cfg = load_config()
persist_dir = cfg.database["chroma_persist_dir"]

shutil.rmtree(persist_dir, ignore_errors=True)
print(f"✅ Deleted old persistent folder at {persist_dir}")

from sentence_transformers import SentenceTransformer

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)  # this must succeed without timeout
print("✅ SentenceTransformer loaded successfully")

import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path=persist_dir)

collection = client.create_collection(
    name="crypto_articles",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name
    ),
)
print("✅ Collection created with SentenceTransformerEmbeddingFunction")
