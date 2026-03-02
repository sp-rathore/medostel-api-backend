# Migration Strategy: State_City_PinCode_Master Schema Update

**Version:** 1.0
**Date:** March 2, 2026
**Status:** Ready for Execution
**Type:** Database Schema Refactoring

---

## Executive Summary

This document outlines the migration strategy for updating the State_City_PinCode_Master table schema from VARCHAR to INTEGER data types and changing the primary key from 'id' (SERIAL) to 'pinCode' (INTEGER).

## Current State (Before Migration)

### Table Schema
```sql
CREATE TABLE State_City_PinCode_Master (
    id SERIAL PRIMARY KEY,
    stateId VARCHAR(10) NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    cityId VARCHAR(10) NOT NULL,
    pinCode VARCHAR(10) NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Issues
1. **Data Types:** stateId, cityId, and pinCode are VARCHAR(10) - not ideal for numeric data
2. **Primary Key:** Numeric 'id' field is less meaningful; pinCode should be PK
3. **Redundancy:** Numeric data stored as strings consumes more storage
4. **Performance:** VARCHAR comparisons slower than INTEGER comparisons

### Current Indexes
- idx_state_name on stateName
- idx_city_name on cityName
- idx_pincode on pinCode (unique but not PK)
- idx_state_city on (stateId, cityId)

---

## Target State (After Migration)

### New Table Schema
```sql
CREATE TABLE State_City_PinCode_Master (
    pinCode INTEGER PRIMARY KEY,
    stateId INTEGER NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    cityId INTEGER NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Benefits
1. **Data Type Correctness:** Numeric fields stored as INTEGER
2. **Better Primary Key:** pinCode is unique and meaningful
3. **Storage Efficiency:** INTEGER (4 bytes) vs VARCHAR(10) (11+ bytes)
4. **Performance:** Faster comparisons and joins
5. **Validation:** PostgreSQL enforces numeric constraints

### New Indexes
- idx_state_name on stateName
- idx_city_name on cityName
- idx_state_id on stateId
- idx_city_id on cityId
- idx_state_city on (stateId, cityId)
- idx_status on status

---

## Migration Steps

### Step 1: Pre-Migration Verification
**Purpose:** Ensure data integrity before migration

```sql
-- Check for NULL values in critical fields
SELECT COUNT(*) as null_state_id FROM State_City_PinCode_Master WHERE stateId IS NULL;
SELECT COUNT(*) as null_city_id FROM State_City_PinCode_Master WHERE cityId IS NULL;
SELECT COUNT(*) as null_pincode FROM State_City_PinCode_Master WHERE pinCode IS NULL;

-- Check for duplicate pinCodes (violates future PK constraint)
SELECT pinCode, COUNT(*) as count FROM State_City_PinCode_Master
GROUP BY pinCode HAVING COUNT(*) > 1;

-- Verify pinCode is numeric format (no non-numeric characters)
SELECT COUNT(*) as non_numeric FROM State_City_PinCode_Master
WHERE pinCode ~ '[^0-9]';

-- Check existing data types and sizes
SELECT
    column_name,
    data_type,
    character_maximum_length
FROM information_schema.columns
WHERE table_name = 'State_City_PinCode_Master';
```

### Step 2: Create Backup
**Purpose:** Ensure rollback capability

```sql
-- Create backup table
CREATE TABLE State_City_PinCode_Master_Backup AS
SELECT * FROM State_City_PinCode_Master;

-- Create backup of indexes
-- Note: Backup reference for recreation if needed
-- Current indexes: idx_state_name, idx_city_name, idx_pincode, idx_state_city
```

### Step 3: Disable Constraints & Indexes
**Purpose:** Speed up data migration

```sql
-- Drop dependent foreign keys (if any)
-- ALTER TABLE other_tables DROP CONSTRAINT fk_location_id;

-- Drop existing indexes
DROP INDEX IF EXISTS idx_state_name;
DROP INDEX IF EXISTS idx_city_name;
DROP INDEX IF EXISTS idx_pincode;
DROP INDEX IF EXISTS idx_state_city;

-- Disable triggers (if any) to speed up migration
-- ALTER TABLE State_City_PinCode_Master DISABLE TRIGGER ALL;
```

### Step 4: Create New Table with New Schema
**Purpose:** Build target table with proper schema

```sql
CREATE TABLE State_City_PinCode_Master_New (
    pinCode INTEGER PRIMARY KEY,
    stateId INTEGER NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    cityId INTEGER NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 5: Data Migration with Type Conversion
**Purpose:** Convert data types and populate new table

```sql
-- Migrate data with type conversion
INSERT INTO State_City_PinCode_Master_New
(pinCode, stateId, stateName, cityName, cityId, countryName, status, createdDate, updatedDate)
SELECT
    CAST(pinCode AS INTEGER),           -- Convert pinCode to INTEGER
    CAST(stateId AS INTEGER),           -- Convert stateId to INTEGER
    stateName,
    cityName,
    CAST(cityId AS INTEGER),            -- Convert cityId to INTEGER
    countryName,
    status,
    createdDate,
    updatedDate
FROM State_City_PinCode_Master;

-- Verify row count matches
SELECT 'Original table row count:' as check_point, COUNT(*) FROM State_City_PinCode_Master
UNION ALL
SELECT 'New table row count:', COUNT(*) FROM State_City_PinCode_Master_New;
```

### Step 6: Verify Data Integrity
**Purpose:** Ensure no data was lost or corrupted

```sql
-- Check for data mismatches
SELECT
    CASE
        WHEN (SELECT COUNT(*) FROM State_City_PinCode_Master) =
             (SELECT COUNT(*) FROM State_City_PinCode_Master_New)
        THEN 'Row count matches'
        ELSE 'Row count MISMATCH - ABORT!'
    END as verification;

-- Verify numeric values are valid (5-6 digits for Indian pinCodes)
SELECT COUNT(*) as invalid_pincode_format
FROM State_City_PinCode_Master_New
WHERE pinCode < 100000 OR pinCode > 999999;

-- Check for NULL values in new table
SELECT COUNT(*) as null_stateId FROM State_City_PinCode_Master_New WHERE stateId IS NULL
UNION ALL
SELECT COUNT(*) as null_cityId FROM State_City_PinCode_Master_New WHERE cityId IS NULL
UNION ALL
SELECT COUNT(*) as null_pinCode FROM State_City_PinCode_Master_New WHERE pinCode IS NULL;
```

### Step 7: Rename Tables (Atomic Operation)
**Purpose:** Switch old table for new table in transaction

```sql
BEGIN TRANSACTION;

-- Rename old table to backup
ALTER TABLE State_City_PinCode_Master RENAME TO State_City_PinCode_Master_Old;

-- Rename new table to original name
ALTER TABLE State_City_PinCode_Master_New RENAME TO State_City_PinCode_Master;

COMMIT;
```

### Step 8: Recreate Indexes
**Purpose:** Restore query performance

```sql
CREATE INDEX idx_state_name ON State_City_PinCode_Master(stateName);
CREATE INDEX idx_city_name ON State_City_PinCode_Master(cityName);
CREATE INDEX idx_state_id ON State_City_PinCode_Master(stateId);
CREATE INDEX idx_city_id ON State_City_PinCode_Master(cityId);
CREATE INDEX idx_state_city ON State_City_PinCode_Master(stateId, cityId);
CREATE INDEX idx_status ON State_City_PinCode_Master(status);
```

### Step 9: Re-enable Triggers & Constraints
**Purpose:** Restore data protection rules

```sql
-- Re-enable triggers
-- ALTER TABLE State_City_PinCode_Master ENABLE TRIGGER ALL;

-- Add foreign key constraints if any other tables reference this
-- ALTER TABLE other_tables ADD CONSTRAINT fk_location_id
--   FOREIGN KEY (pinCode) REFERENCES State_City_PinCode_Master(pinCode);
```

### Step 10: Post-Migration Validation
**Purpose:** Confirm migration success

```sql
-- Verify indexes created successfully
SELECT indexname, tablename FROM pg_indexes
WHERE tablename = 'State_City_PinCode_Master'
ORDER BY indexname;

-- Test queries work correctly
SELECT * FROM State_City_PinCode_Master
WHERE stateId = 27 AND cityId = 102 LIMIT 5;

SELECT DISTINCT pinCode FROM State_City_PinCode_Master
WHERE cityName = 'Mumbai' ORDER BY pinCode;

-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('State_City_PinCode_Master')) as table_size;

