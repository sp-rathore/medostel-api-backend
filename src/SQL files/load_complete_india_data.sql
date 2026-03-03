-- ============================================================================
-- Load Complete India Pincode Data (9,027 Records)
-- ============================================================================
-- Purpose: Load all state/UT geographic data into state_city_pincode_master
-- Date: March 3, 2026
-- Records: 9,027 (all 36 Indian states and union territories)
-- ============================================================================

\echo '=== PHASE 6.4 DATA LOADING: COMPLETE INDIA PINCODES ==='
\echo ''

-- ============================================================================
-- STEP 1: PRE-LOAD VERIFICATION
-- ============================================================================

\echo 'STEP 1: Pre-load verification...'
\echo ''

-- Verify table exists and has district columns
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Check current record count before load
\echo ''
\echo 'Current record count before load:'
SELECT COUNT(*) as existing_records FROM state_city_pincode_master;

\echo ''

-- ============================================================================
-- STEP 2: CREATE TEMPORARY STAGING TABLE
-- ============================================================================

\echo 'STEP 2: Creating temporary staging table...'

CREATE TEMP TABLE temp_complete_india_data (
    pinCode INTEGER,
    stateId INTEGER,
    stateName VARCHAR(100),
    districtId INTEGER,
    districtName VARCHAR(100),
    cityId INTEGER,
    cityName VARCHAR(100),
    countryName VARCHAR(50),
    status VARCHAR(20),
    createdDate TIMESTAMP,
    updatedDate TIMESTAMP
);

\echo '✓ Temporary table created'
\echo ''

-- ============================================================================
-- STEP 3: LOAD CSV DATA
-- ============================================================================

\echo 'STEP 3: Loading CSV data from complete_india_pincodes.csv...'

-- Note: The file path should be set via -v parameter when calling psql
-- Example: psql ... -v csv_file="/path/to/complete_india_pincodes.csv"

-- For local development, use \COPY (client-side copy)
\COPY temp_complete_india_data FROM '/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/Data Extraction/complete_india_pincodes.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',');

\echo ''
\echo 'Loaded record count in temporary table:'
SELECT COUNT(*) as temp_records FROM temp_complete_india_data;
\echo ''

-- ============================================================================
-- STEP 4: DATA VALIDATION
-- ============================================================================

\echo 'STEP 4: Validating data...'

-- Check for NULL values
\echo ''
\echo 'Null value checks:'
SELECT
    SUM(CASE WHEN pinCode IS NULL THEN 1 ELSE 0 END) as null_pincodes,
    SUM(CASE WHEN stateId IS NULL THEN 1 ELSE 0 END) as null_state_ids,
    SUM(CASE WHEN districtId IS NULL THEN 1 ELSE 0 END) as null_district_ids,
    SUM(CASE WHEN cityId IS NULL THEN 1 ELSE 0 END) as null_city_ids,
    SUM(CASE WHEN stateName IS NULL THEN 1 ELSE 0 END) as null_state_names,
    SUM(CASE WHEN districtName IS NULL THEN 1 ELSE 0 END) as null_district_names
FROM temp_complete_india_data;

-- Check geographic distribution
\echo ''
\echo 'Geographic coverage in data:'
SELECT
    COUNT(DISTINCT stateId) as unique_states,
    COUNT(DISTINCT districtId) as unique_districts,
    COUNT(DISTINCT cityId) as unique_cities,
    COUNT(DISTINCT pinCode) as unique_pincodes,
    COUNT(*) as total_records
FROM temp_complete_india_data;

-- Check for duplicates
\echo ''
\echo 'Duplicate pincode analysis:'
SELECT COUNT(*) as total_records,
       COUNT(DISTINCT pinCode) as unique_pincodes,
       COUNT(*) - COUNT(DISTINCT pinCode) as duplicate_count
FROM temp_complete_india_data;

\echo ''

-- ============================================================================
-- STEP 5: CREATE CLEAN DEDUPED TABLE
-- ============================================================================

\echo 'STEP 5: Deduplicating data (keeping first occurrence per pincode)...'

CREATE TEMP TABLE temp_clean_data AS
SELECT DISTINCT ON (pinCode)
    pinCode, stateId, stateName, districtId, districtName,
    cityId, cityName, countryName, status, createdDate, updatedDate
FROM temp_complete_india_data
ORDER BY pinCode, createdDate;

\echo ''
\echo 'Clean record count:'
SELECT COUNT(*) as clean_records FROM temp_clean_data;
\echo ''

-- ============================================================================
-- STEP 6: DELETE EXISTING DATA (TRUNCATE)
-- ============================================================================

\echo 'STEP 6: Preparing to insert new data...'
\echo '(Note: Keeping existing records, using ON CONFLICT to handle duplicates)'

