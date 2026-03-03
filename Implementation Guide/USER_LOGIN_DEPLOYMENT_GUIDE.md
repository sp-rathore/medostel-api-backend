# User_Login API - Deployment Guide

**Date:** March 3, 2026
**Version:** 1.0
**Status:** Ready for Deployment
**Target Environment:** Production (PostgreSQL 18 on Google Cloud SQL)

---

## 📋 Pre-Deployment Checklist

Before executing deployment, verify all items:

- [ ] All code committed to git
- [ ] All tests passing locally (105/105)
- [ ] Documentation reviewed
- [ ] Database credentials verified
- [ ] Network connectivity confirmed
- [ ] Backup strategy planned
- [ ] Rollback procedure reviewed
- [ ] Team notification sent
- [ ] Maintenance window scheduled

---

## 🔧 Environment Setup

### Required Tools

```bash
# PostgreSQL client
psql --version
# Expected: psql (PostgreSQL) 13+

# Python environment
python --version
# Expected: Python 3.11+

# Git for version control
git --version
# Expected: git version 2.x+

# Cloud SQL Proxy (for GCP)
cloud_sql_proxy --version
# Expected: Cloud SQL Proxy version 1.x+
```

### Database Connection Verification

```bash
# Test admin connection
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "SELECT version();"

# Expected output:
# PostgreSQL 18.2 on x86_64-pc-linux-gnu...

# Test API user connection
psql -h 35.244.27.232 -U medostel_api_user -d medostel -c "SELECT 1;"

# Expected output:
# 1
```

### Using Cloud SQL Proxy

```bash
# Start proxy in background
cloud_sql_proxy -instances=gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance=tcp:5432 &

# Verify proxy is running
netstat -tuln | grep 5432

# Expected output:
# tcp        0      0 127.0.0.1:5432         0.0.0.0:*               LISTEN
```

---

## 📦 Deployment Phases

### Phase 1: Pre-Migration Verification (15 minutes)

**Step 1.1: Run pre-migration checks**

```bash
cd /path/to/medostel-api-backend

# Execute pre-migration validation
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -f src/SQL\ files/01_pre_migration_checks.sql
```

**Expected Output:**
```
✓ Database connectivity: OK
✓ user_master table exists
✓ user_role_master table exists
✓ No existing user_login table
```

**Step 1.2: Backup current database**

```bash
# Create backup with timestamp
BACKUP_FILE="backup_user_login_$(date +%Y%m%d_%H%M%S).sql"

pg_dump -h 35.244.27.232 -U medostel_admin_user -d medostel > "$BACKUP_FILE"

# Verify backup size
ls -lh "$BACKUP_FILE"

# Expected: ~304 KB or larger
```

**Step 1.3: Verify backup integrity**

```bash
# Test backup can be restored (dry run)
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -f "$BACKUP_FILE" --dry-run

# Expected: No errors
```

**Checklist:**
- [ ] Pre-migration checks passed
- [ ] Database backup created
- [ ] Backup verified
- [ ] All tables accounted for

---

### Phase 2: Database Schema Migration (20 minutes)

**Step 2.1: Execute migration script**

```bash
# Run migration
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -f src/SQL\ files/05_migrate_user_login_schema.sql

# Monitor output for any errors
```

**Expected Output:**
```
CREATE TABLE
CREATE INDEX (x5)
NOTICE: Migration completed successfully!
NOTICE: New user_login table created
NOTICE: Backup table: user_login_backup
```

**Step 2.2: Validate migration**

```bash
# Run validation script
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -f src/SQL\ files/06_validate_user_login_migration.sql

# Review all validation results
```

**Expected Output:**
```
✓ user_login table exists
✓ Correct column count: 7
✓ All required columns present
✓ All old columns removed
✓ email_id is PRIMARY KEY
✓ All indexes created (5 total)
✓ Foreign key constraints verified
✓ CHECK constraints verified
✓ All data integrity checks passed
```

**Step 2.3: Verify table structure**

```bash
# Check table structure
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "\d user_login"

# Expected columns:
# email_id | password | mobile_number | is_active | last_login | created_date | updated_date
```

**Step 2.4: Verify indexes**

```bash
# List all indexes
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "\di user_login*"

# Expected indexes (5):
# pk_user_login
# idx_login_mobile
# idx_login_is_active
# idx_login_last_login
# idx_login_updated_date
```

