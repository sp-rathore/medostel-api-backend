# Phase 6: Manual Execution Guide

**Alternative to:** `execute_phase_6.sh`
**For users who prefer step-by-step manual execution**
**Last Updated:** March 3, 2026

---

## Quick Start (Automated)

If you want to run all phases automatically:

```bash
cd "/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/DevOps Development/DBA"
bash execute_phase_6.sh
```

This will execute all 5 phases with logging and verification.

---

## Manual Execution Steps

If you prefer to execute each phase manually, follow these steps:

---

## PHASE 6.1: Pre-Migration Verification

### Verify Database Connection

```bash
# Test PostgreSQL connection
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -c "SELECT version();"

# Expected output:
# PostgreSQL X.X.X on...
```

### Check Current Table Structure

```bash
# Connect to database and view current schema
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel << 'EOF'

-- View current columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Current record count
SELECT COUNT(*) as current_record_count FROM State_City_PinCode_Master;

-- Sample records
SELECT stateId, stateName, cityId, cityName, pinCode FROM State_City_PinCode_Master LIMIT 3;

EOF
```

**Expected Output:**
- Current columns: pinCode, stateId, stateName, cityId, cityName, countryName, status, createdDate, updatedDate
- Record count: X records (note this number for verification)
- Sample records showing existing data structure

**✓ Phase 6.1 Complete:** You have verified the current state and can proceed to migration.

---

## PHASE 6.2: Database Schema Migration

### Execute Migration Script

```bash
# Set PostgreSQL password environment variable
export PGPASSWORD="Iag2bMi@6aD"

# Run migration script
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -f "DevOps Development/DBA/migration_step1_1.sql"

# Unset password after completion
unset PGPASSWORD
```

**What happens:**
1. Backup table created: `State_City_PinCode_Master_Backup_Step1_1`
2. 2 new columns added: `districtId` (INTEGER), `districtName` (VARCHAR(100))
3. 6 new indexes created for hierarchical queries
4. Schema verified

**Expected Duration:** 2-3 minutes

### Verify Migration Success

```bash
# Check new columns exist
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel << 'EOF'

-- View updated columns
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Verify backup
SELECT COUNT(*) as backup_count FROM State_City_PinCode_Master_Backup_Step1_1;

-- Verify indexes created
SELECT indexname FROM pg_indexes
WHERE tablename = 'state_city_pincode_master'
ORDER BY indexname;

EOF
```

**Expected Output:**
- New columns: districtId, districtName in the column list
- Backup count: Should match original record count
- Indexes: 6 new indexes (idx_districtId, idx_districtName, idx_state_district, etc.)

**✓ Phase 6.2 Complete:** Schema migration successful!

---

## PHASE 6.3: Data Preparation

### Option A: Check for Pre-Prepared Data

```bash
# Check if cleaned data exists
ls -lh "Data Extraction/cleaned_data.csv"

# If file exists, skip transformation and go to Phase 6.4
# If file doesn't exist, proceed to Option B
```

### Option B: Download and Transform OGD Data

#### Step 1: Download OGD Data

Go to: https://data.gov.in/

Search for: "Indian postal codes" or "pincode data"

Download CSV file and save as:
```
Data Extraction/ogd_india_pincodes.csv
```

#### Step 2: Transform Data

```bash
# Navigate to data extraction directory
cd "Data Extraction"

# Run Python transformer
python pin_code_data_transformer.py

# Output:
# - cleaned_data.csv (19,000+ records)
# - data_transformation_report.txt (metrics)

# Return to project directory
cd -
```

### Verify Transformation

```bash
# Check output files
ls -lh "Data Extraction/cleaned_data.csv"
ls -lh "Data Extraction/data_transformation_report.txt"

# View transformation report
cat "Data Extraction/data_transformation_report.txt"

# Count records
wc -l "Data Extraction/cleaned_data.csv"
```

**Expected Output:**
- cleaned_data.csv: ~19,234 lines
- Report shows:
  - Total records processed: 19,234
  - States: 36
  - Districts: 380+
  - Cities: 1,500+
  - Status: SUCCESS