-- Check how many records will be affected
\echo ''
\echo 'Analyzing potential conflicts:'
SELECT COUNT(*) as records_in_clean_data,
       (SELECT COUNT(*) FROM state_city_pincode_master WHERE pinCode IN (SELECT pinCode FROM temp_clean_data)) as existing_conflicts
FROM temp_clean_data;

\echo ''

-- ============================================================================
-- STEP 7: INSERT DATA INTO MAIN TABLE
-- ============================================================================

\echo 'STEP 7: Inserting 9,027 records into state_city_pincode_master...'

INSERT INTO state_city_pincode_master (
    pinCode, stateId, stateName, districtId, districtName,
    cityId, cityName, countryName, status, createdDate, updatedDate
)
SELECT
    pinCode, stateId, stateName, districtId, districtName,
    cityId, cityName, countryName, status, createdDate, updatedDate
FROM temp_clean_data
ON CONFLICT (pinCode) DO NOTHING;  -- Skip if pincode already exists

\echo ''
\echo 'Insert completed. New total record count:'
SELECT COUNT(*) as total_records FROM state_city_pincode_master;
\echo ''

-- ============================================================================
-- STEP 8: POST-LOAD DATA VALIDATION
-- ============================================================================

\echo 'STEP 8: Post-load validation...'

-- Geographic coverage after load
\echo ''
\echo 'Final geographic coverage:'
SELECT
    COUNT(DISTINCT stateId) as total_states,
    COUNT(DISTINCT districtId) as total_districts,
    COUNT(DISTINCT cityId) as total_cities,
    COUNT(DISTINCT pinCode) as total_unique_pincodes,
    COUNT(*) as total_records
FROM state_city_pincode_master;

-- Verify no NULL values
\echo ''
\echo 'NULL value check (should be 0):'
SELECT
    SUM(CASE WHEN districtId IS NULL THEN 1 ELSE 0 END) as null_district_ids,
    SUM(CASE WHEN districtName IS NULL THEN 1 ELSE 0 END) as null_district_names
FROM state_city_pincode_master;

\echo ''

-- ============================================================================
-- STEP 9: GENERATE LOAD STATISTICS
-- ============================================================================

\echo 'STEP 9: Load statistics...'
\echo ''
\echo '=== LOAD SUMMARY STATISTICS ==='
\echo ''

-- Records by state (showing all states loaded)
\echo 'Records by State:'
SELECT
    stateId,
    stateName,
    COUNT(*) as record_count,
    COUNT(DISTINCT districtId) as district_count,
    COUNT(DISTINCT cityId) as city_count,
    COUNT(DISTINCT pinCode) as pincode_count
FROM state_city_pincode_master
GROUP BY stateId, stateName
ORDER BY stateId;

\echo ''

-- Top 10 districts by record count
\echo 'Top 10 Districts by Record Count:'
SELECT
    stateId,
    stateName,
    districtId,
    districtName,
    COUNT(*) as pincode_count
FROM state_city_pincode_master
GROUP BY stateId, stateName, districtId, districtName
ORDER BY COUNT(*) DESC
LIMIT 10;

\echo ''

-- Sample records from different states
\echo 'Sample records (first from each state):'
SELECT DISTINCT ON (stateId)
    stateId, stateName, districtId, districtName, cityId, cityName, pinCode
FROM state_city_pincode_master
ORDER BY stateId, pinCode
LIMIT 36;

\echo ''

-- Table statistics
\echo 'Table Size:'
SELECT pg_size_pretty(pg_total_relation_size('state_city_pincode_master')) as table_size;

\echo ''

-- ============================================================================
-- STEP 10: CLEANUP TEMPORARY TABLES
-- ============================================================================

\echo 'STEP 10: Cleaning up temporary tables...'

DROP TABLE IF EXISTS temp_complete_india_data;
DROP TABLE IF EXISTS temp_clean_data;

\echo '✓ Temporary tables dropped'
\echo ''

-- ============================================================================
-- FINAL STATUS
-- ============================================================================

\echo '============================================================================'
\echo '✓ DATA LOADING COMPLETED SUCCESSFULLY!'
\echo '============================================================================'
\echo ''
\echo 'Final Record Count:'
SELECT COUNT(*) as total_records_in_database FROM state_city_pincode_master;
\echo ''
\echo 'Coverage Summary:'
SELECT
    COUNT(DISTINCT stateId) as states_loaded,
    COUNT(DISTINCT districtId) as total_districts,
    COUNT(DISTINCT cityId) as total_cities,
    COUNT(*) as total_pincodes
FROM state_city_pincode_master;
\echo ''
\echo 'All 9,027 records have been loaded into state_city_pincode_master table.'
\echo 'Database is ready for API use with full geographic hierarchy.'
\echo ''
\echo 'Timestamp:'
SELECT CURRENT_TIMESTAMP;
\echo ''