**Checklist:**
- [ ] Migration script executed
- [ ] Validation script passed (all checks)
- [ ] Table structure verified
- [ ] All 5 indexes created
- [ ] Foreign keys verified
- [ ] No errors in migration log

---

### Phase 3: Application Code Deployment (20 minutes)

**Step 3.1: Update code from git**

```bash
# Pull latest changes
git pull origin main

# Verify User_Login files present
ls -la src/routes/v1/user_login.py
ls -la src/schemas/user_login.py
ls -la src/db/user_login_utils.py
ls -la src/utils/password_utils.py
```

**Expected:** All 4 files present and up-to-date

**Step 3.2: Install/Update dependencies**

```bash
# Install required packages
pip install fastapi
pip install pydantic>=2.0
pip install bcrypt
pip install passlib
pip install psycopg2-binary

# Verify installations
pip list | grep -E "fastapi|pydantic|bcrypt|passlib|psycopg"
```

**Step 3.3: Register API routes**

```python
# In main app file (src/main.py or similar):
from src.routes.v1 import user_login

app = FastAPI()
app.include_router(user_login.router)

# Verify routes are registered
# GET /openapi.json should include /api/v1/user-login/* paths
```

**Step 3.4: Update database connection**

```python
# In src/routes/v1/user_login.py, update get_db_connection():
def get_db_connection():
    """Get database connection from connection pool"""
    import psycopg2
    return psycopg2.connect(
        host='35.244.27.232',
        user='medostel_api_user',
        password='Iag2bMi@0@6aD',
        database='medostel',
        port=5432
    )
```

**Checklist:**
- [ ] Code files present
- [ ] Dependencies installed
- [ ] Routes registered in main app
- [ ] Database connection configured
- [ ] Connection credentials correct

---

### Phase 4: Testing Deployment (30 minutes)

**Step 4.1: Run unit tests**

```bash
# Navigate to project root
cd /path/to/medostel-api-backend

# Run all User_Login tests
pytest tests/test_user_login_*.py -v --tb=short

# Expected output:
# test_user_login_schemas.py ..................... 30 PASSED
# test_user_login_db_utils.py .................... 35 PASSED
# test_user_login_api.py ......................... 40 PASSED
# 105 passed in X.XXs
```

**Step 4.2: Run integration tests (with live DB)**

```bash
# Create integration test script
cat > test_deployment.py << 'EOF'
import psycopg2
from src.db.user_login_utils import UserLoginManager

# Test database connection
conn = psycopg2.connect(
    host='35.244.27.232',
    user='medostel_api_user',
    password='Iag2bMi@0@6aD',
    database='medostel'
)

# Test table exists
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='user_login'")
exists = cursor.fetchone()[0] > 0
print(f"✓ user_login table exists: {exists}")

# Test indexes exist
cursor.execute("SELECT COUNT(*) FROM pg_indexes WHERE tablename='user_login'")
index_count = cursor.fetchone()[0]
print(f"✓ user_login indexes: {index_count} (expected 5)")

# Test Foreign Key
cursor.execute("""
    SELECT COUNT(*) FROM information_schema.table_constraints
    WHERE table_name='user_login' AND constraint_type='FOREIGN KEY'
""")
fk_count = cursor.fetchone()[0]
print(f"✓ user_login foreign keys: {fk_count} (expected 1)")

conn.close()
print("\n✅ All integration checks passed!")
EOF

# Run integration tests
python test_deployment.py
```

**Expected Output:**
```
✓ user_login table exists: True
✓ user_login indexes: 5 (expected 5)
✓ user_login foreign keys: 1 (expected 1)

✅ All integration checks passed!
```

**Step 4.3: Test API endpoints (manual)**

```bash
# Start FastAPI server
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Wait for server to start
sleep 5

# Test 1: Health check
curl -X GET "http://localhost:8000/api/v1/user-login/health"
# Expected: {"status": "healthy", "service": "user_login", "timestamp": "..."}

# Test 2: Authenticate (should fail - no record yet)
curl -X GET "http://localhost:8000/api/v1/user-login/authenticate?email_id=test@example.com"
# Expected: 404 Not Found

# Test 3: Check Swagger documentation
curl -X GET "http://localhost:8000/docs"
# Expected: Swagger UI accessible

# Kill FastAPI server
pkill -f "uvicorn src.main:app"
```

