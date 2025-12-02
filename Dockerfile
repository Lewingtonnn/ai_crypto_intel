# Dockerfile

# Stage 1: Build Environment - Use a base Python image
FROM python:3.11-slim AS builder

# Set environment variables for non-interactive Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Application Runner - The final, smaller image
FROM python:3.11-slim

# Set working directory again
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

COPY app ./app
COPY configs ./configs
COPY ut1ls ./ut1ls
COPY run_pipeline.py .
COPY run_api.py .
COPY .env .
COPY data/processed ./data/processed

RUN python run_pipeline.py

# Expose the application port (8000 from config.yaml)
EXPOSE 8000

# Set the entry point to run the API
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]