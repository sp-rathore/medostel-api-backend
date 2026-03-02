# Phase 6: Data Loading & Verification - Execution Checklist

**Status:** READY FOR EXECUTION
**Date:** March 3, 2026
**Prepared by:** Step 1.1 Implementation

---

## ✅ PRE-EXECUTION VERIFICATION

### Infrastructure Check
- [x] Database host reachable: 35.244.27.232:5432
- [x] Database name: medostel
- [x] Database user: medostel_api_user
- [x] Network access: Verified in previous phases
- [x] Backup procedures: Documented

### Code Readiness Check
- [x] API schemas updated with district fields
- [x] Service layer methods created (6 endpoints)
- [x] Route handlers implemented (15 endpoints)
- [x] Database schema changes prepared
- [x] Test suite created (65 tests)
- [x] Fixtures updated (8 fixtures)

### Documentation Check
- [x] Migration script created: `migration_step1_1.sql`
- [x] Data loading script created: `load_pincode_data.sql`
- [x] Data transformation script: `pin_code_data_transformer.py`
- [x] Execution guide: `PHASE_6_EXECUTION_GUIDE.md`
- [x] Rollback procedures documented

### Git Status Check
- [x] Phase 1-5 committed (5 commits)
- [x] Working tree clean
- [x] Ready for Phase 6 execution

---

## 📋 PHASE 6.1: PRE-MIGRATION BACKUP

**Task:** Verify database and create backup

**Action Items:**
```sql
-- Execute in PostgreSQL client or pgAdmin

-- Step 1: Verify current state
SELECT COUNT(*) as current_records FROM State_City_PinCode_Master;
SELECT column_name FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Step 2: Create backup (included in migration script)
-- Will be executed automatically in migration_step1_1.sql
```

**Expected Result:**
- Current record count: Check output
- Columns: pinCode, stateId, stateName, cityId, cityName, countryName, status, createdDate, updatedDate
- Backup: State_City_PinCode_Master_Backup_Step1_1 created with same record count

**Command to Execute:**
```bash
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -c "SELECT COUNT(*) as current_records FROM State_City_PinCode_Master;"
```

---

## 🔄 PHASE 6.2: SCHEMA MIGRATION

**Task:** Add districtId and districtName columns

**Migration Script:** `DevOps Development/DBA/migration_step1_1.sql`

**Critical Steps:**
1. Verify table structure (BEFORE)
2. Create backup table
3. Add 2 new columns
4. Create 6 new indexes
5. Verify columns (AFTER)
6. Count records

**Command to Execute:**
```bash
# Single command to run entire migration script
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -f "DevOps Development/DBA/migration_step1_1.sql"
```

**Expected Output:**
```
Status: Step 1: Verifying current table structure...
[Table structure output]

Status: Step 2: Creating backup table...
Backup created successfully!

Status: Step 3: Adding new district columns...
District columns added successfully!

Status: Step 4: Creating indexes...
Indexes created successfully!
```

**Verification Query:**
```sql
-- Verify columns after migration
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Expected columns:
-- pinCode, stateId, stateName, districtId, districtName, cityId, cityName,
-- countryName, status, createdDate, updatedDate

-- Verify backup
SELECT COUNT(*) FROM State_City_PinCode_Master_Backup_Step1_1;
```

---

## 📊 PHASE 6.3: DATA PREPARATION

**Task:** Extract and transform OGD data

**Source:** Official Government Data (OGD) Platform
- URL: https://data.gov.in/
- Dataset: Indian postal codes with geographic hierarchy
- Format: CSV
- Expected records: ~19,000

**Step 3.1: Download OGD Data**

Option 1: Download from OGD website
```bash
cd "Data Extraction"
# Download CSV and save as ogd_india_pincodes.csv
```

Option 2: Use pre-extracted data (if available)
```bash
# Check if file already exists
ls -lh Data Extraction/ogd_india_pincodes.csv
```

**Step 3.2: Transform Data**

```bash
cd "Data Extraction"
python pin_code_data_transformer.py
```

**Script Output:**
- `cleaned_data.csv` - 19,000+ records with hierarchical IDs
- `data_transformation_report.txt` - Validation metrics

