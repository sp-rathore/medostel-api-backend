# Google Cloud Cost Report System

## 📋 Overview

Automated daily cost reports sent to **shishupal.rathore@gmail.com** containing:
- Total daily costs across all GCP projects
- Per-project cost breakdown
- Top services/resources by cost
- Cost percentage distribution

---

## 📁 Files in This Folder

### Core Files
- **`cost_report_function.py`** - Main Cloud Function that generates and sends reports
- **`requirements.txt`** - Python dependencies for the function
- **`deploy_cost_report.sh`** - Automated deployment script (executable)
- **`COST_REPORT_QUICKSTART.md`** - Quick start guide (5 minutes to setup)

---

## 🚀 Quick Start

### 1. Get SendGrid API Key
```bash
# Sign up at https://sendgrid.com (free: 100 emails/day)
# Create API key: Settings → API Keys → Create API Key
```

### 2. Deploy
```bash
# From this directory
bash deploy_cost_report.sh

# When prompted, paste your SendGrid API key
```

### 3. Test
```bash
# View logs
gcloud functions logs read cost-report-function --limit=50

# Or trigger manually
curl -X POST <FUNCTION_URL>
```

---

## ⏰ Schedule

**Default**: Daily at **8:00 AM IST** (2:30 AM UTC)

To change: Edit the cron schedule in `deploy_cost_report.sh`

---

## 📊 Email Report Format

```
Google Cloud Daily Cost Report
Date: 2026-02-28

Daily Summary
─────────────
Total Daily Cost: $96.22 USD
Projects: 3

Project: Medostel - AI Assistant
Daily Cost: $45.32
├─ Cloud SQL: $25.50 (56.3%)
├─ Compute Engine: $12.80 (28.2%)
├─ Cloud Storage: $4.20 (9.3%)
├─ Cloud Functions: $1.82 (4.0%)
└─ Cloud Monitoring: $0.50 (1.1%)

[Additional projects...]
```

---

## 🔧 Configuration

### Change Recipient Email
```bash
gcloud functions deploy cost-report-function \
  --set-env-vars RECIPIENT_EMAIL=newemail@example.com
```

### Change Schedule
Edit `deploy_cost_report.sh` line with cron expression:
```bash
--schedule="30 2 * * *"  # Current: 2:30 AM UTC (8:00 AM IST)
```

### Enable Real Billing Data
1. Enable Cloud Billing → BigQuery Export
2. Create dataset: `billing_dataset`
3. Update function environment:
```bash
gcloud functions deploy cost-report-function \
  --set-env-vars BILLING_DATASET=billing_dataset
```

---

## 💰 Cost

- Cloud Functions: FREE (under free tier)
- Cloud Scheduler: FREE (under free tier)  
- SendGrid: FREE (100 emails/day)
- **Total: ~$0.00/month**

---

## 🐛 Troubleshooting

### Email Not Arriving
```bash
# Check logs
gcloud functions logs read cost-report-function --limit=50

# View recent executions
gcloud scheduler jobs describe cost-report-job --location=us-central1
```

### Check Scheduler Job
```bash
gcloud scheduler jobs describe cost-report-job --location=us-central1 --format=json
```

### Manually Trigger Report
```bash
gcloud scheduler jobs run cost-report-job --location=us-central1
```

---

## 📞 Support

See `COST_REPORT_QUICKSTART.md` for detailed documentation

---

## ✅ Deployment Checklist

- [ ] SendGrid API key obtained
- [ ] Deployment script executed
- [ ] Cloud Function deployed successfully
- [ ] Cloud Scheduler job created
- [ ] First test email received
- [ ] Schedule time verified
- [ ] Email filtering configured (if needed)

---

**Last Updated**: 2026-02-28
**Location**: `/Users/shishupals/Documents/Claude/projects/Medostel/Development/DevOps Development/Cloud Cost report/`
