# Dockerfile

# Stage 1: Build Environment
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Application Runner
FROM python:3.11-slim

WORKDIR /app

# --- THE FIX ---
# 1. Copy the Python libraries (Code)
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
# 2. Copy the Python executables (Binaries like uvicorn) - THIS FIXES THE ERROR
COPY --from=builder /usr/local/bin/ /usr/local/bin/
# ----------------

# Copy application code
COPY app ./app
COPY configs ./configs
COPY ut1ls ./ut1ls
COPY run_pipeline.py .
COPY run_api.py .
COPY .env .

# Copy processed data so we can ingest it
COPY data/processed ./data/processed

# Force delete ANY existing database folders (Zombie DB protection)
RUN rm -rf /app/data/chroma_db /app/data/vector_store /app/chroma

# Build the Database Fresh
RUN python run_pipeline.py

EXPOSE 8080

# Explicitly call uvicorn with the full path just to be safe, though PATH should now work
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8080"]