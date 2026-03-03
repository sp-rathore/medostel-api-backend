-- ============================================================================
-- Migration Step 1.2: User_Master Schema Enhancement with Geographic Hierarchy
-- ============================================================================
-- Purpose: Add foreign key relationships to State_City_PinCode_Master table
-- Changes:
--   1. Add stateId (INTEGER, FK)
--   2. Add districtId (INTEGER, FK)
--   3. Add cityId (INTEGER, FK)
--   4. Change pinCode from VARCHAR(10) to INTEGER
--   5. Create indexes for new columns
--   6. Maintain backward compatibility
--
-- Database: Medostel
-- Date: March 4, 2026
-- ============================================================================

\echo '=== MIGRATION STEP 1.2: User_Master Geographic Hierarchy Enhancement ==='
\echo ''

-- ============================================================================
-- STEP 1: Pre-migration verification
-- ============================================================================
\echo 'Step 1: Verifying current table structure...'

SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'user_master'
ORDER BY ordinal_position;

\echo 'Current User_Master record count:'
SELECT COUNT(*) as current_record_count FROM User_Master;

-- ============================================================================
-- STEP 2: Create backup table
-- ============================================================================
\echo ''
\echo 'Step 2: Creating backup table...'

CREATE TABLE IF NOT EXISTS User_Master_Backup_Step1_2 AS
SELECT * FROM User_Master;

\echo 'Backup table created successfully!'
SELECT COUNT(*) as backup_record_count FROM User_Master_Backup_Step1_2;

-- ============================================================================
-- STEP 3: Add new columns to User_Master
-- ============================================================================
\echo ''
\echo 'Step 3: Adding new geographic columns...'

-- Add stateId column
ALTER TABLE User_Master
ADD COLUMN IF NOT EXISTS stateId INTEGER;

-- Add districtId column
ALTER TABLE User_Master
ADD COLUMN IF NOT EXISTS districtId INTEGER;

-- Add cityId column
ALTER TABLE User_Master
ADD COLUMN IF NOT EXISTS cityId INTEGER;

\echo 'New columns added successfully!'

-- ============================================================================
-- STEP 4: Convert pinCode from VARCHAR to INTEGER
-- ============================================================================
\echo ''
\echo 'Step 4: Converting pinCode data type...'

-- Rename old pinCode column
ALTER TABLE User_Master
RENAME COLUMN pinCode TO pinCode_varchar;

-- Create new pinCode column as INTEGER
ALTER TABLE User_Master
ADD COLUMN pinCode INTEGER;

-- Migrate data with type conversion
-- Only convert valid 6-digit numeric strings
UPDATE User_Master
SET pinCode = CAST(pinCode_varchar AS INTEGER)
WHERE pinCode_varchar ~ '^\d{6}$';

-- Log records that couldn't be converted
\echo 'Records with invalid pinCode format (not converted):'
SELECT userId, pinCode_varchar
FROM User_Master
WHERE pinCode IS NULL AND pinCode_varchar IS NOT NULL;

-- Drop old VARCHAR column
ALTER TABLE User_Master
DROP COLUMN pinCode_varchar;

\echo 'pinCode type conversion completed!'

-- ============================================================================
-- STEP 5: Create foreign key constraints
-- ============================================================================
\echo ''
\echo 'Step 5: Creating foreign key constraints...'

-- Add FK constraint for stateId
ALTER TABLE User_Master
ADD CONSTRAINT fk_user_state_id
FOREIGN KEY (stateId)
REFERENCES State_City_PinCode_Master(stateId)
ON DELETE RESTRICT;

-- Add FK constraint for districtId
ALTER TABLE User_Master
ADD CONSTRAINT fk_user_district_id
FOREIGN KEY (districtId)
REFERENCES State_City_PinCode_Master(districtId)
ON DELETE RESTRICT;

-- Add FK constraint for cityId
ALTER TABLE User_Master
ADD CONSTRAINT fk_user_city_id
FOREIGN KEY (cityId)
REFERENCES State_City_PinCode_Master(cityId)
ON DELETE RESTRICT;

-- Add FK constraint for pinCode
ALTER TABLE User_Master
ADD CONSTRAINT fk_user_pincode
FOREIGN KEY (pinCode)
REFERENCES State_City_PinCode_Master(pinCode)
ON DELETE RESTRICT;

\echo 'Foreign key constraints created successfully!'

-- ============================================================================
-- STEP 6: Create indexes on new columns
-- ============================================================================
\echo ''
\echo 'Step 6: Creating indexes on geographic columns...'

