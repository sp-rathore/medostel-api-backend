-- ============================================================================
-- Migration Script: Step 1.1 - Add District Columns to State_City_PinCode_Master
-- ============================================================================
-- Purpose: Add districtId and districtName columns to support hierarchical
--          geographic data structure (State -> District -> City -> PinCode)
--
-- Version: 1.0
-- Date: March 3, 2026
-- Database: PostgreSQL
-- ============================================================================

-- ============================================================================
-- STEP 1: PRE-MIGRATION VERIFICATION
-- ============================================================================

-- Check current table structure
SELECT 'Step 1: Verifying current table structure...' AS status;

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- Count existing records
SELECT COUNT(*) as existing_record_count FROM State_City_PinCode_Master;

-- ============================================================================
-- STEP 2: BACKUP EXISTING DATA
-- ============================================================================

SELECT 'Step 2: Creating backup table...' AS status;

CREATE TABLE IF NOT EXISTS State_City_PinCode_Master_Backup_Step1_1 AS
SELECT * FROM State_City_PinCode_Master;

SELECT COUNT(*) as backup_record_count FROM State_City_PinCode_Master_Backup_Step1_1;
SELECT 'Backup created successfully!' AS status;

-- ============================================================================
-- STEP 3: ADD NEW COLUMNS
-- ============================================================================

SELECT 'Step 3: Adding new district columns...' AS status;

ALTER TABLE State_City_PinCode_Master
ADD COLUMN IF NOT EXISTS districtId INTEGER,
ADD COLUMN IF NOT EXISTS districtName VARCHAR(100);

-- Verify columns were added
SELECT 'District columns added successfully!' AS status;

-- ============================================================================
-- STEP 4: ADD CONSTRAINTS AND COMMENTS
-- ============================================================================

SELECT 'Step 4: Adding constraints and column comments...' AS status;

-- Add NOT NULL constraint after data is populated (will be done in data loading phase)
-- For now, allow NULL during transition

-- Add column comments for documentation
COMMENT ON COLUMN State_City_PinCode_Master.districtId IS 'District Identifier (0001-N per state, resets per state)';
COMMENT ON COLUMN State_City_PinCode_Master.districtName IS 'District Name (proper district names from OGD data)';

SELECT 'Constraints and comments added!' AS status;

-- ============================================================================
-- STEP 5: DROP OLD INDEXES (if any) AND CREATE NEW INDEXES
-- ============================================================================

SELECT 'Step 5: Creating new indexes for district columns...' AS status;

-- Create single column indexes
CREATE INDEX IF NOT EXISTS idx_district_id ON State_City_PinCode_Master(districtId);
CREATE INDEX IF NOT EXISTS idx_district_name ON State_City_PinCode_Master(districtName);

-- Create composite indexes for hierarchical queries
CREATE INDEX IF NOT EXISTS idx_state_district ON State_City_PinCode_Master(stateId, districtId);
CREATE INDEX IF NOT EXISTS idx_district_city ON State_City_PinCode_Master(districtId, cityId);
CREATE INDEX IF NOT EXISTS idx_state_district_city ON State_City_PinCode_Master(stateId, districtId, cityId);
CREATE INDEX IF NOT EXISTS idx_district_status ON State_City_PinCode_Master(districtId, status);

SELECT 'Indexes created successfully!' AS status;

-- ============================================================================
-- STEP 6: VERIFY SCHEMA UPDATE
-- ============================================================================

SELECT 'Step 6: Verifying updated table structure...' AS status;

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master'
ORDER BY ordinal_position;

-- ============================================================================
-- STEP 7: DATA INTEGRITY CHECKS
-- ============================================================================

SELECT 'Step 7: Running data integrity checks...' AS status;

-- Check for records with NULL district values (expected during transition)
SELECT COUNT(*) as null_district_count
FROM State_City_PinCode_Master
WHERE districtId IS NULL OR districtName IS NULL;

-- Display sample of existing data
SELECT 'Sample existing data:' AS status;
SELECT pinCode, stateId, stateName, cityId, cityName, districtId, districtName
FROM State_City_PinCode_Master
LIMIT 5;

-- ============================================================================
-- STEP 8: POST-MIGRATION VALIDATION
-- ============================================================================

SELECT 'Step 8: Validating migration...' AS status;

-- Check table statistics
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size
FROM (
    SELECT 'State_City_PinCode_Master' as table_name
) t;

-- Verify indexes exist
SELECT indexname
FROM pg_indexes
WHERE tablename = 'state_city_pincode_master'
ORDER BY indexname;

-- ============================================================================
-- STEP 9: COMPLETION STATUS
-- ============================================================================

SELECT '✓ Migration Step 1.1 Completed Successfully!' AS status;
SELECT 'Schema updated with district columns.' AS message;
SELECT 'Next: Run data loading script to populate district data.' AS next_step;
SELECT CURRENT_TIMESTAMP as completion_timestamp;

-- ============================================================================
-- ROLLBACK PROCEDURE (if needed)
-- ============================================================================
/*
If issues arise, use the following rollback procedure:

-- ROLLBACK STEPS:
-- 1. Restore from backup
BEGIN TRANSACTION;
DROP TABLE IF EXISTS State_City_PinCode_Master;
ALTER TABLE State_City_PinCode_Master_Backup_Step1_1 RENAME TO State_City_PinCode_Master;
COMMIT;

-- 2. Verify restoration
SELECT COUNT(*) FROM State_City_PinCode_Master;
SELECT * FROM State_City_PinCode_Master LIMIT 5;
*/

-- ============================================================================
-- END OF MIGRATION SCRIPT
-- ============================================================================