**Transformation Includes:**
- Hierarchical ID assignment (Country→State→District→City→PinCode)
- Duplicate removal
- Data validation
- City name extraction (proper names, not post office names)
- Missing value handling

**Example Output from Report:**
```
=== Data Transformation Report ===
Total records processed: 19,234
Unique pincodes: 19,234
States identified: 36
Districts identified: 382
Cities identified: 1,523
Duplicates removed: 245
Invalid records: 12
Transformation time: 5.2 seconds
Status: SUCCESS
```

---

## 💾 PHASE 6.4: DATA LOADING

**Task:** Load cleaned data into database

**Data Loading Script:** `DevOps Development/DBA/load_pincode_data.sql`

**12-Step Loading Process:**

1. **Pre-load Verification**
   - Check constraints
   - Verify indexes exist

2. **Create Temp Table**
   - Staging area for CSV data

3. **Load CSV Data**
   ```bash
   # Data from: Data Extraction/cleaned_data.csv
   # Into: temp_pincode_staging
   ```

4. **Data Validation**
   - Check NOT NULL fields
   - Verify numeric ranges
   - Confirm unique pincodes

5. **Apply NOT NULL Constraints**
   - stateId, stateName, districtId, districtName
   - cityId, cityName, pinCode

6. **Update Statistics**
   - Analyze table for query optimization

7. **Index Verification**
   - Confirm all 6 indexes built

8. **Cleanup**
   - Remove temporary tables

9. **Final Record Count**
   - Verify all 19,000+ records loaded

10. **Performance Tests**
    - Sample queries to verify speed

11. **Post-Load Backup**
    - Save backup after successful load

12. **Documentation**
    - Record metrics and timestamp

**Command to Execute:**
```bash
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -f "DevOps Development/DBA/load_pincode_data.sql"

# Expected execution time: 2-5 minutes
# Estimated data size: ~500MB
```

**Expected Output:**
```
Step 1: Pre-load Verification...
[Constraints and indexes verified]

Step 2: Creating staging table...
Temp table created

Step 3: Loading data from CSV...
19,234 records loaded

Step 4: Validating data...
All records valid ✓
No NULL values in required fields ✓
All pincodes unique ✓

Step 5-12: [Processing steps...]

FINAL RESULTS:
==================
Total Records Loaded: 19,234
Load Time: 3.2 seconds
States: 36
Districts: 382
Cities: 1,523
Pincodes: 19,234
Status: ✓ SUCCESS
==================
```

**Verification Queries:**
```sql
-- Check total record count
SELECT COUNT(*) as total_records FROM State_City_PinCode_Master;
-- Expected: 19,234

-- Check by state
SELECT stateId, stateName, COUNT(*) as record_count
FROM State_City_PinCode_Master
GROUP BY stateId, stateName
ORDER BY stateId;
-- Expected: 36 states with varying record counts

-- Check district distribution
SELECT districtId, districtName, COUNT(*) as record_count
FROM State_City_PinCode_Master
WHERE stateId = 27
GROUP BY districtId, districtName
ORDER BY districtId;
-- Expected: Multiple districts in Maharashtra

-- Verify no NULL values
SELECT COUNT(*) FROM State_City_PinCode_Master
WHERE stateId IS NULL OR districtId IS NULL;
-- Expected: 0

-- Test query performance
EXPLAIN ANALYZE
SELECT * FROM State_City_PinCode_Master
WHERE stateId = 27 AND districtId = 1;
-- Expected: < 100ms execution time
```

---

## ✔️ PHASE 6.5: API VERIFICATION

**Task:** Test all location endpoints with loaded data

**API Endpoints to Verify:**

### 1. API 1: GET /api/v1/locations/all
```bash
curl -X GET "http://localhost:8000/api/v1/locations/all?state_id=27&limit=5" \
  -H "Accept: application/json"

# Expected Response:
# - status: "success"
# - code: 200
# - data.count: 5
# - data.locations[0].districtId: 1-3 (Maharashtra districts)
# - data.locations[0].districtName: "Mumbai", "Pune", "Nagpur", etc.
```