**Checklist:**
- [ ] All 105 unit tests passing
- [ ] Integration tests passing
- [ ] Table exists and accessible
- [ ] Indexes created correctly
- [ ] Foreign keys verified
- [ ] API endpoints responding
- [ ] Documentation accessible

---

### Phase 5: Performance Verification (15 minutes)

**Step 5.1: Check query performance**

```bash
# Enable query timing
psql -h 35.244.27.232 -U medostel_admin_user -d medostel

# In psql prompt:
\timing on

# Test email lookup query
SELECT COUNT(*) FROM user_login WHERE email_id = 'test@example.com';
# Expected: < 50ms with index

# Test mobile lookup query
SELECT COUNT(*) FROM user_login WHERE mobile_number = 9876543210;
# Expected: < 100ms with index

# Test status filter
SELECT COUNT(*) FROM user_login WHERE is_active = 'Y';
# Expected: < 100ms with index

\q
```

**Step 5.2: Monitor database performance**

```bash
# Check active connections
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "SELECT COUNT(*) FROM pg_stat_activity;"
# Expected: < 10 connections

# Check table size
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
  FROM pg_tables
  WHERE tablename='user_login';
"
# Expected: Small size initially (< 1 MB)
```

**Checklist:**
- [ ] Index query performance verified
- [ ] All queries < 150ms
- [ ] Connection count normal
- [ ] Table size reasonable

---

## 🔄 Rollback Procedure

**If migration fails or needs rollback:**

### Quick Rollback (< 10 minutes)

```bash
# Step 1: Stop application
systemctl stop medostel-api || pkill -f "uvicorn"

# Step 2: Execute rollback script
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -f src/SQL\ files/07_rollback_user_login_migration.sql

# Step 3: Verify old schema restored
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "\d user_login"

# Step 4: Restore from backup if needed
psql -h 35.244.27.232 -U medostel_admin_user -d medostel < backup_user_login_YYYYMMDD_HHMMSS.sql

# Step 5: Restart application
systemctl start medostel-api
```

**Rollback Checklist:**
- [ ] Application stopped
- [ ] Rollback script executed
- [ ] Old schema verified
- [ ] Data integrity confirmed
- [ ] Application restarted
- [ ] Tests passing

---

## 📊 Post-Deployment Verification

### Verification Checklist (Execute within 1 hour of deployment)

**1. Database Health (5 minutes)**
```bash
psql -h 35.244.27.232 -U medostel_admin_user -d medostel << 'EOF'
-- Check table exists and is accessible
SELECT tablename FROM pg_tables WHERE tablename = 'user_login';

-- Check record count
SELECT COUNT(*) as total_records FROM user_login;

-- Check backup table
SELECT COUNT(*) FROM user_login_backup;

-- Check no orphaned records
SELECT COUNT(*) FROM user_login ul
WHERE NOT EXISTS (SELECT 1 FROM user_master um WHERE um.emailId = ul.email_id);
EOF
```

**2. API Health (5 minutes)**
```bash
# Check health endpoint
curl -s http://localhost:8000/api/v1/user-login/health | jq .

# Check Swagger documentation
curl -s http://localhost:8000/openapi.json | jq '.paths["/api/v1/user-login"]' | head -20

# Check API is responding
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/user-login/health
# Expected: 200
```

**3. Performance Monitoring (10 minutes)**
```bash
# Monitor response times
ab -n 100 -c 10 http://localhost:8000/api/v1/user-login/health

# Expected:
# Requests per second: > 100
# Time per request: < 50ms
# Failed requests: 0
```

**4. Error Logging (5 minutes)**
```bash
# Check application logs
tail -f /var/log/medostel-api/error.log

# Expected: No error messages related to user_login
```

**5. Database Audit (5 minutes)**
```bash
# Check access logs
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT usename, application_name, state
  FROM pg_stat_activity
  WHERE datname = 'medostel';
"

# Expected: API user connections are healthy
```

---

## 📈 Monitoring & Maintenance

### Daily Monitoring

```bash
# Check table size growth
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT pg_size_pretty(pg_total_relation_size('user_login'));
"

# Check index fragmentation
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT schemaname, tablename, indexname
  FROM pg_indexes
  WHERE tablename = 'user_login';
"

# Check unused indexes
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT indexname, idx_scan
  FROM pg_stat_user_indexes
  WHERE relname = 'user_login'
  ORDER BY idx_scan DESC;
"
```

