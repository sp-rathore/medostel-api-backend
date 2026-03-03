-- ============================================================================
-- PRE-MIGRATION VERIFICATION SCRIPT
-- Purpose: Verify system state before user_master migration
-- Date: 2026-03-03
-- ============================================================================

-- Document current schema
COMMENT ON TABLE user_master IS 'BACKUP: Pre-migration schema as of 2026-03-03';

-- Show current table structure
SELECT '=== CURRENT USER_MASTER STRUCTURE ===' as info;
\d user_master

-- Count records
SELECT '=== CURRENT RECORD COUNT ===' as info;
SELECT COUNT(*) as record_count FROM user_master;

-- Check dependent constraints
SELECT '=== DEPENDENT CONSTRAINTS ===' as info;
SELECT
    constraint_name,
    table_name,
    column_name
FROM information_schema.key_column_usage
WHERE referenced_table_name = 'user_master'
ORDER BY table_name, constraint_name;

-- Verify user_role_master exists
SELECT '=== VERIFYING USER_ROLE_MASTER ===' as info;
SELECT COUNT(*) as role_count FROM user_role_master;

-- Verify state_city_pincode_master exists
SELECT '=== VERIFYING STATE_CITY_PINCODE_MASTER ===' as info;
SELECT COUNT(*) as location_count FROM state_city_pincode_master;

-- Show available roles
SELECT '=== AVAILABLE ROLES FOR FK MAPPING ===' as info;
SELECT roleid, rolename, status
FROM user_role_master
ORDER BY roleid;

-- Create backup table for safety
SELECT '=== CREATING BACKUP TABLE ===' as info;
CREATE TABLE user_master_backup_20260303 AS SELECT * FROM user_master;
SELECT 'Backup table created successfully: user_master_backup_20260303' as status;

-- Final verification
SELECT '=== PRE-MIGRATION VERIFICATION COMPLETE ===' as info;
SELECT CURRENT_TIMESTAMP as check_timestamp;
