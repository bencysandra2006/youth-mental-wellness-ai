#!/usr/bin/env bash
set -euo pipefail

GCP_PROJECT_ID=${GCP_PROJECT_ID:?set}
REGION=${GCP_REGION:-asia-south1}
SERVICE=${SERVICE_NAME:-youth-wellness-ai}

gcloud config set project "$GCP_PROJECT_ID"
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$SERVICE
gcloud run deploy $SERVICE \
  --image gcr.io/$GCP_PROJECT_ID/$SERVICE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=$GCP_PROJECT_ID,GCP_LOCATION=$REGION,USE_FIRESTORE=false
