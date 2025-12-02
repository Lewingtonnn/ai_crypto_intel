# AI-Enhanced Crypto Intelligence Pipeline (RAG)

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)](https://www.docker.com)
[![Google Cloud Run](https://img.shields.io/badge/GCP-Cloud%20Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)](https://python.langchain.com)

## 🚀 Live Demo

**API Endpoint:** [https://crypto-rag-api-351995124578.us-central1.run.app/docs](https://crypto-rag-api-351995124578.us-central1.run.app/docs)

---

## 📖 Project Overview

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** pipeline designed to ingest cryptocurrency news, store them in a vector database, and answer user queries using a locally-hosted Large Language Model (LLM). Unlike standard wrappers, this project implements a **self-contained AI architecture**. It runs the embedding model, vector store (ChromaDB), and generation model (Google Flan-T5) entirely within the application container, removing dependencies on unstable external APIs.

### Key Engineering Features

* **Full-Stack ETL Pipeline:** Ingests raw text, chunks data intelligently, embeds using `sentence-transformers`, and stores in a persistent vector database.
* **Self-Contained Inference:** Runs `google/flan-t5-small` locally on CPU, ensuring zero external API costs and high resilience.
* **Lazy Loading Architecture:** Implemented a lazy-load pattern for heavy AI models to solve "Cold Start" timeouts in serverless environments (Cloud Run).
* **Dockerized & Cloud-Native:** Fully containerized with a multi-stage Docker build, optimized for deployment on Google Cloud Run with 4GB RAM configuration.

---

## 🏗️ Architecture

```
[User Query] --> [FastAPI Endpoint]
                        |
                        v
                [Query Embedding]
                        |
                        v
    [ChromaDB (Vector Store)] --> (Retrieve Top-k Chunks) --> [Prompt Construction]
                        |
                        v
                [Local LLM (Flan-T5)]
                        |
                        v
                [Synthesized Answer]
```

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Framework:** FastAPI (REST API), Pydantic (Data Validation)
- **Orchestration:** LangChain (Chain Management)
- **Database:** ChromaDB (Local Vector Store)
- **ML Models:**
  - **Embedding:** sentence-transformers/all-MiniLM-L6-v2
  - **Generation:** google/flan-t5-small (Hugging Face Pipeline)
- **Infrastructure:** Docker, Google Cloud Run

---

## ⚡ Setup & Installation

### Prerequisites

- Python 3.10+
- Docker (optional, for containerization)

### 1. Local Setup

```bash
# Clone the repository
git clone https://github.com/lewingtonnn/ai-crypto-intel.git
cd ai-crypto-intel

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Ingestion Pipeline (Builds the DB)
python run_pipeline.py

# Start the API Server
python run_api.py
```

### 2. Docker Setup

```bash
# Build the image (This runs ingestion inside the container)
docker build -t crypto-rag-api .

# Run the container
docker run -p 8080:8080 crypto-rag-api
```

---

## 🔌 API Usage

**Endpoint:** `/api/v1/query` (POST)

Accepts a natural language question and returns a synthesized answer with sources.

### Request:

```json
{
  "query": "What is the latest news regarding Ethereum gas fees?"
}
```

### Response:

```json
{
  "query": "What is the latest news regarding Ethereum gas fees?",
  "answer": "Ethereum's 'Dencun' upgrade is expected to significantly lower gas fees for Layer 2 networks...",
  "sources": [
    {
      "content": "...",
      "slug": "ethereum-dencun-upgrade",
      "similarity_score": 0.45
    }
  ]
}
```

---

## 🧠 Challenges & Solutions

### 1. The "Zombie Database" Conflict

**Problem:** Cloud builds were accidentally including old, incompatible local database files, causing ChromaDB to crash on startup due to hash collisions.

**Solution:** Implemented a "Scorched Earth" policy in the Dockerfile. We explicitly `COPY` source data but `RUN rm -rf` on any database directories before the ingestion step, guaranteeing a fresh, conflict-free build every time.

### 2. Serverless Cold Starts (Memory Overload)

**Problem:** Loading both the Embedding Model and the LLM at container startup caused Cloud Run to time out (OOM) before the health check passed.

**Solution:** Refactored the `LLMEngine` to use **Lazy Loading**. The heavy T5 model initializes only upon the first API request. This reduced startup time from >2 minutes to <5 seconds.

---

## 🔮 Future Roadmap

- [ ] **Frontend:** Build a Streamlit dashboard for visual interaction.
- [ ] **Model Upgrade:** Swap T5-Small for a quantized Llama-3 model (requires GPU).
- [ ] **Hybrid Search:** Implement keyword search alongside vector search for better accuracy.

---

## 👨‍💻 Author

**Lewis Nganga Githua**  
Role: AI Data Engineer

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.