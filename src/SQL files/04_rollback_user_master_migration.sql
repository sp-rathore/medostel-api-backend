-- ============================================================================
-- ROLLBACK SCRIPT FOR USER_MASTER MIGRATION
-- Purpose: Restore previous schema if migration fails
-- Date: 2026-03-03
--
-- IMPORTANT: This script assumes that pre_migration_checks.sql was run
-- and user_master_backup_20260303 table exists
-- ============================================================================

BEGIN;

SELECT '=====================================================================' as step;
SELECT 'ROLLBACK PROCEDURE INITIATED' as step;
SELECT '=====================================================================' as step;

-- ============================================================================
-- STEP 1: DROP DEPENDENT CONSTRAINTS
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 1: Removing dependent foreign key constraints' as step;

ALTER TABLE IF EXISTS report_history DROP CONSTRAINT IF EXISTS report_history_userid_fkey;
ALTER TABLE IF EXISTS user_login DROP CONSTRAINT IF EXISTS user_login_userid_fkey;

SELECT 'STEP 1 COMPLETE: Dependent constraints removed' as result;

-- ============================================================================
-- STEP 2: DROP NEW TABLE
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 2: Dropping new schema' as step;

DROP TABLE IF EXISTS user_master CASCADE;

SELECT 'STEP 2 COMPLETE: New table removed' as result;

-- ============================================================================
-- STEP 3: RESTORE FROM BACKUP
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 3: Restoring from backup' as step;

CREATE TABLE user_master AS
SELECT * FROM user_master_backup_20260303;

SELECT 'STEP 3 COMPLETE: Backup restored' as result;

-- ============================================================================
-- STEP 4: RECREATE ORIGINAL CONSTRAINTS
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 4: Recreating original constraints' as step;

-- Primary key
ALTER TABLE user_master
ADD CONSTRAINT user_master_pkey PRIMARY KEY (userid);

-- Unique constraints
ALTER TABLE user_master
ADD CONSTRAINT user_master_emailid_key UNIQUE (emailid);

ALTER TABLE user_master
ADD CONSTRAINT user_master_mobilenumber_key UNIQUE (mobilenumber);

-- Check constraint for status
ALTER TABLE user_master
ADD CONSTRAINT user_master_status_check
CHECK (status::text = ANY (ARRAY['Active'::character varying, 'Inactive'::character varying]::text[]));

-- Foreign key constraint for currentrole
ALTER TABLE user_master
ADD CONSTRAINT user_master_currentrole_fkey
FOREIGN KEY (currentrole) REFERENCES user_role_master(roleid)
ON UPDATE CASCADE
ON DELETE SET NULL;

SELECT 'STEP 4 COMPLETE: Original constraints recreated' as result;

-- ============================================================================
-- STEP 5: RECREATE ORIGINAL INDEXES
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 5: Recreating original indexes' as step;

CREATE INDEX idx_user_created_date ON user_master(createddate);
CREATE INDEX idx_user_email ON user_master(emailid);
CREATE INDEX idx_user_mobile ON user_master(mobilenumber);
CREATE INDEX idx_user_role ON user_master(currentrole);
CREATE INDEX idx_user_status ON user_master(status);

SELECT 'STEP 5 COMPLETE: Original indexes recreated' as result;

-- ============================================================================
-- STEP 6: RECREATE DEPENDENT FOREIGN KEYS
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 6: Recreating dependent foreign key constraints' as step;

ALTER TABLE report_history
ADD CONSTRAINT report_history_userid_fkey
FOREIGN KEY (userid) REFERENCES user_master(userid)
ON DELETE CASCADE;

ALTER TABLE user_login
ADD CONSTRAINT user_login_userid_fkey
FOREIGN KEY (userid) REFERENCES user_master(userid)
ON DELETE CASCADE;

SELECT 'STEP 6 COMPLETE: Dependent constraints recreated' as result;

-- ============================================================================
-- STEP 7: VERIFICATION
-- ============================================================================

SELECT '' as space;
SELECT 'STEP 7: Verifying restoration' as step;

-- Table structure
SELECT 'Original table structure restored:' as verification;
SELECT COUNT(*) as column_count FROM information_schema.columns WHERE table_name = 'user_master';
SELECT COUNT(*) as constraint_count FROM information_schema.table_constraints WHERE table_name = 'user_master';
SELECT COUNT(*) as index_count FROM pg_indexes WHERE tablename = 'user_master';

-- Record count
SELECT 'Original data restored:' as verification;
SELECT COUNT(*) as record_count FROM user_master;

SELECT 'STEP 7 COMPLETE: Restoration verified' as result;

-- ============================================================================
-- COMMIT TRANSACTION
-- ============================================================================

COMMIT;

SELECT '' as space;
SELECT '=====================================================================' as final;
SELECT 'ROLLBACK COMPLETE: Original schema restored!' as final;
SELECT '=====================================================================' as final;
SELECT '' as space;
SELECT 'Original user_master table is now active and ready for use.' as message;
SELECT 'All constraints and indexes have been recreated.' as message;
SELECT 'Dependent tables (report_history, user_login) are now functional.' as message;
SELECT '' as space;
SELECT 'NOTE: To clean up the backup table when you are confident with the' as message;
SELECT '      recovery, run: DROP TABLE user_master_backup_20260303;' as message;
SELECT '' as space;
SELECT CURRENT_TIMESTAMP as rollback_completed_at;
