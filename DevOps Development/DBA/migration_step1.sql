-- ============================================================================
-- Migration Script: State_City_PinCode_Master Schema Update
-- Date: March 2, 2026
-- Description: Migrate from VARCHAR to INTEGER data types and change PK to pinCode
-- ============================================================================

-- Connect to Medostel database
\c Medostel

-- ============================================================================
-- STEP 1: PRE-MIGRATION VERIFICATION
-- ============================================================================

\echo '--- STEP 1: PRE-MIGRATION VERIFICATION ---'

-- Check for NULL values in critical fields
\echo 'Checking for NULL values...'
SELECT 'NULL stateId count' as check_type, COUNT(*) as count
FROM State_City_PinCode_Master WHERE stateId IS NULL;

SELECT 'NULL cityId count' as check_type, COUNT(*) as count
FROM State_City_PinCode_Master WHERE cityId IS NULL;

SELECT 'NULL pinCode count' as check_type, COUNT(*) as count
FROM State_City_PinCode_Master WHERE pinCode IS NULL;

-- Check for duplicate pinCodes (violates future PK constraint)
\echo 'Checking for duplicate pinCodes...'
SELECT pinCode, COUNT(*) as duplicate_count
FROM State_City_PinCode_Master
GROUP BY pinCode
HAVING COUNT(*) > 1;

-- Verify pinCode is numeric format
\echo 'Checking for non-numeric pinCodes...'
SELECT COUNT(*) as non_numeric_count
FROM State_City_PinCode_Master
WHERE pinCode ~ '[^0-9]';

-- Current row count
\echo 'Current table row count:'
SELECT COUNT(*) as original_row_count FROM State_City_PinCode_Master;

-- ============================================================================
-- STEP 2: CREATE BACKUP TABLE
-- ============================================================================

\echo '--- STEP 2: CREATE BACKUP TABLE ---'
CREATE TABLE IF NOT EXISTS State_City_PinCode_Master_Backup AS
SELECT * FROM State_City_PinCode_Master;

\echo 'Backup created. Row count:'
SELECT COUNT(*) as backup_row_count FROM State_City_PinCode_Master_Backup;

-- ============================================================================
-- STEP 3: DROP EXISTING INDEXES
-- ============================================================================

\echo '--- STEP 3: DROP EXISTING INDEXES ---'
DROP INDEX IF EXISTS idx_state_name;
DROP INDEX IF EXISTS idx_city_name;
DROP INDEX IF EXISTS idx_pincode;
DROP INDEX IF EXISTS idx_state_city;

\echo 'Indexes dropped successfully.'

-- ============================================================================
-- STEP 4: CREATE NEW TABLE WITH NEW SCHEMA
-- ============================================================================

