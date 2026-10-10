# Step-by-Step Deployment Procedure: Ritucast Agricultural Intelligence Platform

## 1. Overview

This document provides the standard operating procedure (SOP) for deploying Ritucast to staging and production environments on Google Cloud Run.

---

## 2. Prerequisites & Access Requirements

Before initiating a deployment, the operator must have:
1. Google Cloud SDK (`gcloud` CLI) installed and authenticated:
   ```bash
   gcloud auth login
   ```
2. Docker CLI installed and running locally.
3. IAM Permissions on the target GCP Project:
   - `roles/run.admin` (Cloud Run Administrator)
   - `roles/artifactregistry.admin` (Artifact Registry Administrator)
   - `roles/iam.serviceAccountUser` (Service Account User)

---

## 3. Automated Deployment via `deploy.sh`

The primary deployment method is the executable script `deploy/cloudrun/deploy.sh`:

```bash
# 1. Export configuration variables
export GCP_PROJECT_ID="ritucast-prod"
export GCP_REGION="asia-south1"

# 2. Run automated deployment script
./deploy/cloudrun/deploy.sh
```

### Script Execution Sequence
The script automatically executes:
1. Google Cloud authentication check.
2. Enabling required APIs (`run.googleapis.com`, `artifactregistry.googleapis.com`).
3. Creating Artifact Registry Docker repository `ritucast` if absent.
4. Building and pushing the backend container image with git SHA tag.
5. Deploying `ritucast-backend` to Cloud Run and capturing its production URL.
6. Building and pushing the frontend container image with the backend URL baked in.
7. Deploying `ritucast-frontend` to Cloud Run and capturing its production URL.
8. Updating backend CORS origins to include the newly deployed frontend URL.
9. Executing automated post-deployment smoke tests (`/health` probes).

---

## 4. Manual Step-by-Step Deployment (Fallback)

If scripted execution is unavailable, execute the steps manually:

```bash
# Step 1: Configure project
gcloud config set project $GCP_PROJECT_ID

# Step 2: Build & Push Backend
docker build -t asia-south1-docker.pkg.dev/$GCP_PROJECT_ID/ritucast/backend:latest -f deploy/docker/Dockerfile.backend .
docker push asia-south1-docker.pkg.dev/$GCP_PROJECT_ID/ritucast/backend:latest

# Step 3: Deploy Backend
gcloud run deploy ritucast-backend \
  --image=asia-south1-docker.pkg.dev/$GCP_PROJECT_ID/ritucast/backend:latest \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1024Mi

# Step 4: Capture backend URL and build frontend
BACKEND_URL=$(gcloud run services describe ritucast-backend --region=asia-south1 --format='value(status.url)')
docker build --build-arg VITE_API_BASE_URL="$BACKEND_URL" -t asia-south1-docker.pkg.dev/$GCP_PROJECT_ID/ritucast/frontend:latest -f deploy/docker/Dockerfile.frontend .
docker push asia-south1-docker.pkg.dev/$GCP_PROJECT_ID/ritucast/frontend:latest

# Step 5: Deploy Frontend
gcloud run deploy ritucast-frontend \
  --image=asia-south1-docker.pkg.dev/$GCP_PROJECT_ID/ritucast/frontend:latest \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=256Mi
```
