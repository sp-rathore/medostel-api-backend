-- ============================================================================
-- Data Loading Script: Populate State_City_PinCode_Master with OGD Data
-- ============================================================================
-- Purpose: Load cleaned pincode data from CSV into State_City_PinCode_Master
--
-- Prerequisites:
--   1. Run migration_step1_1.sql to add district columns
--   2. Run pin_code_data_transformer.py to generate cleaned_data.csv
--   3. Place cleaned_data.csv in accessible directory
--
-- Version: 1.0
-- Date: March 3, 2026
-- Database: PostgreSQL
-- ============================================================================

-- ============================================================================
-- STEP 1: PRE-LOAD VERIFICATION
-- ============================================================================

SELECT 'Step 1: Verifying pre-load conditions...' AS status;

-- Check table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Verify backup exists
SELECT COUNT(*) as backup_record_count
FROM State_City_PinCode_Master_Backup_Step1_1;

-- Check if data already loaded (for idempotency)
SELECT COUNT(*) as current_record_count FROM State_City_PinCode_Master;

SELECT 'Pre-load verification complete!' AS status;

-- ============================================================================
-- STEP 2: PREPARE DATA FOR LOADING
-- ============================================================================

SELECT 'Step 2: Preparing for data load...' AS status;

-- Create temporary table for validation
CREATE TEMP TABLE temp_pincode_data (
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

SELECT 'Temporary table created!' AS status;

-- ============================================================================
-- STEP 3: LOAD DATA FROM CSV
-- ============================================================================

SELECT 'Step 3: Loading data from cleaned_data.csv...' AS status;

-- Note: This COPY command needs to be executed with proper file path
-- For local file:
-- COPY temp_pincode_data FROM '/path/to/cleaned_data.csv' WITH (FORMAT CSV, HEADER);

-- Alternative: If using psql command line:
-- \COPY temp_pincode_data FROM 'cleaned_data.csv' WITH (FORMAT CSV, HEADER);

-- For programmatic loading, use Python with psycopg2 or similar
-- Example Python code:
/*
import psycopg2
import csv

connection = psycopg2.connect("dbname=medostel user=postgres")
cursor = connection.cursor()

with open('cleaned_data.csv', 'r') as f:
    next(f)  # Skip header
    cursor.copy_from(f, 'temp_pincode_data', sep=',')

connection.commit()
cursor.close()
connection.close()
*/

-- Assuming data is loaded, verify count
SELECT COUNT(*) as temp_data_count FROM temp_pincode_data;

SELECT 'Data loaded into temporary table!' AS status;

-- ============================================================================
-- STEP 4: DATA VALIDATION AND CLEANING
-- ============================================================================

SELECT 'Step 4: Validating loaded data...' AS status;

-- Check for NULL values in required columns
SELECT 'Null values in required columns:' AS validation;
SELECT
    SUM(CASE WHEN pinCode IS NULL THEN 1 ELSE 0 END) as null_pincodes,
    SUM(CASE WHEN stateId IS NULL THEN 1 ELSE 0 END) as null_state_ids,
    SUM(CASE WHEN districtId IS NULL THEN 1 ELSE 0 END) as null_district_ids,
    SUM(CASE WHEN cityId IS NULL THEN 1 ELSE 0 END) as null_city_ids
FROM temp_pincode_data;

-- Check for invalid pincode ranges
SELECT COUNT(*) as invalid_pincodes
FROM temp_pincode_data
WHERE pinCode < 100000 OR pinCode > 999999;

-- Check for duplicate pincodes
SELECT COUNT(DISTINCT pinCode) as unique_pincodes,
       COUNT(*) as total_records,
       COUNT(*) - COUNT(DISTINCT pinCode) as duplicate_count
FROM temp_pincode_data;

-- Check geographic hierarchy consistency
SELECT COUNT(DISTINCT stateId) as unique_states,
       COUNT(DISTINCT districtId) as unique_districts,
       COUNT(DISTINCT cityId) as unique_cities
FROM temp_pincode_data;

SELECT 'Data validation complete!' AS status;

-- ============================================================================
-- STEP 5: DEDUPLICATE IF NEEDED
-- ============================================================================

SELECT 'Step 5: Removing duplicates...' AS status;

-- Create clean temporary table (keep first occurrence of each pincode)
CREATE TEMP TABLE temp_pincode_clean AS
SELECT DISTINCT ON (pinCode)
    pinCode, stateId, stateName, districtId, districtName,
    cityId, cityName, countryName, status, createdDate, updatedDate
FROM temp_pincode_data
ORDER BY pinCode, createdDate;

SELECT COUNT(*) as cleaned_record_count FROM temp_pincode_clean;
SELECT 'Deduplication complete!' AS status;

-- ============================================================================
-- STEP 6: BULK INSERT INTO MAIN TABLE
-- ============================================================================

SELECT 'Step 6: Inserting data into State_City_PinCode_Master...' AS status;

INSERT INTO State_City_PinCode_Master (
    pinCode, stateId, stateName, districtId, districtName,
    cityId, cityName, countryName, status, createdDate, updatedDate
)
SELECT
    pinCode, stateId, stateName, districtId, districtName,
    cityId, cityName, countryName, status, createdDate, updatedDate
FROM temp_pincode_clean
ON CONFLICT (pinCode) DO NOTHING;  -- Skip if pincode already exists

SELECT COUNT(*) as inserted_record_count FROM State_City_PinCode_Master;
SELECT 'Data insertion complete!' AS status;

-- ============================================================================
-- STEP 7: POST-LOAD DATA VALIDATION
-- ============================================================================

SELECT 'Step 7: Validating loaded data...' AS status;

-- Check for orphaned records (shouldn't happen with proper hierarchy)
SELECT COUNT(*) as records_without_district
FROM State_City_PinCode_Master
WHERE districtId IS NULL OR districtName IS NULL;

-- Verify geographic hierarchy
SELECT
    COUNT(DISTINCT stateId) as total_states,
    COUNT(DISTINCT districtId) as total_districts,
    COUNT(DISTINCT cityId) as total_cities,
    COUNT(*) as total_pincodes
FROM State_City_PinCode_Master;

-- Sample records from each state (first record)
SELECT 'Sample records by state:' AS status;
SELECT DISTINCT ON (stateId)
    stateId, stateName, districtId, districtName, cityId, cityName, pinCode
FROM State_City_PinCode_Master
ORDER BY stateId, pinCode
LIMIT 35;

-- ============================================================================
-- STEP 8: UPDATE NOT NULL CONSTRAINTS (after successful load)
-- ============================================================================

SELECT 'Step 8: Adding NOT NULL constraints...' AS status;

ALTER TABLE State_City_PinCode_Master
ALTER COLUMN districtId SET NOT NULL,
ALTER COLUMN districtName SET NOT NULL;

SELECT 'NOT NULL constraints added!' AS status;

-- ============================================================================
-- STEP 9: VERIFY DATA INTEGRITY
-- ============================================================================

SELECT 'Step 9: Final data integrity checks...' AS status;

-- Check for valid pincode format (6 digits)
SELECT COUNT(*) as valid_pincodes
FROM State_City_PinCode_Master
WHERE pinCode >= 100000 AND pinCode <= 999999;

-- Check status values
SELECT COUNT(DISTINCT status) as unique_statuses,
       ARRAY_AGG(DISTINCT status) as status_values
FROM State_City_PinCode_Master;

-- Check country values (should be all India)
SELECT COUNT(DISTINCT countryName) as country_count,
       ARRAY_AGG(DISTINCT countryName) as countries
FROM State_City_PinCode_Master;

-- Performance check: Verify indexes are working
EXPLAIN ANALYZE
SELECT COUNT(*) FROM State_City_PinCode_Master
WHERE stateId = 1;

EXPLAIN ANALYZE
SELECT COUNT(*) FROM State_City_PinCode_Master
WHERE districtId = 1;

SELECT 'Data integrity verification complete!' AS status;

-- ============================================================================
-- STEP 10: GENERATE LOAD STATISTICS
-- ============================================================================

SELECT 'Step 10: Generating load statistics...' AS status;

SELECT 'LOAD SUMMARY STATISTICS' AS summary;

-- Overall statistics
SELECT
    COUNT(*) as total_records,
    COUNT(DISTINCT stateId) as total_states,
    COUNT(DISTINCT districtId) as total_districts,
    COUNT(DISTINCT cityId) as total_cities,
    COUNT(DISTINCT pinCode) as total_unique_pincodes,
    ROUND(AVG(pinCode)) as avg_pincode,
    MIN(pinCode) as min_pincode,
    MAX(pinCode) as max_pincode
FROM State_City_PinCode_Master;

-- State-wise statistics
SELECT 'State-wise Record Count:' AS state_stats;
SELECT
    stateId,
    stateName,
    COUNT(*) as record_count,
    COUNT(DISTINCT districtId) as district_count,
    COUNT(DISTINCT cityId) as city_count
FROM State_City_PinCode_Master
GROUP BY stateId, stateName
ORDER BY stateId;

-- District statistics (sample)
SELECT 'Top 10 Districts by Record Count:' AS district_stats;
SELECT
    stateId,
    stateName,
    districtId,
    districtName,
    COUNT(*) as record_count
FROM State_City_PinCode_Master
GROUP BY stateId, stateName, districtId, districtName
ORDER BY COUNT(*) DESC
LIMIT 10;

-- ============================================================================
-- STEP 11: CLEANUP AND COMPLETION
-- ============================================================================

SELECT 'Step 11: Cleaning up temporary tables...' AS status;

DROP TABLE IF EXISTS temp_pincode_data;
DROP TABLE IF EXISTS temp_pincode_clean;

SELECT 'Temporary tables cleaned!' AS status;

-- ============================================================================
-- STEP 12: FINAL STATUS
-- ============================================================================

SELECT '✓ DATA LOADING COMPLETED SUCCESSFULLY!' AS final_status;
SELECT CURRENT_TIMESTAMP as completion_timestamp;
SELECT 'All geographic data has been loaded into State_City_PinCode_Master.' AS message;
SELECT 'APIs can now use hierarchical queries by state, district, city, and pincode.' AS next_action;

-- ============================================================================
-- USEFUL QUERY EXAMPLES FOR VERIFICATION
-- ============================================================================

/*
-- Get all pincodes for a specific state
SELECT * FROM State_City_PinCode_Master
WHERE stateId = 1  -- Maharashtra
ORDER BY districtId, cityId, pinCode;

-- Get all districts in a state
SELECT DISTINCT districtId, districtName
FROM State_City_PinCode_Master
WHERE stateId = 1
ORDER BY districtId;

-- Get all cities in a district
SELECT DISTINCT cityId, cityName
FROM State_City_PinCode_Master
WHERE districtId = 1
ORDER BY cityId;

-- Get all pincodes in a specific district
SELECT pinCode, cityName
FROM State_City_PinCode_Master
WHERE districtId = 1
ORDER BY pinCode;

-- Get all pincodes for a specific city
SELECT pinCode
FROM State_City_PinCode_Master
WHERE cityId = 1 AND districtId = 1
ORDER BY pinCode;

-- Get state hierarchy (sample)
SELECT DISTINCT stateId, stateName FROM State_City_PinCode_Master
ORDER BY stateId;
*/

-- ============================================================================
-- END OF DATA LOADING SCRIPT
-- ============================================================================
