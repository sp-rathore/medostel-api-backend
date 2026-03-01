# Database Table Deployment Guide

## Overview

This guide provides step-by-step instructions to create the 6 core tables in the Medostel PostgreSQL database.

**Database**: Medostel
**Engine**: PostgreSQL 18
**Instance**: medostel-ai-assistant-pgdev-instance
**Project**: gen-lang-client-0064186167

---

## Prerequisites

Before deploying tables, ensure:

1. ✅ Cloud SQL instance is RUNNABLE
2. ✅ Database users are created (medostel_admin_user, medostel_api_user)
3. ✅ Cloud SQL Proxy is installed
4. ✅ psql or compatible client is available

---

## Step 1: Create Database Users (If Not Already Done)

Execute the `complete_setup.sql` script to create users:

```bash
cd /Users/shishupals/Documents/Claude/projects/Medostel/Development/DevOps\ Development

# Start Cloud SQL Proxy in background
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

# Wait for proxy to start
sleep 3

# Connect and execute setup
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=postgres \
  --project=gen-lang-client-0064186167 \
  --database=Medostel < complete_setup.sql
```

Expected Output:
```
✓ Roles created
✓ Users created with passwords
✓ Permissions configured
```

---

## Step 2: Create Tables

After users are created, execute the table creation script:

```bash
cd /Users/shishupals/Documents/Claude/projects/Medostel/Development/DevOps\ Development/DBA

# Start Cloud SQL Proxy
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

# Wait for proxy
sleep 3

# Connect as admin user
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user \
  --project=gen-lang-client-0064186167 \
  --database=Medostel < create_tables.sql
```

---

## Step 3: Verify Tables Created

Check that all tables were created:

```bash
# Start proxy
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

sleep 3

# Connect and list tables
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user \
  --project=gen-lang-client-0064186167 \
  --database=Medostel

# In the psql prompt, run:
\dt
\di
```

Expected Tables:
- [ ] User_Role_Master
- [ ] State_City_PinCode_Master
- [ ] User_Master
- [ ] User_Login
- [ ] New_User_Request
- [ ] Report_History

---

## Tables Created

### 1. **User_Role_Master** (6 columns)
- roleId (PK), roleName, status, createdDate, updatedDate, comments

### 2. **State_City_PinCode_Master** (9 columns)
- id (PK), stateId, stateName, cityName, cityId, pinCode, countryName, status, timestamps

### 3. **User_Master** (14 columns)
- userId (PK), firstName, lastName, currentRole, organisation, emailId, mobileNumber, address, location, status, timestamps

### 4. **User_Login** (10 columns)
- userId (PK/FK), username, passwordHash, mobilePhone, roleId, isActive, login timestamps

### 5. **New_User_Request** (15 columns)
- requestId (PK), user details, currentRole, requestStatus, timestamps, approvalDetails

### 6. **Report_History** (11 columns)
- id (PK), userId (FK), timestamp, fileName, fileType, reportType, diagnosis, pdfUrl, jsonData, status

---

## Indexes Created

### Performance Indexes
- User_Role_Master: idx_user_role_name, idx_user_role_status
- State_City_PinCode_Master: idx_state_name, idx_city_name, idx_pincode, idx_state_city
- User_Master: idx_user_email, idx_user_mobile, idx_user_role, idx_user_status, idx_user_created_date
- User_Login: idx_login_username, idx_login_role_id, idx_login_active, idx_login_last_login
- New_User_Request: idx_new_user_email, idx_new_user_status, idx_new_user_created
- Report_History: idx_report_user_id, idx_report_timestamp, idx_report_type, idx_report_status, idx_report_created

---

## Files Included

| File | Purpose |
|------|---------|
| `Databasespecs.md` | Database specification document |
| `create_tables.sql` | SQL script to create all 6 tables |
| `DEPLOYMENT_GUIDE.md` | This deployment guide |
| `Tables.md` | (To be created) Documentation of table structures |

---

## Troubleshooting

### Cloud SQL Proxy Not Found
```bash
# Reinstall proxy
gcloud components install cloud-sql-proxy
```

### Connection Refused
- Ensure instance is RUNNABLE: `gcloud sql instances list`
- Ensure proxy is running on port 5432
- Check firewall rules allow connections

### Authentication Failed
- Verify user password in CREDENTIALS.md
- Ensure users were created via complete_setup.sql
- Check user permissions

### Table Already Exists
- All CREATE TABLE statements use "IF NOT EXISTS"
- Safe to re-run without errors
- Tables will be skipped if they already exist

---

## Data Model Relationships

```
User_Role_Master (1) ──────────── (N) User_Master
         │                              │
         │                              │
    User_Login                    Report_History
         │
         └─ User_Master (FK)

State_City_PinCode_Master (Referenced by User_Master & New_User_Request)
```

---

## Next Steps

After successful deployment:

1. **Populate Master Data**
   - Insert user roles in User_Role_Master
   - Insert geographic data in State_City_PinCode_Master

2. **Create API Endpoints**
   - User registration (New_User_Request)
   - Login (User_Login)
   - Report upload (Report_History)

3. **Set Up Monitoring**
   - Monitor table growth
   - Set up automated backups
   - Configure query performance tracking

4. **Security**
   - Implement row-level security policies
   - Audit sensitive operations
   - Monitor access patterns

---

## Support Files Location

```
/Users/shishupals/Documents/Claude/projects/Medostel/Development/DevOps Development/DBA/
├── Databasespecs.md
├── create_tables.sql
├── DEPLOYMENT_GUIDE.md
└── Tables.md
```

---

## Quick Command Reference

```bash
# Start proxy
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

# List tables
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user --project=gen-lang-client-0064186167 --database=Medostel
# Then: \dt

# View table structure
# Then: \d table_name

# Show indexes
# Then: \di
```

---

**Last Updated**: 2026-02-28
**Status**: Ready for Deployment
**Created By**: Claude Code
