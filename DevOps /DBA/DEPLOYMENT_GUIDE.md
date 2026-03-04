# Database Table Deployment Guide

## Overview

This guide provides step-by-step instructions to create the 6 core tables in the Medostel PostgreSQL database.

**Database**: Medostel
**Engine**: PostgreSQL 18.2
**Instance**: medostel-ai-assistant-pgdev-instance
**Project**: gen-lang-client-0064186167
**Schema Version**: 2.1 (Updated March 3, 2026)
**Status**: Production Ready ✅

### Recent Schema Changes (March 3, 2026 - STEP 1.3)
- ✅ User_Role_Master.roleId changed from VARCHAR(10) to SERIAL INTEGER (auto-increment 1-8)
- ✅ User_Master.currentRole changed from VARCHAR(50) to INTEGER (references roleId 1-8)
- ✅ User_Login.roleId changed from VARCHAR(50) to INTEGER (references roleId 1-8)
- ✅ Migration script with rollback available: user_role_master_migration.sql
- ✅ All dependent foreign keys updated with CASCADE rules

### Previous Schema Changes (March 1, 2026)
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

## Step 2.5: Execute STEP 1.3 User_Role_Master Migration (IF UPGRADING FROM EXISTING DATABASE)

**⚠️ IMPORTANT**: Only execute this step if you have an existing database with VARCHAR(10) roleId. For fresh installations, the create_Tables.sql already contains the new SERIAL INTEGER schema.

Execute the migration script to convert roleId from VARCHAR(10) to SERIAL INTEGER:

```bash
cd /Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/src/SQL\ files

# Start Cloud SQL Proxy
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

sleep 3

# Create backup first (HIGHLY RECOMMENDED)
gcloud sql backups create medostel-pre-step1-3 \
  --instance=medostel-ai-assistant-pgdev-instance \
  --project=gen-lang-client-0064186167

# Execute migration
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user \
  --project=gen-lang-client-0064186167 \
  --database=Medostel < user_role_master_migration.sql
```

**Migration Script Details**:
- Drops dependent foreign keys from user_master and user_login
- Drops old user_role_master table
- Creates new user_role_master with SERIAL INTEGER roleId (auto-increment 1-8)
- Inserts 8 standard roles with auto-generated IDs
- Updates user_master.currentRole to INTEGER with proper FK constraints
- Updates user_login.roleId to INTEGER with proper FK constraints
- Includes rollback script (commented) for manual rollback if needed

**Expected Output**:
```
✓ Foreign keys dropped
✓ Old table dropped
✓ New table created with SERIAL roleId
✓ 8 roles inserted (IDs 1-8)
✓ Foreign key constraints updated
✓ Migration complete
```

**Verification After Migration**:
```bash
# Connect to database
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user \
  --project=gen-lang-client-0064186167 \
  --database=Medostel

# Run these queries:
SELECT * FROM user_role_master;  -- Should show roleId as 1-8 (integers)
SELECT COUNT(*) FROM user_role_master;  -- Should show 8 rows
SELECT * FROM information_schema.table_constraints WHERE table_name = 'user_master' AND constraint_type = 'FOREIGN KEY';  -- Verify FKs
```

---

## Step 2.6: New_User_Request Schema Migration (NEW - March 4, 2026)

**⚠️ IMPORTANT**: This step is REQUIRED if you have an existing `new_user_request` table with the old schema. For fresh installations, the `create_Tables.sql` already contains the new schema. Execute ONLY if upgrading from previous versions.

### Pre-Migration Checklist

Before executing the migration:

```bash
# 1. Backup the database
gcloud sql backups create medostel-backup-$(date +%Y%m%d-%H%M%S) \
  --instance=medostel-ai-assistant-pgdev-instance \
  --project=gen-lang-client-0064186167

# 2. Verify backup completion
gcloud sql backups list --instance=medostel-ai-assistant-pgdev-instance
```

### Migration Scripts Location

The migration scripts are located in:
```
/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/src/SQL\ files/
├── 08_migrate_new_user_request_schema.sql (Schema migration)
├── 09_validate_new_user_request_migration.sql (Validation)
└── 10_rollback_new_user_request_migration.sql (Rollback - if needed)
```

### Schema Changes

The migration restructures `new_user_request` table from:
```
OLD: requestId, userName, emailId, requestStatus, approvalDate, etc.
NEW: requestId, userId, firstName, lastName, mobileNumber, organization,
     currentRole, status, city_name, district_name, pincode, state_name,
     created_Date, updated_Date
```

### Migration Steps

**Step 1: Execute Migration Script**
```bash
cd /Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend

# Start Cloud SQL Proxy (if not already running)
/opt/homebrew/share/google-cloud-sdk/bin/cloud-sql-proxy \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance &

sleep 3

# Execute migration
PGPASSWORD='Iag2bMi@0@6aA' psql \
  -h localhost \
  -p 5432 \
  -U medostel_admin_user \
  -d medostel \
  -f "src/SQL files/08_migrate_new_user_request_schema.sql"
```

Expected Output:
```
BEGIN
ALTER TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
...
INSERT 0 X  (X = number of rows migrated)
COMMIT
```

**Step 2: Validate Migration**
```bash
# Execute validation script
PGPASSWORD='Iag2bMi@0@6aA' psql \
  -h localhost \
  -p 5432 \
  -U medostel_admin_user \
  -d medostel \
  -f "src/SQL files/09_validate_new_user_request_migration.sql"
```

Expected Output:
```
=== SCHEMA VALIDATION ===
[14 columns with correct types verified]

=== CONSTRAINT VALIDATION ===
[7 indexes listed]

=== DATA INTEGRITY CHECKS ===
[All validation checks passed]

=== MIGRATION SUMMARY ===
[Row counts match, no data loss]
```

**Step 3: Verify Table Structure**
```bash
# Connect to database
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=medostel_admin_user \
  --project=gen-lang-client-0064186167 \
  --database=medostel

# Run verification queries:
\d new_user_request  -- Show all columns and constraints
\di new_user_request*  -- List all indexes
SELECT COUNT(*) FROM new_user_request;  -- Row count
```

### Rollback Procedure (If Migration Fails)

If the migration encounters issues:

```bash
# Execute rollback script
PGPASSWORD='Iag2bMi@0@6aA' psql \
  -h localhost \
  -p 5432 \
  -U medostel_admin_user \
  -d medostel \
  -f "src/SQL files/10_rollback_new_user_request_migration.sql"
```

This will:
- Drop the new `new_user_request` table
- Restore the backup as `new_user_request`
- Recreate original indexes

### Migration Verification Checklist

After successful migration, verify:

```
☐ Schema validation script passed all checks
☐ All 14 columns present with correct data types
☐ All 7 indexes created and functional
☐ All 3 CHECK constraints active
☐ No data loss during migration
☐ Backup table cleaned up (optional: DROP TABLE IF EXISTS new_user_request_backup)
☐ Application tests pass (105+ tests for new_user_request API)
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
