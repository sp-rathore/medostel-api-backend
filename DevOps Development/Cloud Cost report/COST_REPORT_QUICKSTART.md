# Google Cloud Daily Cost Report - Quick Start Guide

## 📋 Overview

Automated daily cost reports sent to **shishupal.rathore@gmail.com** with breakdown by:
- **Project**: Total costs per GCP project  
- **Resources**: Top services/resources consuming costs within each project

---

## 🚀 Quick Setup (5 minutes)

### 1. Get Your Billing Account ID

```bash
gcloud billing accounts list
```

### 2. Get SendGrid API Key

Sign up at [SendGrid](https://sendgrid.com) and create an API key

### 3. Deploy

```bash
bash deploy_cost_report.sh
```

### 4. Verify

```bash
gcloud functions logs read cost-report-function --limit=50
```

---

## 📧 Email Report Features

✓ **Daily Summary**
  - Total cost across all projects
  - Cost per project with breakdown

✓ **Per-Project Details**  
  - Project name and ID
  - Daily cost
  - Top 5 resources by cost
  - Cost percentage breakdown

---

## ⏰ Schedule

Default: Daily at **8:00 AM IST** (2:30 AM UTC)

---

## 🧪 Test Setup

```bash
# Get function URL
gcloud functions describe cost-report-function --region=us-central1 --format='value(httpsTrigger.url)'

# Test it
curl -X POST <FUNCTION_URL>
```

---

## 🔧 Configuration

### Change Recipient Email:

```bash
gcloud functions deploy cost-report-function \
  --set-env-vars RECIPIENT_EMAIL=newemail@example.com
```

### Enable BigQuery for Real Data:

1. Enable Billing Export to BigQuery
2. Update function with dataset name
3. Function will use real billing data

---

## 📁 Files Included

- `cost_report_function.py` - Cloud Function code
- `requirements.txt` - Dependencies
- `deploy_cost_report.sh` - Deployment automation
- `cost_report_setup.md` - Detailed documentation
- `COST_REPORT_QUICKSTART.md` - This quick start

---

## ✅ Deployment Checklist

- [ ] Billing Account ID obtained
- [ ] SendGrid API key created
- [ ] Deployment script executed
- [ ] Cloud Function deployed
- [ ] Cloud Scheduler job created
- [ ] Test email received
- [ ] Schedule verified

---

See `cost_report_setup.md` for detailed documentation
