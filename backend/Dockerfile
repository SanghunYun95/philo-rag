FROM python:3.12-slim

# Set environment variables (using key=value format to avoid legacy warnings)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-privileged user first so we can use it for directory ownership
RUN adduser --disabled-password --gecos "" appuser

# Setup model cache directory with proper ownership for pre-loading (restrictive permissions)
RUN mkdir -p /app/model_cache && \
    chown -R appuser:appuser /app && \
    chmod 755 /app/model_cache

ENV HF_HOME=/app/model_cache

# Pre-load the embedding model to reduce cold start latency
RUN python -c "from langchain_huggingface import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})"

# Switch to non-privileged user
USER appuser

# Expose the port
EXPOSE 8080

# Command to run the application (0.0.0.0 for Cloud Run)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
