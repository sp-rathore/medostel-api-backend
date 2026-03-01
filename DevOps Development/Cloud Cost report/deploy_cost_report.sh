#!/bin/bash

# Google Cloud Daily Cost Report Deployment Script

set -e

PROJECT_ID="gen-lang-client-0064186167"
REGION="us-central1"
SERVICE_ACCOUNT="cost-report-sa"
FUNCTION_NAME="cost-report-function"
SCHEDULER_JOB="cost-report-job"
RECIPIENT_EMAIL="shishupal.rathore@gmail.com"

echo "=================================="
echo "Google Cloud Cost Report Setup"
echo "=================================="
echo ""

# Enable APIs
echo "Enabling required APIs..."
gcloud services enable cloudbilling.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudfunctions.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudscheduler.googleapis.com --project=$PROJECT_ID
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID
echo "✓ APIs enabled"

# Create service account
echo ""
echo "Creating service account..."
gcloud iam service-accounts create $SERVICE_ACCOUNT \
    --display-name="Cost Report Service Account" \
    --project=$PROJECT_ID 2>/dev/null || echo "✓ Service account already exists"

# Grant permissions
echo "Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --role=roles/billing.viewer --quiet 2>/dev/null || true

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --role=roles/logging.logWriter --quiet 2>/dev/null || true

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor --quiet 2>/dev/null || true

echo "✓ Permissions granted"

# Store SendGrid API Key
echo ""
echo "Enter your SendGrid API key (press Enter to skip):"
read -s SENDGRID_API_KEY

if [ ! -z "$SENDGRID_API_KEY" ]; then
    echo -n "$SENDGRID_API_KEY" | gcloud secrets create sendgrid-api-key \
        --data-file=- --project=$PROJECT_ID 2>/dev/null || \
    echo "$SENDGRID_API_KEY" | gcloud secrets versions add sendgrid-api-key \
        --data-file=- --project=$PROJECT_ID 2>/dev/null
    
    echo "✓ SendGrid API key stored"
fi

# Deploy Cloud Function
echo ""
echo "Deploying Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point=generate_cost_report \
    --service-account=${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --memory=512MB \
    --timeout=540s \
    --source=. \
    --region=$REGION \
    --set-env-vars RECIPIENT_EMAIL=$RECIPIENT_EMAIL,SENDGRID_API_KEY_SECRET=sendgrid-api-key,GCP_PROJECT=$PROJECT_ID \
    --project=$PROJECT_ID

echo "✓ Cloud Function deployed"

# Get function URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --project=$PROJECT_ID --format='value(httpsTrigger.url)')
echo "Function URL: $FUNCTION_URL"

# Create Cloud Scheduler job
echo ""
echo "Creating Cloud Scheduler job..."
gcloud scheduler jobs delete $SCHEDULER_JOB --location=$REGION --project=$PROJECT_ID --quiet 2>/dev/null || true

gcloud scheduler jobs create http $SCHEDULER_JOB \
    --schedule="30 2 * * *" \
    --time-zone="UTC" \
    --uri=$FUNCTION_URL \
    --http-method=POST \
    --location=$REGION \
    --project=$PROJECT_ID \
    --message-body='{}'

echo "✓ Cloud Scheduler job created"
echo ""
echo "Setup Complete!"
echo "Daily reports will be sent at 8:00 AM IST"
