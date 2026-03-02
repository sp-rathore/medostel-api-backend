# Phase 6: Data Loading & Verification - Execution Guide

**Step 1.1 Implementation Plan**
**Version:** 1.0
**Date:** March 3, 2026
**Status:** Ready for Execution

---

## 📋 Pre-Execution Checklist

### Database Prerequisites
- [x] PostgreSQL instance running (35.244.27.232:5432)
- [x] Medostel database exists
- [x] medostel_api_user has proper permissions
- [x] Network connectivity verified

### Infrastructure
- [x] Migration script created (migration_step1_1.sql)
- [x] Data loading script created (load_pincode_data.sql)
- [x] Data transformation script created (pin_code_data_transformer.py)
- [x] Backup procedures documented
- [x] Rollback procedures documented

### API Code
- [x] Location schemas updated (districtId, districtName)
- [x] Location service methods updated (6 endpoints)
- [x] Location routes updated (15 endpoint handlers)
- [x] Tests created (65 location tests)
- [x] Fixtures updated (8 location fixtures)

### Documentation
- [x] API specifications updated (15 APIs)
- [x] Test documentation updated (65 tests)
- [x] Database schema documentation updated

---

## 🗄️ Database Connection Details

```
Host:           35.244.27.232
Port:           5432
Database:       medostel
User:           medostel_api_user
Password:       Iag2bMi@6aD
Instance:       medostel-ai-assistant-pgdev-instance
```

**Connection String:**
```
postgresql://medostel_api_user:Iag2bMi@6aD@35.244.27.232:5432/medostel
```

---

## 🔄 Execution Plan

### PHASE 6.1: Pre-Migration Backup

**Objective:** Create full database backup before schema changes

**Steps:**
1. Connect to PostgreSQL database
2. Create backup of State_City_PinCode_Master table
3. Verify backup count matches current record count
4. Save backup for rollback if needed

**Scripts:**
- Migration script includes automatic backup (Step 2 in migration_step1_1.sql)
- Backup table: `State_City_PinCode_Master_Backup_Step1_1`

---

### PHASE 6.2: Database Schema Migration

**Objective:** Add districtId and districtName columns to State_City_PinCode_Master

**Migration Changes:**
1. Add `districtId` (INTEGER)
2. Add `districtName` (VARCHAR(100))
3. Create 6 new indexes for hierarchical queries:
   - idx_districtId
   - idx_districtName
   - idx_state_district
   - idx_district_city
   - idx_state_district_city
   - idx_district_status

**Script Location:** `DevOps Development/DBA/migration_step1_1.sql`

**Execution Method:**
```bash
# Option 1: Using psql command line
psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -f "DevOps Development/DBA/migration_step1_1.sql"

# Option 2: Using SQL client GUI
# Open the SQL file in pgAdmin or DBeaver and execute
```

**Expected Output:**
- Backup table created with existing records
- 2 new columns added to state_city_pincode_master
- 6 new indexes created
- Schema verified successfully

**Rollback Procedure:**
```sql
-- If migration fails, restore from backup:
DROP TABLE state_city_pincode_master;
ALTER TABLE State_City_PinCode_Master_Backup_Step1_1
RENAME TO state_city_pincode_master;
```

---

### PHASE 6.3: Data Preparation & Transformation

**Objective:** Extract OGD data and transform into database-ready format

**Source Data:**
- Official Government Data (OGD) platform
- India postal codes with state, district, city information
- ~19,000 records expected

**Transformation Process:**

1. **Extract from OGD:**
   - Download CSV file from OGD portal
   - Save to: `Data Extraction/ogd_india_pincodes.csv`

2. **Transform Data:**
   ```bash
   cd "Data Extraction"
   python pin_code_data_transformer.py
   ```

   **Outputs:**
   - `cleaned_data.csv` - Processed data with hierarchical IDs
   - `data_transformation_report.txt` - Quality metrics and validation

3. **Transformation Logic:**
   - Assign sequential numeric IDs:
     * Country: 0001
     * State: 0001-0035
     * District: 0001-N per state
     * City: 0001-N per district
     * PinCode: 6-digit numeric
   - Remove duplicates and invalid entries
   - Extract proper city names (not post office names)
   - Validate data integrity

---

### PHASE 6.4: Data Loading

**Objective:** Load transformed data into database

**Script Location:** `DevOps Development/DBA/load_pincode_data.sql`

**Data Loading Process (12 Steps):**

1. **Pre-load Verification** - Check constraints and indexes
2. **Create Temp Table** - Staging area for CSV data
3. **Load CSV Data** - COPY transformed data into temp table
4. **Data Validation** - Verify data quality
5. **NOT NULL Constraints** - Apply after data validated
6. **Update Statistics** - Prepare indexes for queries
7. **Index Verification** - Confirm all indexes built
8. **Cleanup** - Remove temporary tables
9. **Final Count** - Verify all 19,000+ records loaded
10. **Performance Tests** - Run sample queries
11. **Backup Post-Load** - Create backup after successful load
12. **Documentation** - Record load date and metrics

