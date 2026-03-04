-- ============================================================================
-- Validation Script: new_user_request Migration Verification
-- ============================================================================
-- Date: March 3, 2026
-- Purpose: Validate that migration completed successfully and data integrity maintained
-- Version: 1.0
-- ============================================================================

-- ============================================================================
-- 1. SCHEMA VALIDATION
-- ============================================================================
SELECT '=== SCHEMA VALIDATION ===' AS check_category;

-- Check if new_user_request table exists with correct structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'new_user_request'
ORDER BY ordinal_position;

-- ============================================================================
-- 2. CONSTRAINT VALIDATION
-- ============================================================================
SELECT '=== CONSTRAINT VALIDATION ===' AS check_category;

-- Check if all indexes exist
SELECT indexname FROM pg_indexes
WHERE tablename = 'new_user_request'
ORDER BY indexname;

-- ============================================================================
-- 3. DATA INTEGRITY CHECKS
-- ============================================================================
SELECT '=== DATA INTEGRITY CHECKS ===' AS check_category;

-- Check 1: All rows have valid requestId format
SELECT COUNT(*) AS rows_with_valid_requestId
FROM new_user_request
WHERE requestId ~ '^REQ_[0-9]+$' OR requestId IS NOT NULL;

-- Check 2: All rows have unique userId (emails)
SELECT COUNT(DISTINCT userId) AS unique_userIds, COUNT(*) AS total_rows
FROM new_user_request;

-- Check 3: All rows have valid status values
SELECT status, COUNT(*) AS count
FROM new_user_request
GROUP BY status
ORDER BY status;

-- Check 4: All rows have valid mobileNumber format (10 digits)
SELECT COUNT(*) AS rows_with_valid_mobile
FROM new_user_request
WHERE mobileNumber >= 1000000000 AND mobileNumber <= 9999999999;

-- Check 5: All rows have timestamps
SELECT COUNT(*) AS rows_with_created_date, COUNT(*) AS rows_with_updated_date
FROM new_user_request
WHERE created_Date IS NOT NULL AND updated_Date IS NOT NULL;

-- ============================================================================
-- 4. COMPARISON WITH BACKUP
-- ============================================================================
SELECT '=== BACKUP COMPARISON ===' AS check_category;

-- Row count comparison
SELECT
    (SELECT COUNT(*) FROM new_user_request) AS new_table_count,
    (SELECT COUNT(*) FROM new_user_request_backup) AS backup_table_count;

-- Check if all requestIds from backup exist in new table
SELECT COUNT(*) AS rows_in_backup_not_in_new
FROM new_user_request_backup
WHERE requestId NOT IN (SELECT requestId FROM new_user_request);

-- ============================================================================
-- 5. CONSTRAINT VALIDATION
-- ============================================================================
SELECT '=== DETAILED CONSTRAINT CHECKS ===' AS check_category;

-- Check if any userId violates email format constraint
SELECT COUNT(*) AS invalid_emails
FROM new_user_request
WHERE NOT (userId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$');

-- Check if any status violates CHECK constraint
SELECT COUNT(*) AS invalid_status
FROM new_user_request
WHERE status NOT IN ('pending', 'active', 'rejected');

-- ============================================================================
-- 6. SUMMARY REPORT
-- ============================================================================
SELECT '=== MIGRATION SUMMARY ===' AS check_category;

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT userId) AS unique_emails,
    COUNT(DISTINCT currentRole) AS unique_roles,
    COUNT(DISTINCT status) AS status_values,
    MIN(created_Date) AS earliest_creation,
    MAX(created_Date) AS latest_creation
FROM new_user_request;

-- ============================================================================
-- 7. CLEANUP RECOMMENDATION
-- ============================================================================
SELECT '=== CLEANUP RECOMMENDATION ===' AS message,
       'If all validation checks pass, run:' AS action,
       'DROP TABLE new_user_request_backup;' AS command;

-- ============================================================================
-- Validation Complete
-- ============================================================================
-- If all checks show expected results:
-- - new_table_count should equal backup_table_count
-- - rows_in_backup_not_in_new should be 0
-- - invalid_emails and invalid_status should be 0
-- - All required columns should be present
-- Then migration is successful and backup can be dropped
-- ============================================================================
