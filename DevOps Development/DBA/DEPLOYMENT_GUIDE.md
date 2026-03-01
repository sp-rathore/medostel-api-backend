# Database Table Deployment Guide

## Overview

This guide provides step-by-step instructions to create the 6 core tables in the Medostel PostgreSQL database.

**Database**: Medostel
**Engine**: PostgreSQL 18.2
**Instance**: medostel-ai-assistant-pgdev-instance
**Project**: gen-lang-client-0064186167
**Schema Version**: 2.0 (Updated March 1, 2026)
**Status**: Production Ready ✅

### Recent Schema Changes (March 1, 2026)
- ✅ User_Master.userId changed from VARCHAR(255) to BIGINT (supports up to 1 billion users)
- ✅ Email validation added using RFC 5322 regex pattern
- ✅ Mobile number changed to NUMERIC(10) with 10-digit validation (1000000000-9999999999)
- ✅ User_Login.userId updated to BIGINT to match User_Master
- ✅ All dependent tables updated with new constraints

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
cd /Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/DevOps\ Development

# Start Cloud SQL Proxy
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

# Wait for proxy
sleep 3

# Connect as admin user
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user \
  --project=gen-lang-client-0064186167 \
  --database=Medostel < create_Tables.sql
```

**Note**: The `create_Tables.sql` file includes all schema enhancements dated March 1, 2026.

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
- System Roles: ADMIN, DOCTOR, HOSPITAL, NURSE, PARTNER, PATIENT, RECEPTION, TECHNICIAN

### 2. **State_City_PinCode_Master** (9 columns)
- id (PK), stateId, stateName, cityName, cityId, pinCode, countryName, status, timestamps
- Geographic reference data for location-based queries

### 3. **User_Master** (12 columns) - ✅ ENHANCED
- userId (BIGINT PK), firstName, lastName, currentRole (FK), emailId (RFC 5322 validated), mobileNumber (NUMERIC(10) - 10 digits), organisation, address, status, createdDate, updatedDate
- **Schema v2.0**: BIGINT userId (supports 1 billion users), Email regex validation, 10-digit numeric mobile validation

### 4. **User_Login** (10 columns) - ✅ UPDATED
- userId (BIGINT PK/FK), username, password, roleId (FK), isActive, lastLoginTime, loginAttempts, timestamps
- **Schema v2.0**: userId now BIGINT to match User_Master, tracks login attempts

### 5. **New_User_Request** (13 columns) - ✅ ENHANCED
- requestId (PK), userName, firstName, lastName, currentRole, emailId (RFC 5322 validated), mobileNumber (NUMERIC(10) - 10 digits), address, requestStatus, approvalDate, approvalComments, timestamps
- **Schema v2.0**: Matching User_Master validation rules for email and mobile

### 6. **Report_History** (12 columns) - ✅ UPDATED
- id (PK), userId (BIGINT FK), fileName, fileType, reportType, status, diagnosis, inferredDiagnosis, pdfUrl, bucketLocation, jsonData, timestamps
- **Schema v2.0**: userId now BIGINT to match User_Master, enhanced status tracking

---

## Indexes Created

### Performance Indexes (35 total)

**User_Role_Master**:
- pk_user_role_master (PK), idx_role_status, idx_role_name, idx_role_updated

**State_City_PinCode_Master**:
- pk_state_city_pincode (PK), idx_state_id, idx_city_id, idx_pin_code, idx_country, idx_location_status

**User_Master** - ✅ ENHANCED:
- pk_user_master (PK), idx_user_email, idx_user_mobile, idx_user_role, idx_user_status, idx_user_name, idx_user_updated

**User_Login** - ✅ UPDATED:
- pk_user_login (PK), idx_login_username, idx_login_active, idx_login_role, idx_login_attempts, idx_login_lastlogin, idx_login_updated

**New_User_Request** - ✅ ENHANCED:
- pk_new_user_request (PK), idx_request_email, idx_request_mobile, idx_request_status, idx_request_role, idx_request_created, idx_request_updated

**Report_History** - ✅ UPDATED:
- pk_report_history (PK), idx_report_user, idx_report_type, idx_report_status, idx_report_created, idx_report_updated

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
/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/
├── DevOps Development/
│   ├── create_Tables.sql (Complete schema with all enhancements)
│   └── DBA/
│       ├── Databasespecs.md (Schema specifications)
│       ├── DBA.md (Complete DBA documentation)
│       └── DEPLOYMENT_GUIDE.md (This file)
└── Data Engineering/
    └── Medostel Tables Agent.md (Master table documentation)
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

**Last Updated**: 2026-03-01
**Schema Version**: 2.0 (Enhanced with BIGINT userId, email validation, 10-digit mobile validation)
**Status**: ✅ Production Ready with Enhanced Schema
**Created By**: Claude Code