\echo '--- STEP 4: CREATE NEW TABLE WITH NEW SCHEMA ---'
CREATE TABLE State_City_PinCode_Master_New (
    pinCode INTEGER PRIMARY KEY,
    stateId INTEGER NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    cityId INTEGER NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
        CHECK (status IN ('Active', 'Inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

\echo 'New table created successfully.'

-- ============================================================================
-- STEP 5: MIGRATE DATA WITH TYPE CONVERSION
-- ============================================================================

\echo '--- STEP 5: MIGRATE DATA WITH TYPE CONVERSION ---'
INSERT INTO State_City_PinCode_Master_New
(pinCode, stateId, stateName, cityName, cityId, countryName, status, createdDate, updatedDate)
SELECT
    CAST(pinCode AS INTEGER),
    CAST(stateId AS INTEGER),
    stateName,
    cityName,
    CAST(cityId AS INTEGER),
    countryName,
    status,
    createdDate,
    updatedDate
FROM State_City_PinCode_Master;

\echo 'Data migration completed. Row count:'
SELECT COUNT(*) as new_table_row_count FROM State_City_PinCode_Master_New;

-- ============================================================================
-- STEP 6: VERIFY DATA INTEGRITY
-- ============================================================================

\echo '--- STEP 6: VERIFY DATA INTEGRITY ---'

-- Row count comparison
\echo 'Row count verification:'
SELECT
    (SELECT COUNT(*) FROM State_City_PinCode_Master) as original_count,
    (SELECT COUNT(*) FROM State_City_PinCode_Master_New) as new_count,
    CASE
        WHEN (SELECT COUNT(*) FROM State_City_PinCode_Master) =
             (SELECT COUNT(*) FROM State_City_PinCode_Master_New)
        THEN 'PASS'
        ELSE 'FAIL'
    END as status;

-- Check for NULL values in new table
\echo 'Checking for NULL values in new table:'
SELECT
    (SELECT COUNT(*) FROM State_City_PinCode_Master_New WHERE stateId IS NULL) as null_stateId,
    (SELECT COUNT(*) FROM State_City_PinCode_Master_New WHERE cityId IS NULL) as null_cityId,
    (SELECT COUNT(*) FROM State_City_PinCode_Master_New WHERE pinCode IS NULL) as null_pinCode;

-- Verify pinCode format (5-6 digits for Indian postal codes)
\echo 'Checking pinCode format (should be 5-6 digits):'
SELECT
    COUNT(*) as invalid_format
FROM State_City_PinCode_Master_New
WHERE pinCode < 100000 OR pinCode > 999999;

-- Check for duplicate pinCodes
\echo 'Checking for duplicate pinCodes:'
SELECT
    COUNT(*) as duplicate_pincode_count
FROM (
    SELECT pinCode, COUNT(*) as count
    FROM State_City_PinCode_Master_New
    GROUP BY pinCode
    HAVING COUNT(*) > 1
) duplicates;

-- Sample data verification
\echo 'Sample data from new table:'
SELECT * FROM State_City_PinCode_Master_New LIMIT 3;

-- ============================================================================
-- STEP 7: RENAME TABLES (ATOMIC OPERATION)
-- ============================================================================

\echo '--- STEP 7: RENAME TABLES ---'
BEGIN TRANSACTION;

ALTER TABLE State_City_PinCode_Master RENAME TO State_City_PinCode_Master_Old;
ALTER TABLE State_City_PinCode_Master_New RENAME TO State_City_PinCode_Master;

COMMIT;

\echo 'Table rename completed successfully.'

-- ============================================================================
-- STEP 8: RECREATE INDEXES
-- ============================================================================

\echo '--- STEP 8: RECREATE INDEXES ---'
CREATE INDEX idx_state_name ON State_City_PinCode_Master(stateName);
CREATE INDEX idx_city_name ON State_City_PinCode_Master(cityName);
CREATE INDEX idx_state_id ON State_City_PinCode_Master(stateId);
CREATE INDEX idx_city_id ON State_City_PinCode_Master(cityId);
CREATE INDEX idx_state_city ON State_City_PinCode_Master(stateId, cityId);
CREATE INDEX idx_status ON State_City_PinCode_Master(status);

\echo 'Indexes recreated successfully.'

-- ============================================================================
-- STEP 9: POST-MIGRATION VALIDATION
-- ============================================================================

\echo '--- STEP 9: POST-MIGRATION VALIDATION ---'

-- Verify all indexes exist
\echo 'Verifying indexes:'
SELECT indexname, tablename
FROM pg_indexes
WHERE tablename = 'State_City_PinCode_Master'
ORDER BY indexname;

-- Test sample queries
\echo 'Testing sample queries:'

-- Query 1: Get all locations for a specific state
SELECT COUNT(*) as state_locations
FROM State_City_PinCode_Master
WHERE stateId = (SELECT stateId FROM State_City_PinCode_Master LIMIT 1);

-- Query 2: Get all pinCodes for a specific city
SELECT COUNT(*) as city_pincodes
FROM State_City_PinCode_Master
WHERE cityId = (SELECT cityId FROM State_City_PinCode_Master LIMIT 1);

-- Query 3: Get specific pinCode
SELECT COUNT(*) as specific_pincode_count
FROM State_City_PinCode_Master
WHERE pinCode = (SELECT pinCode FROM State_City_PinCode_Master LIMIT 1);

-- Table statistics
\echo 'Table statistics:'
SELECT
    pg_size_pretty(pg_total_relation_size('State_City_PinCode_Master')) as table_size,
    (SELECT COUNT(*) FROM State_City_PinCode_Master) as row_count;

-- ============================================================================
-- STEP 10: CLEANUP (OPTIONAL - UNCOMMENT AFTER SUCCESSFUL VALIDATION)
-- ============================================================================

\echo '--- STEP 10: CLEANUP (OPTIONAL) ---'
\echo 'To clean up backup tables after successful migration, uncomment and run:'
\echo '-- DROP TABLE IF EXISTS State_City_PinCode_Master_Backup;'
\echo '-- DROP TABLE IF EXISTS State_City_PinCode_Master_Old;'

-- ============================================================================
-- MIGRATION COMPLETION SUMMARY
-- ============================================================================

\echo ''
\echo '================================================================================'
\echo 'MIGRATION COMPLETED SUCCESSFULLY'
\echo '================================================================================'
\echo 'Date: March 2, 2026'
\echo 'Table: State_City_PinCode_Master'
\echo 'Changes:'
\echo '  - pinCode: Changed from SERIAL id to INTEGER PRIMARY KEY'
\echo '  - stateId: Changed from VARCHAR(10) to INTEGER'
\echo '  - cityId: Changed from VARCHAR(10) to INTEGER'
\echo '  - Removed: id (SERIAL) column'
\echo '  - Added indexes: idx_state_id, idx_city_id, idx_status'
\echo '================================================================================'
\echo ''
\echo 'Final Row Count:'
SELECT COUNT(*) FROM State_City_PinCode_Master;

\echo ''
\echo 'Migration script completed at:' || NOW()::TEXT;