**Execution:**
```bash
# Using PostgreSQL COPY (Fastest method - recommended)
# This method is built into load_pincode_data.sql

psql -h 35.244.27.232 -p 5432 -U medostel_api_user -d medostel \
  -f "DevOps Development/DBA/load_pincode_data.sql"
```

**Expected Results:**
- ~19,000 records loaded into state_city_pincode_master
- Load time: 2-5 minutes (depending on network)
- All 6 indexes created and optimized
- Zero data integrity violations
- All queries returning expected results

---

### PHASE 6.5: API Verification

**Objective:** Test all 6 location endpoints with loaded data

**Verification Tests:**

1. **API 1: GET /api/v1/locations/all**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/locations/all?state_id=27&limit=10" \
     -H "Accept: application/json"

   # Expected: Return 10 locations from Maharashtra
   # Verify: districtId, districtName in response
   ```

2. **API 3.2: GET /api/v1/locations/districts/27**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/locations/districts/27" \
     -H "Accept: application/json"

   # Expected: Return all districts in Maharashtra
   # Verify: Multiple districtId values (1, 2, 3, etc.)
   ```

3. **API 3.3: GET /api/v1/locations/cities/1**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/locations/cities/1" \
     -H "Accept: application/json"

   # Expected: Return all cities in district 1
   # Verify: Multiple cityName values
   ```

4. **API 3.4: GET /api/v1/locations/by-district/1**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/locations/by-district/1" \
     -H "Accept: application/json"

   # Expected: Return all pincodes in district 1
   # Verify: 100+ pincode records organized by city
   ```

5. **Run Unit Tests:**
   ```bash
   # Run all location tests
   pytest "API Development/Unit Testing/test_locations_api.py" -v

   # Expected: 65 tests pass
   # Coverage: All 6 endpoints tested
   ```

---

## ⚠️ Risk Mitigation

| Risk | Mitigation Strategy |
|------|-------------------|
| Data loss during migration | Automatic backup created before changes |
| Schema incompatibility | Migration verified with dummy data first |
| Performance degradation | Indexes created to optimize queries |
| Data validation failures | Pre-load validation catches issues |
| Network interruption | Transaction rollback available |
| Duplicate pincode values | Data transformation removes duplicates |

---

## 📊 Success Criteria

### Migration Success
- [ ] 2 new columns added to state_city_pincode_master
- [ ] 6 new indexes created
- [ ] Backup table created with correct record count
- [ ] Schema verified successfully

### Data Loading Success
- [ ] ~19,000 records loaded
- [ ] Zero validation errors
- [ ] All NOT NULL constraints satisfied
- [ ] All indexes built and optimized
- [ ] Query performance verified (< 100ms)

### API Verification Success
- [ ] GET /api/v1/locations/all returns district fields
- [ ] GET /api/v1/locations/districts/{state_id} returns results
- [ ] GET /api/v1/locations/cities/{district_id} returns results
- [ ] GET /api/v1/locations/by-district/{district_id} returns results
- [ ] All 65 unit tests pass
- [ ] Response times < 100ms for all queries

### Overall Success
- [ ] Database schema matches API code expectations
- [ ] All 6 location endpoints return valid data
- [ ] Hierarchical queries work correctly
- [ ] Performance baselines met
- [ ] Documentation updated with load metrics

---

## 📅 Estimated Timeline

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 6.1 | Pre-migration backup | 5 min | Automated |
| 6.2 | Schema migration | 2-3 min | Manual |
| 6.3 | OGD data extraction | 10 min | Manual |
| 6.3 | Data transformation | 3-5 min | Script |
| 6.4 | Data loading | 2-5 min | Script |
| 6.5 | API verification | 10 min | Manual |
| **Total** | **Complete Phase 6** | **32-38 min** | **Ready** |

---

## 📝 Rollback Procedures

### If Migration Fails:
1. Database transactions automatically rollback
2. Use backup table if manual rollback needed:
   ```sql
   DROP TABLE state_city_pincode_master;
   ALTER TABLE State_City_PinCode_Master_Backup_Step1_1
   RENAME TO state_city_pincode_master;
   ```

### If Data Loading Fails:
1. Restore pre-load backup
2. Check data transformation for errors
3. Re-run transformation with corrections
4. Attempt data loading again

### Complete Rollback:
1. Restore entire database from full backup
2. Redeploy API without district support
3. Use migration_step1_1.sql to document rollback date

---

## 🎯 Next Steps

1. **Execute Step 6.1-6.2:** Database migration
2. **Execute Step 6.3:** Data preparation
3. **Execute Step 6.4:** Data loading
4. **Execute Step 6.5:** API verification
5. **Document Results:** Record execution metrics
6. **Proceed to Phase 7:** Version control and final commits

---

**Ready to proceed?**
- [ ] Pre-execution checklist confirmed
- [ ] Backup procedures understood
- [ ] Rollback procedures reviewed
- [ ] All scripts location verified

**Approved by:** _______________
**Date:** _______________
**Notes:** _______________