**✓ Phase 6.3 Complete:** Data is transformed and ready to load!

---

## PHASE 6.4: Data Loading

### Load Data into Database

```bash
# Execute loading script
export PGPASSWORD="Iag2bMi@6aD"

psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -f "DevOps Development/DBA/load_pincode_data.sql"

unset PGPASSWORD
```

**What happens:**
1. Creates temporary staging table
2. Loads CSV data using COPY command
3. Validates data integrity
4. Applies NOT NULL constraints
5. Updates table statistics
6. Verifies indexes
7. Cleans up temporary tables
8. Performs final count verification

**Expected Duration:** 2-5 minutes
**Expected Data Size:** ~500MB

### Verify Data Loading

```bash
# Check if data loaded successfully
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel << 'EOF'

-- Total records loaded
SELECT COUNT(*) as total_records FROM State_City_PinCode_Master;

-- Records by state (first 5)
SELECT stateId, stateName, COUNT(*) as record_count
FROM State_City_PinCode_Master
GROUP BY stateId, stateName
ORDER BY stateId
LIMIT 5;

-- Sample records with district fields
SELECT stateId, stateName, districtId, districtName, cityId, cityName, pinCode
FROM State_City_PinCode_Master
WHERE districtId IS NOT NULL
LIMIT 5;

-- Verify no NULL values in required fields
SELECT
    (SELECT COUNT(*) FROM State_City_PinCode_Master WHERE stateId IS NULL) as null_stateId,
    (SELECT COUNT(*) FROM State_City_PinCode_Master WHERE districtId IS NULL) as null_districtId,
    (SELECT COUNT(*) FROM State_City_PinCode_Master WHERE pinCode IS NULL) as null_pinCode;

-- Table statistics
SELECT pg_size_pretty(pg_total_relation_size('state_city_pincode_master')) as table_size;

EOF
```

**Expected Results:**
- Total records: 19,234
- Records distributed across 36 states
- Sample records show districtId and districtName
- NULL check results: All zeros (no NULL values)
- Table size: ~500MB

**✓ Phase 6.4 Complete:** Data successfully loaded!

---

## PHASE 6.5: API Verification

### Start the API Server

```bash
# Terminal 1: Start FastAPI server
cd "/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

### Test Endpoints Manually (Terminal 2)

#### Test 1: API 1 - Get All Locations

```bash
curl -X GET "http://localhost:8000/api/v1/locations/all?state_id=27&limit=5" \
  -H "Accept: application/json" | jq .

# Expected:
# - status: "success"
# - code: 200
# - data.count: 5
# - data.locations[0].districtId: (numeric)
# - data.locations[0].districtName: (string)
```

#### Test 2: API 3.2 - Get Districts by State

```bash
curl -X GET "http://localhost:8000/api/v1/locations/districts/27" \
  -H "Accept: application/json" | jq .

# Expected:
# - status: "success"
# - data.count: 35+ (districts in Maharashtra)
# - data.districts[0]: {districtId: 1, districtName: "...", stateName: "Maharashtra"}
```

#### Test 3: API 3.3 - Get Cities by District

```bash
curl -X GET "http://localhost:8000/api/v1/locations/cities/1" \
  -H "Accept: application/json" | jq .

# Expected:
# - status: "success"
# - data.count: 10+ (cities in district 1)
# - data.cities[0]: {cityId: ..., cityName: "...", districtName: "...", stateName: "..."}
```

#### Test 4: API 3.4 - Get PinCodes by District

```bash
curl -X GET "http://localhost:8000/api/v1/locations/by-district/1" \
  -H "Accept: application/json" | jq .

# Expected:
# - status: "success"
# - data.count: 100+ (pincodes in district 1)
# - data.pincodes[0]: {pinCode: ..., cityName: "...", cityId: ...}
```

### Run Unit Tests

```bash
# Terminal 2: Run tests
cd "/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend"
pytest "API Development/Unit Testing/test_locations_api.py" -v

