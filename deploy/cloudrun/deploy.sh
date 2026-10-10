#!/usr/bin/env bash
# ==============================================================================
# Ritucast Cloud Run Deployment Automation Script
# Phase 13: Deployment Architecture and Production Readiness
# ==============================================================================
# Usage:
#   export GCP_PROJECT_ID="your-gcp-project-id"
#   export GCP_REGION="asia-south1"
#   ./deploy/cloudrun/deploy.sh
# ==============================================================================

set -euo pipefail

# 1. Configuration & Pre-flight checks
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-asia-south1}"
REPO_NAME="ritucast"
IMAGE_TAG="$(git rev-parse --short HEAD 2>/dev/null || echo 'v1.0.0')"

if [[ -z "$PROJECT_ID" ]]; then
  echo "[-] ERROR: GCP_PROJECT_ID environment variable is required."
  echo "    Example: export GCP_PROJECT_ID='ritucast-prod' && ./deploy/cloudrun/deploy.sh"
  exit 1
fi

echo "[+] ======================================================================"
echo "[+] Starting Ritucast Production Deployment to Google Cloud Run"
echo "[+] Project ID: $PROJECT_ID | Region: $REGION | Tag: $IMAGE_TAG"
echo "[+] ======================================================================"

# 2. Verify gcloud authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
  echo "[-] ERROR: gcloud CLI is not authenticated. Please run 'gcloud auth login'."
  exit 1
fi

gcloud config set project "$PROJECT_ID" --quiet

# 3. Enable necessary Google Cloud APIs
echo "[+] Enabling required Cloud APIs (run, artifactregistry, cloudbuild)..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  iam.googleapis.com \
  --project="$PROJECT_ID"

# 4. Create Artifact Registry repository if not present
echo "[+] Ensuring Artifact Registry repository '$REPO_NAME' exists in $REGION..."
if ! gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Ritucast production container images" \
    --project="$PROJECT_ID"
fi

# Configure Docker credentials helper
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

BACKEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/backend:$IMAGE_TAG"
FRONTEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/frontend:$IMAGE_TAG"

# 5. Build and Push Backend Container
echo "[+] Building and pushing Ritucast Backend image: $BACKEND_IMAGE..."
docker build \
  -t "$BACKEND_IMAGE" \
  -t "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/backend:latest" \
  -f deploy/docker/Dockerfile.backend .
docker push "$BACKEND_IMAGE"
docker push "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/backend:latest"

# 6. Deploy Backend Service to Cloud Run
echo "[+] Deploying Ritucast Backend to Cloud Run..."
gcloud run deploy ritucast-backend \
  --image="$BACKEND_IMAGE" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --cpu=1 \
  --memory=1024Mi \
  --min-instances=0 \
  --max-instances=5 \
  --concurrency=80 \
  --timeout=60s \
  --set-env-vars="ENVIRONMENT=production,DEBUG=false,MAX_WEATHER_AGE_HOURS=36.0,DEFAULT_DANGER_LEVEL_M=8.25" \
  --project="$PROJECT_ID"

BACKEND_URL="$(gcloud run services describe ritucast-backend --region="$REGION" --format='value(status.url)' --project="$PROJECT_ID")"
echo "[+] Backend deployed successfully at: $BACKEND_URL"

# 7. Build and Push Frontend Container (with Backend URL)
echo "[+] Building and pushing Ritucast Frontend image: $FRONTEND_IMAGE..."
docker build \
  --build-arg VITE_API_BASE_URL="$BACKEND_URL" \
  -t "$FRONTEND_IMAGE" \
  -t "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/frontend:latest" \
  -f deploy/docker/Dockerfile.frontend .
docker push "$FRONTEND_IMAGE"
docker push "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/frontend:latest"

# 8. Deploy Frontend Service to Cloud Run
echo "[+] Deploying Ritucast Frontend to Cloud Run..."
gcloud run deploy ritucast-frontend \
  --image="$FRONTEND_IMAGE" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --cpu=1 \
  --memory=256Mi \
  --min-instances=0 \
  --max-instances=5 \
  --concurrency=80 \
  --timeout=30s \
  --project="$PROJECT_ID"

FRONTEND_URL="$(gcloud run services describe ritucast-frontend --region="$REGION" --format='value(status.url)' --project="$PROJECT_ID")"
echo "[+] Frontend deployed successfully at: $FRONTEND_URL"

# 9. Update Backend CORS to permit Frontend Origin
echo "[+] Updating backend CORS origins with frontend URL: $FRONTEND_URL..."
gcloud run services update ritucast-backend \
  --region="$REGION" \
  --update-env-vars="CORS_ORIGINS=[\"$FRONTEND_URL\"]" \
  --project="$PROJECT_ID"

# 10. Smoke Test Validation
echo "[+] Performing automated smoke test on live services..."
echo "    Probing backend health: $BACKEND_URL/health"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health")
if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "[-] WARNING: Backend health probe returned HTTP $HTTP_STATUS"
else
  echo "[+] Backend health probe: HTTP 200 OK"
fi

echo "    Probing frontend health: $FRONTEND_URL/health"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/health")
if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "[-] WARNING: Frontend health probe returned HTTP $HTTP_STATUS"
else
  echo "[+] Frontend health probe: HTTP 200 OK"
fi

echo "[+] ======================================================================"
echo "[+] Ritucast Deployment Complete!"
echo "[+] Frontend Application: $FRONTEND_URL"
echo "[+] Backend API:          $BACKEND_URL"
echo "[+] API Documentation:    $BACKEND_URL/docs"
echo "[+] ======================================================================"
