-- ============================================================================
-- Rollback Script: new_user_request Migration Rollback
-- ============================================================================
-- Date: March 3, 2026
-- Purpose: Rollback new_user_request table to previous schema if migration fails
-- Version: 1.0
-- Status: Emergency Only - Use only if migration validation fails
-- ============================================================================
-- WARNING: This script should only be executed if the migration has failed
-- or validation has shown critical issues. It will restore the previous schema.
-- ============================================================================

BEGIN TRANSACTION;

-- Step 1: Drop the new (problematic) table
DROP TABLE IF EXISTS new_user_request CASCADE;

-- Step 2: Restore from backup
ALTER TABLE IF EXISTS new_user_request_backup RENAME TO new_user_request;

-- Step 3: Recreate indexes from original schema
CREATE UNIQUE INDEX pk_new_user_request ON new_user_request(requestId);
CREATE INDEX idx_request_email ON new_user_request(emailId);
CREATE INDEX idx_request_mobile ON new_user_request(mobileNumber);
CREATE INDEX idx_request_status ON new_user_request(requestStatus);
CREATE INDEX idx_request_role ON new_user_request(currentRole);
CREATE INDEX idx_request_created ON new_user_request(createdDate);
CREATE INDEX idx_request_updated ON new_user_request(updatedDate);

-- Step 4: Commit rollback
COMMIT;

-- ============================================================================
-- Rollback Verification
-- ============================================================================
SELECT 'Rollback Complete! Original schema restored.' AS Status;

-- Verify table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'new_user_request'
ORDER BY ordinal_position;

-- Verify row count
SELECT COUNT(*) AS total_records FROM new_user_request;

-- ============================================================================
-- Post-Rollback Actions
-- ============================================================================
-- After successful rollback:
-- 1. Review error logs to identify cause of migration failure
-- 2. Fix the issue in migration script
-- 3. Re-run migration with corrected script
-- 4. Re-run validation script
-- ============================================================================
