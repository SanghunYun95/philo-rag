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
RUN adduser --disabled-password --gecos "" appuser && \
    mkdir -p /app/model_cache

# Copy source code and fix permissions
COPY . .
RUN chown -R appuser:appuser /app && \
    chmod 755 /app/model_cache

ENV HF_HOME=/app/model_cache

# Switch to non-privileged user BEFORE pre-loading models
# This ensures a consistent environment (permissions) between build-time pre-loading and runtime
USER appuser

# Pre-load the embedding model to reduce cold start latency
# This runs as 'appuser', matching the runtime environment
RUN python -c "from langchain_huggingface import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})"

# Expose the port (Cloud Run defaults to 8080, but can be overridden by $PORT)
EXPOSE 8080

# Command to run the application using the PORT environment variable with exec form
# We use exec to ensure uvicorn becomes the PID 1 process and handles termination signals properly
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers --forwarded-allow-ips='130.211.0.0/22,35.191.0.0/16'"]