CREATE INDEX IF NOT EXISTS idx_user_state_id ON User_Master(stateId);
CREATE INDEX IF NOT EXISTS idx_user_district_id ON User_Master(districtId);
CREATE INDEX IF NOT EXISTS idx_user_city_id ON User_Master(cityId);
CREATE INDEX IF NOT EXISTS idx_user_pincode ON User_Master(pinCode);

-- Composite indexes for efficient hierarchical queries
CREATE INDEX IF NOT EXISTS idx_user_state_district ON User_Master(stateId, districtId);
CREATE INDEX IF NOT EXISTS idx_user_district_city ON User_Master(districtId, cityId);

\echo 'Indexes created successfully!'

-- ============================================================================
-- STEP 7: Verify migration
-- ============================================================================
\echo ''
\echo 'Step 7: Verifying migration...'

\echo 'Updated User_Master structure:'
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'user_master'
ORDER BY ordinal_position;

\echo ''
\echo 'Foreign keys added:'
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'user_master'
AND constraint_type = 'FOREIGN KEY'
ORDER BY constraint_name;

\echo ''
\echo 'Indexes created:'
SELECT indexname
FROM pg_indexes
WHERE tablename = 'user_master'
AND indexname LIKE 'idx_user_%'
ORDER BY indexname;

-- ============================================================================
-- STEP 8: Data integrity checks
-- ============================================================================
\echo ''
\echo 'Step 8: Data integrity checks...'

\echo 'Record count comparison:'
\echo '  Original: '
SELECT COUNT(*) as original_count FROM User_Master_Backup_Step1_2;
\echo '  Current: '
SELECT COUNT(*) as current_count FROM User_Master;

\echo ''
\echo 'Null value checks for new columns (expected to show nulls for existing users):'
SELECT
    (SELECT COUNT(*) FROM User_Master WHERE stateId IS NULL) as null_stateId,
    (SELECT COUNT(*) FROM User_Master WHERE districtId IS NULL) as null_districtId,
    (SELECT COUNT(*) FROM User_Master WHERE cityId IS NULL) as null_cityId,
    (SELECT COUNT(*) FROM User_Master WHERE pinCode IS NULL) as null_pinCode;

-- ============================================================================
-- STEP 9: Backup verification
-- ============================================================================
\echo ''
\echo 'Step 9: Backup table verification...'

\echo 'Backup table exists and contains data:'
SELECT COUNT(*) as backup_record_count FROM User_Master_Backup_Step1_2;

\echo ''
\echo '=== MIGRATION STEP 1.2 COMPLETED SUCCESSFULLY ==='
\echo ''
\echo 'Summary:'
\echo '  ✓ Added 3 new geographic foreign key columns'
\echo '  ✓ Changed pinCode from VARCHAR(10) to INTEGER'
\echo '  ✓ Created 6 new indexes for geographic queries'
\echo '  ✓ Created foreign key constraints'
\echo '  ✓ Backup table created for rollback'
\echo ''
\echo 'To rollback this migration, execute migration_step1_2_rollback.sql'
\echo ''

-- ============================================================================
-- ROLLBACK INSTRUCTIONS (Manual)
-- ============================================================================
-- If needed, use the following steps to rollback:
--
-- 1. Drop all constraints added in this migration:
--    ALTER TABLE User_Master DROP CONSTRAINT fk_user_state_id;
--    ALTER TABLE User_Master DROP CONSTRAINT fk_user_district_id;
--    ALTER TABLE User_Master DROP CONSTRAINT fk_user_city_id;
--    ALTER TABLE User_Master DROP CONSTRAINT fk_user_pincode;
--
-- 2. Drop new columns:
--    ALTER TABLE User_Master DROP COLUMN stateId;
--    ALTER TABLE User_Master DROP COLUMN districtId;
--    ALTER TABLE User_Master DROP COLUMN cityId;
--    ALTER TABLE User_Master DROP COLUMN pinCode;
--
-- 3. Add back old VARCHAR pinCode column:
--    ALTER TABLE User_Master ADD COLUMN pinCode VARCHAR(10);
--    UPDATE User_Master SET pinCode = CAST(b.pinCode_varchar AS VARCHAR(10))
--    FROM User_Master_Backup_Step1_2 b WHERE User_Master.userId = b.userId;
--
-- 4. Drop indexes:
--    DROP INDEX IF EXISTS idx_user_state_id;
--    DROP INDEX IF EXISTS idx_user_district_id;
--    DROP INDEX IF EXISTS idx_user_city_id;
--    DROP INDEX IF EXISTS idx_user_pincode;
--    DROP INDEX IF EXISTS idx_user_state_district;
--    DROP INDEX IF EXISTS idx_user_district_city;
--
-- 5. Verify rollback:
--    SELECT COUNT(*) FROM User_Master;  -- Should match backup count
-- ============================================================================