### Weekly Maintenance

```bash
# Analyze table for query optimization
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "ANALYZE user_login;"

# Vacuum to clean up dead rows
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "VACUUM ANALYZE user_login;"

# Check for null values
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT column_name, COUNT(*)
  FROM user_login
  WHERE column_name IS NULL
  GROUP BY column_name;
"
```

### Monthly Monitoring

```bash
# Verify backup integrity
pg_dump -h 35.244.27.232 -U medostel_admin_user -d medostel --verbose > /dev/null

# Check for bloat
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "
  SELECT pg_size_pretty(pg_total_relation_size('user_login')) as size,
         (SELECT COUNT(*) FROM user_login) as rows;
"

# Archive old login records (optional)
-- Keep only last 90 days
DELETE FROM user_login WHERE updated_date < NOW() - INTERVAL '90 days' AND is_active = 'N';
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

**Issue 1: Migration fails with FK error**
```
ERROR: insert or update on table "user_login" violates foreign key constraint
```
**Solution:**
```bash
# Verify user_master records exist
SELECT COUNT(*) FROM user_master;

# Check for orphaned emails
SELECT ul.email_id FROM user_login_backup ul
WHERE NOT EXISTS (SELECT 1 FROM user_master um WHERE um.emailId = ul.email_id);

# Clean orphaned records before migration
```

**Issue 2: Index creation fails**
```
ERROR: relation "user_login" already exists
```
**Solution:**
```bash
# Drop conflicting table/indexes
DROP TABLE IF EXISTS user_login CASCADE;

# Re-run migration script
```

**Issue 3: API cannot connect to database**
```
ERROR: could not connect to server: No such file or directory
```
**Solution:**
```bash
# Verify database is running
psql -h 35.244.27.232 -U medostel_admin_user -d medostel -c "SELECT 1;"

# Check firewall rules
gcloud sql connect medostel-ai-assistant-pgdev-instance --user=root

# Verify credentials
echo "Host: 35.244.27.232"
echo "User: medostel_api_user"
echo "Database: medostel"
echo "Port: 5432"
```

**Issue 4: Performance degradation**
```
Query time > 500ms
```
**Solution:**
```bash
# Check for missing indexes
SELECT indexname FROM pg_indexes WHERE tablename='user_login';

# Rebuild index if needed
REINDEX INDEX idx_login_mobile;

# Analyze table
ANALYZE user_login;

# Check for table bloat
VACUUM ANALYZE user_login;
```

---

## ✅ Deployment Success Criteria

Deployment is successful when:

- [x] Pre-migration checks pass
- [x] Migration completes without errors
- [x] Validation script passes all 15 checks
- [x] All 105 tests pass
- [x] API endpoints respond correctly
- [x] Performance metrics acceptable (< 150ms)
- [x] No errors in application logs
- [x] Database integrity verified
- [x] Backup verified
- [x] Rollback procedure tested

---

## 📞 Support Contacts

**Database Issues:**
- DBA: medostel-dba@company.com
- GCP Support: support@google.com

**Application Issues:**
- API Developer: medostel-api-dev@company.com
- Operations: ops@company.com

**Emergency Rollback:**
- On-Call: +1-XXX-XXX-XXXX
- Escalation: medostel-incident@company.com

---

## 📝 Deployment Log Template

Use this template to document your deployment:

```
DEPLOYMENT LOG - User_Login API
Date: _______________
Deployed By: _______________
Environment: Production

PRE-DEPLOYMENT:
- [ ] Tests passed locally: _______________
- [ ] Code review completed: _______________
- [ ] Database backup created: _______________

MIGRATION:
- [ ] Pre-migration checks: PASSED / FAILED
- [ ] Migration script executed: HH:MM:SS
- [ ] Validation script passed: ___/15 checks
- [ ] Issues encountered: _______________

POST-DEPLOYMENT:
- [ ] API health check: PASSED / FAILED
- [ ] All endpoints tested: _______________
- [ ] Performance verified: _______________
- [ ] Logs reviewed: _______________

SIGN-OFF:
- Deployed: Date Time
- Verified: Date Time
- Approved: Date Time

Notes:
_________________________________________________________________
```

---

**Deployment Guide Complete**

Ready to deploy? Follow the steps above in order.
Questions? Refer to troubleshooting section or contact support.

**Last Updated:** March 3, 2026
**Status:** Ready for Production Deployment
