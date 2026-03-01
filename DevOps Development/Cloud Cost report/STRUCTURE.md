# Cloud Cost Report Folder Structure

```
📁 Cloud Cost report/
├── 📄 README.md                          # Main documentation
├── 📄 COST_REPORT_QUICKSTART.md         # Quick start guide
├── 🐍 cost_report_function.py           # Cloud Function code
├── 📋 requirements.txt                  # Python dependencies
├── 🚀 deploy_cost_report.sh            # Deployment script
├── ⚙️  config.example.env              # Configuration template
└── 📋 STRUCTURE.md                      # This file
```

## File Descriptions

### Documentation
- **README.md** - Overview and getting started
- **COST_REPORT_QUICKSTART.md** - 5-minute setup guide
- **STRUCTURE.md** - This file

### Code & Configuration
- **cost_report_function.py** - Python Cloud Function
  - Fetches billing data
  - Formats HTML reports
  - Sends emails via SendGrid
  
- **requirements.txt** - Dependencies
  - functions-framework
  - google-cloud-billing
  - google-cloud-bigquery
  - google-cloud-secret-manager
  - requests

- **deploy_cost_report.sh** - Automation script
  - Enables APIs
  - Creates service account
  - Deploys Cloud Function
  - Creates Cloud Scheduler job

- **config.example.env** - Configuration template
  - Copy to config.env
  - Fill in your values
  - Used by deployment script

## Deployment Flow

```
1. Review README.md
        ↓
2. Get SendGrid API key
        ↓
3. Run deploy_cost_report.sh
        ↓
4. Deployment script:
   ├─ Enables required APIs
   ├─ Creates service account
   ├─ Stores secrets
   ├─ Deploys Cloud Function
   └─ Creates Cloud Scheduler job
        ↓
5. Daily reports start arriving
```

## Usage

### First Time Setup
```bash
bash deploy_cost_report.sh
```

### Test Report
```bash
gcloud scheduler jobs run cost-report-job --location=us-central1
```

### View Logs
```bash
gcloud functions logs read cost-report-function --limit=50
```

### Update Configuration
```bash
gcloud functions deploy cost-report-function \
  --set-env-vars <KEY>=<VALUE>
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `RECIPIENT_EMAIL` | shishupal.rathore@gmail.com | Email recipient |
| `SENDGRID_API_KEY_SECRET` | sendgrid-api-key | Secret Manager key |
| `GCP_PROJECT` | gen-lang-client-0064186167 | GCP Project ID |
| `BILLING_DATASET` | (optional) | BigQuery dataset for real data |

## Related Folders

Parent structure:
```
📁 Medostel/
└── 📁 Development/
    └── 📁 DevOps Development/
        ├── 📁 Cloud Cost report/     ← YOU ARE HERE
        ├── 📄 API_ACCESS_GUIDE.md
        ├── 📄 CREDENTIALS.md
        ├── 📄 ROLES_SUMMARY.md
        └── 📄 complete_setup.sql
```

