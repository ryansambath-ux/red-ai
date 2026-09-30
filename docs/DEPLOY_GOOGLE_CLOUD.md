# Google Cloud deployment

Red is ready for Cloud Run deployment but cloud account authorization must be completed by the account owner.

Required GitHub repository secrets:
- GCP_PROJECT_ID
- GCP_REGION
- GCP_WORKLOAD_IDENTITY_PROVIDER
- GCP_SERVICE_ACCOUNT

Recommended production secrets stored in Google Secret Manager:
- AI_API_KEY
- RED_DEVICE_SECRET

Create an Artifact Registry repository named `red`, configure GitHub Workload Identity Federation, grant the deployment service account only the required Artifact Registry and Cloud Run permissions, then run the **Deploy Red to Cloud Run** GitHub Action.

Do not place service-account JSON keys in this repository.
