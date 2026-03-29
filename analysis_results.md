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
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers"]
```

### 2. Update `frontend/firebase.json`
- **Updated `site` ID**: Changed from the default project ID to `philo-rag` to deploy correctly to the `philo-rag.web.app` URL.

### 3. Update `backend/app/main.py`
- **Explicit CORS Origins**: Replaced the wildcard `["*"]` with an explicit list of origins. Browsers reject `*` when `allow_credentials=True` is used, so defining the specific Firebase and localhost URLs was necessary to fix the "Failed to fetch" errors.

## Next Steps
1. **Commit the changes**: The fixed `Dockerfile`, `main.py`, and `firebase.json` are now ready to be pushed to the repository.
2. **Re-run the GitHub Action**: When you merge the PR into the `main` branch, the GitHub Actions workflow is triggered.
3. **Verify the results**: 
   - Backend URL: Check readiness at `https://[SUBDOMAIN].a.run.app/ready`
   - Frontend URL: Check `https://philo-rag.web.app/`

> [!TIP]
> Once the deployment is successful, you can verify the status through the Cloud Run URL or the readiness check endpoint: `/ready`.