-- Verify no duplicates exist for primary key
SELECT pinCode, COUNT(*) as count FROM State_City_PinCode_Master
GROUP BY pinCode HAVING COUNT(*) > 1;
```

---

## Rollback Procedure

If any issues are detected, rollback using this procedure:

```sql
BEGIN TRANSACTION;

-- Drop new (current) table
DROP TABLE IF EXISTS State_City_PinCode_Master;

-- Restore old table from backup
ALTER TABLE State_City_PinCode_Master_Old RENAME TO State_City_PinCode_Master;

-- Recreate original indexes
CREATE INDEX IF NOT EXISTS idx_state_name ON State_City_PinCode_Master(stateName);
CREATE INDEX IF NOT EXISTS idx_city_name ON State_City_PinCode_Master(cityName);
CREATE INDEX IF NOT EXISTS idx_pincode ON State_City_PinCode_Master(pinCode);
CREATE INDEX IF NOT EXISTS idx_state_city ON State_City_PinCode_Master(stateId, cityId);

COMMIT;

-- Verify restoration
SELECT COUNT(*) as row_count FROM State_City_PinCode_Master;
SELECT * FROM State_City_PinCode_Master LIMIT 1;
```

---

## Estimated Timeline

| Step | Duration | Notes |
|------|----------|-------|
| Pre-Migration Verification | 5 min | Quick checks |
| Backup Creation | 2-5 min | Depends on data size |
| Disable Indexes | 1 min | Quick operation |
| Create New Table | 1 min | Schema only |
| Data Migration | 5-15 min | Depends on row count |
| Verify Integrity | 5 min | Validation queries |
| Rename Tables | < 1 sec | Atomic operation |
| Recreate Indexes | 5-10 min | Index building |
| Post-Migration Tests | 5 min | Validation |
| **Total** | **30-50 minutes** | In development environment |

---

## Risk Assessment

### High Priority Risks
1. **Data Loss During Conversion**
   - Mitigation: Backup before migration, verify row counts

2. **Invalid Numeric Conversions**
   - Mitigation: Pre-migration verification of numeric format

3. **Duplicate pinCode Values**
   - Mitigation: Pre-migration duplicate check

### Medium Priority Risks
1. **Performance Degradation**
   - Mitigation: Index recreation and query performance testing

2. **Application Downtime**
   - Mitigation: Execute during maintenance window

### Low Priority Risks
1. **Index Fragmentation**
   - Mitigation: ANALYZE and VACUUM after migration

---

## Success Criteria

- ✅ Row count matches before and after
- ✅ No NULL values in stateId, cityId, or pinCode
- ✅ No duplicate pinCode values
- ✅ All indexes created successfully
- ✅ Query performance acceptable (< 100ms for standard queries)
- ✅ No errors in application logs
- ✅ All API tests passing with new schema

---

## Execution Approval

**Ready for execution:** March 2, 2026
**Approved by:** [To be filled]
**Executed on:** [To be filled]
**Status:** [To be filled]

---

## References

- PostgreSQL Data Type Conversion: https://www.postgresql.org/docs/current/sql-syntax.html
- Migration Best Practices: Internal documentation
- Current Schema: create_tables.sql