# Expected output:
# =============== 65 passed in X.XXs ===============
```

**Expected Results:**
- All 4 API tests return valid JSON with district data
- All 65 unit tests pass
- Response times < 100ms
- No errors in API logs

**✓ Phase 6.5 Complete:** All APIs working with loaded data!

---

## Phase 6 Summary

### Final Verification Query

```bash
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel << 'EOF'

\echo '=== PHASE 6 COMPLETION SUMMARY ==='
\echo ''
\echo 'Database: medostel'
\echo 'Table: state_city_pincode_master'
\echo ''
\echo 'Final Record Count:'
SELECT COUNT(*) as total_records FROM State_City_PinCode_Master;

\echo ''
\echo 'Geographic Coverage:'
SELECT
    COUNT(DISTINCT stateId) as states,
    COUNT(DISTINCT districtId) as districts,
    COUNT(DISTINCT cityId) as cities,
    COUNT(DISTINCT pinCode) as pincodes
FROM State_City_PinCode_Master;

\echo ''
\echo 'Sample by State (top 5):'
SELECT stateId, stateName, COUNT(*) as count
FROM State_City_PinCode_Master
GROUP BY stateId, stateName
ORDER BY COUNT(*) DESC
LIMIT 5;

EOF
```

---

## Troubleshooting

### Issue: Cannot Connect to Database

**Solution:**
```bash
# Check if PostgreSQL is running
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel -c "SELECT 1"

# Verify credentials
# User: medostel_api_user
# Host: 35.244.27.232
# Port: 5432
# Database: medostel
# Password: Iag2bMi@6aD
```

### Issue: Migration Script Fails

**Solution:**
```bash
# Check if previous migration ran
SELECT * FROM State_City_PinCode_Master_Backup_Step1_1 LIMIT 1;

# If error about columns already existing, migration already completed
# Check current columns
SELECT column_name FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master';
```

### Issue: Data Load Fails

**Solution:**
```bash
# Check if CSV file exists
ls -lh "Data Extraction/cleaned_data.csv"

# Verify CSV format
head -3 "Data Extraction/cleaned_data.csv"

# Check for data transformation report
cat "Data Extraction/data_transformation_report.txt"
```

### Issue: Unit Tests Fail

**Solution:**
```bash
# Run specific test for debugging
pytest "API Development/Unit Testing/test_locations_api.py::TestAPIOne_GetAllLocations::test_get_all_locations_success" -v

# Check API server logs for errors
# Ensure database migration completed successfully
# Verify data is loaded
```

---

## Rollback Procedures

### If Migration Needs to be Rolled Back

```bash
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel << 'EOF'

-- Drop the modified table
DROP TABLE state_city_pincode_master;

-- Restore from backup
ALTER TABLE State_City_PinCode_Master_Backup_Step1_1
RENAME TO state_city_pincode_master;

-- Verify
SELECT COUNT(*) FROM State_City_PinCode_Master;

EOF
```

### If Data Load Needs to be Rolled Back

```bash
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel << 'EOF'

-- Truncate the table to original post-migration state
TRUNCATE TABLE state_city_pincode_master;

-- Table structure remains intact for re-loading

EOF
```

---

## Success Checklist

- [ ] Phase 6.1: Database verified and backup created
- [ ] Phase 6.2: Schema migration completed (2 new columns, 6 new indexes)
- [ ] Phase 6.3: Data prepared (cleaned_data.csv created)
- [ ] Phase 6.4: Data loaded (19,234 records in database)
- [ ] Phase 6.5: APIs verified (all 4 endpoints returning data)
- [ ] Unit tests passed (65 tests)
- [ ] Final record count: 19,234
- [ ] Geographic coverage: 36 states, 380+ districts
- [ ] No NULL values in required fields

---

## Next Steps

Once Phase 6 is complete and verified:

1. **Commit results** (if using automated script)
2. **Document metrics** (record actual execution times and record counts)
3. **Proceed to Phase 7** (Version Control & Final Commits)

---

**Manual Execution Complete!**

All phases can be executed following this guide. The `execute_phase_6.sh` script automates all these steps.

