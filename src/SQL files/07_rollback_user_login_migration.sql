-- ============================================================================
-- User_Login Table Schema Migration ROLLBACK
-- ============================================================================
-- Date: March 3, 2026
-- Purpose: Rollback user_login table schema to previous state
-- Status: Emergency Rollback Procedure
-- ============================================================================
-- PREREQUISITES:
-- - Migration script (05_migrate_user_login_schema.sql) must have been executed
-- - Backup table (user_login_backup) must exist
-- - No other changes have been made to the new user_login table
-- ============================================================================

BEGIN;

-- Step 1: Safety check - verify backup table exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_login_backup') THEN
        RAISE EXCEPTION 'Cannot rollback: user_login_backup table not found. Rollback aborted.';
    END IF;
    RAISE NOTICE 'Safety check passed: Backup table exists with % records', (SELECT COUNT(*) FROM user_login_backup);
END $$;

-- Step 2: Verify backup table integrity
DO $$
DECLARE
    backup_count INT;
    required_cols TEXT[] := ARRAY['userId', 'username', 'password', 'roleId', 'isActive', 'lastLoginTime', 'loginAttempts', 'createdDate', 'updatedDate'];
    col TEXT;
    missing_count INT := 0;
BEGIN
    SELECT COUNT(*) INTO backup_count FROM user_login_backup;
    RAISE NOTICE 'Backup table contains % records', backup_count;

    -- Note: We check for OLD columns (not new schema), as backup contains old data
    FOREACH col IN ARRAY required_cols LOOP
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_login_backup' AND column_name = col) THEN
            RAISE NOTICE '  ✗ Missing column in backup: %', col;
            missing_count := missing_count + 1;
        END IF;
    END LOOP;

    IF missing_count > 0 THEN
        RAISE EXCEPTION 'Backup table is corrupted (% missing columns). Rollback aborted.', missing_count;
    END IF;

    RAISE NOTICE 'Backup table integrity verified: All required columns present';
END $$;

-- Step 3: Drop new table
DROP TABLE IF EXISTS user_login CASCADE;
RAISE NOTICE 'Dropped new user_login table';

-- Step 4: Recreate old table structure from backup
CREATE TABLE user_login (
    userId BIGINT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    roleId INTEGER NOT NULL,
    isActive BOOLEAN DEFAULT TRUE,
    lastLoginTime TIMESTAMP,
    loginAttempts INTEGER DEFAULT 0,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user_master(userId),
    FOREIGN KEY (roleId) REFERENCES user_role_master(roleId) ON UPDATE CASCADE ON DELETE RESTRICT
);

RAISE NOTICE 'Recreated old user_login table structure';

-- Step 5: Restore data from backup
INSERT INTO user_login (
    userId,
    username,
    password,
    roleId,
    isActive,
    lastLoginTime,
    loginAttempts,
    createdDate,
    updatedDate
)
SELECT
    userId,
    username,
    password,
    roleId,
    isActive,
    lastLoginTime,
    loginAttempts,
    createdDate,
    updatedDate
FROM user_login_backup;

RAISE NOTICE 'Restored % records from backup', (SELECT COUNT(*) FROM user_login);

-- Step 6: Recreate old indexes
CREATE UNIQUE INDEX pk_user_login ON user_login(userId);
CREATE INDEX idx_login_username ON user_login(username);
CREATE INDEX idx_login_active ON user_login(isActive);
CREATE INDEX idx_login_role ON user_login(roleId);
CREATE INDEX idx_login_attempts ON user_login(loginAttempts);
CREATE INDEX idx_login_lastlogin ON user_login(lastLoginTime);
CREATE INDEX idx_login_updated ON user_login(updatedDate);

RAISE NOTICE 'Recreated all indexes on user_login table';

-- Step 7: Verify rollback
DO $$
DECLARE
    current_count INT;
    backup_count INT;
    col_count INT;
BEGIN
    SELECT COUNT(*) INTO current_count FROM user_login;
    SELECT COUNT(*) INTO backup_count FROM user_login_backup;
    SELECT COUNT(*) INTO col_count FROM information_schema.columns WHERE table_name = 'user_login';

    RAISE NOTICE '';
    RAISE NOTICE 'Rollback Verification:';
    RAISE NOTICE '  - Records restored: % (backup had %)', current_count, backup_count;
    RAISE NOTICE '  - Columns restored: % (expected 9)', col_count;

    IF current_count = backup_count AND col_count = 9 THEN
        RAISE NOTICE '  ✓ Rollback completed successfully!';
    ELSE
        RAISE WARNING '  ⚠ Rollback verification failed';
    END IF;
END $$;

COMMIT;

-- Summary
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '====================================================';
    RAISE NOTICE 'ROLLBACK COMPLETED';
    RAISE NOTICE '====================================================';
    RAISE NOTICE 'Old user_login schema has been restored:';
    RAISE NOTICE '  - userId BIGINT PRIMARY KEY';
    RAISE NOTICE '  - username VARCHAR(100) UNIQUE';
    RAISE NOTICE '  - password VARCHAR(255)';
    RAISE NOTICE '  - roleId INTEGER FK';
    RAISE NOTICE '  - isActive BOOLEAN';
    RAISE NOTICE '  - lastLoginTime TIMESTAMP';
    RAISE NOTICE '  - loginAttempts INTEGER';
    RAISE NOTICE '  - createdDate TIMESTAMP';
    RAISE NOTICE '  - updatedDate TIMESTAMP';
    RAISE NOTICE '';
    RAISE NOTICE 'Backup table user_login_backup still exists for reference';
    RAISE NOTICE '====================================================';
END $$;

-- To clean up backup after verifying rollback was successful, run:
-- DROP TABLE user_login_backup;
