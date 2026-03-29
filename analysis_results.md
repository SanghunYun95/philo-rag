# Cloud Run Deployment Troubleshooting Report

The deployment failure in Google Cloud Run was caused by the application failing to start and listen on the expected port (8080) within the allocated timeout. 

## Root Cause Analysis

After investigating the `backend/Dockerfile`, I identified that the **source code was not being copied into the container**. The `Dockerfile` only included `COPY requirements.txt .`, which resulted in a container with all dependencies installed but missing the `app` directory and its logic. Consequently, `uvicorn` was unable to find `app.main:app`, causing the container to crash immediately or fail to bind to the port.

## Changes Applied

### 1. Update `backend/Dockerfile`
I modified the `Dockerfile` to include the following improvements:
- **Added `COPY . .`**: Ensured that the backend source code is properly included in the image.
- **Fixed Permissions**: Added a `chown` command to ensure the non-privileged `appuser` owns the application directory, preventing permission errors during runtime.
- **Improved Port Handling**: Updated the `CMD` to use the `${PORT}` environment variable provided by Cloud Run, with a fallback to `8080`.

```dockerfile
# ... after pip install ...

# Copy source code and fix permissions
COPY . .
RUN chown -R appuser:appuser /app && \
    chmod 755 /app/model_cache

# ...

# Command to run the application using the PORT environment variable
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers"]
```

## Next Steps
1. **Commit the changes**: The fixed `Dockerfile` is now ready to be pushed to the repository.
2. **Re-run the GitHub Action**: Pushing these changes to the `main` branch will trigger a new deployment.

> [!TIP]
> Once the deployment is successful, you can verify the status through the Cloud Run URL or the readiness check endpoint: `/ready`.