### 2. API 3.2: GET /api/v1/locations/districts/27
```bash
curl -X GET "http://localhost:8000/api/v1/locations/districts/27" \
  -H "Accept: application/json"

# Expected Response:
# - status: "success"
# - data.count: 35 (districts in Maharashtra)
# - data.districts[0]: {districtId: 1, districtName: "Mumbai", stateName: "Maharashtra"}
# - Multiple district records
```

### 3. API 3.3: GET /api/v1/locations/cities/1
```bash
curl -X GET "http://localhost:8000/api/v1/locations/cities/1" \
  -H "Accept: application/json"

# Expected Response:
# - status: "success"
# - data.count: 10+ (cities in district 1)
# - data.cities[0]: {cityId: 101, cityName: "Mumbai", districtName: "Mumbai", stateName: "Maharashtra"}
```

### 4. API 3.4: GET /api/v1/locations/by-district/1
```bash
curl -X GET "http://localhost:8000/api/v1/locations/by-district/1" \
  -H "Accept: application/json"

# Expected Response:
# - status: "success"
# - data.count: 100+ (pincodes in district 1)
# - data.pincodes[0]: {pinCode: 400001, cityName: "Mumbai", cityId: 101}
# - Organized by city
```

### 5. Run Unit Tests
```bash
# Navigate to project
cd "/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend"

# Run location tests
pytest "API Development/Unit Testing/test_locations_api.py" -v --tb=short

# Expected Results:
# - 65 tests pass
# - 0 failures
# - Coverage: All endpoints tested with real data
```

**Manual Verification Checklist:**
- [ ] API 1 returns district fields
- [ ] API 3.2 returns multiple districts
- [ ] API 3.3 returns multiple cities
- [ ] API 3.4 returns 100+ pincodes
- [ ] All responses have districtId and districtName
- [ ] Response times < 100ms
- [ ] All 65 unit tests pass

---

## 📊 EXECUTION SUMMARY

### Timeline
| Phase | Task | Duration |
|-------|------|----------|
| 6.1 | Backup verification | 5 min |
| 6.2 | Schema migration | 3 min |
| 6.3 | Data preparation | 15 min |
| 6.4 | Data loading | 5 min |
| 6.5 | API verification | 15 min |
| **Total** | **Complete Phase 6** | **~43 min** |

### Resources Required
- PostgreSQL client (psql)
- 500MB disk space (for data)
- Network access to 35.244.27.232:5432
- Python 3.11+ (for data transformation)

### Success Metrics
- [ ] 19,234 records loaded
- [ ] All 6 location endpoints working
- [ ] All 65 unit tests passing
- [ ] Response times < 100ms
- [ ] Schema verified with backup
- [ ] District hierarchy queries successful

---

## 🔄 ROLLBACK PLAN

### If Any Step Fails:

**6.1 Backup Failed:**
- No data modified yet
- Retry backup command

**6.2 Migration Failed:**
```sql
-- Restore from backup
DROP TABLE state_city_pincode_master;
ALTER TABLE State_City_PinCode_Master_Backup_Step1_1
RENAME TO state_city_pincode_master;
```

**6.3 Data Transformation Failed:**
- Review error log
- Check OGD data format
- Re-run transformer with corrections

**6.4 Data Loading Failed:**
```sql
-- Truncate and retry
TRUNCATE TABLE state_city_pincode_master;
-- Re-run data loading script
```

**6.5 API Tests Failed:**
- Check API logs
- Verify schema matches code
- Run migration again if needed

**Complete Rollback:**
```bash
# Restore entire database to pre-Phase 6 state
# Use DBA team full backup from previous date
```

---

## ✅ APPROVAL & EXECUTION

**Pre-Execution Sign-off:**
- [x] All code changes committed
- [x] All scripts prepared
- [x] Database backups planned
- [x] Rollback procedures documented
- [x] Verification tests prepared

**Ready for Execution: YES**

**Next Step:** Execute Phase 6.1-6.5 in sequence

---

**Prepared:** March 3, 2026
**Prepared by:** Step 1.1 Implementation Team
**Status:** READY FOR EXECUTION

