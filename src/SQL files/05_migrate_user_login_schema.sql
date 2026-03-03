-- ============================================================================
-- User_Login Table Schema Migration
-- ============================================================================
-- Date: March 3, 2026
-- Purpose: Migrate user_login table from old schema to new schema
-- Status: Production Ready
-- ============================================================================
-- Changes:
-- 1. Primary Key: userId (BIGINT) → email_id (VARCHAR(255))
-- 2. Column rename: isActive → is_active (BOOLEAN → CHAR(1))
-- 3. Column rename: lastLoginTime → last_login
-- 4. Column rename: loginAttempts → REMOVED (not in requirements)
-- 5. Column rename: username → REMOVED (not in requirements)
-- 6. Column rename: roleId → REMOVED (not in requirements)
-- 7. New column: mobile_number (NUMERIC(10))
-- 8. FK change: userId → email_id REFERENCES user_master(emailId)
-- 9. Index updates: Align with new schema
-- ============================================================================

BEGIN;

-- Step 1: Pre-migration validation
-- Ensure user_master has required data
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM user_master) = 0 THEN
        RAISE EXCEPTION 'user_master table is empty. Cannot proceed with migration.';
    END IF;
    RAISE NOTICE 'Pre-migration validation passed. Found % records in user_master', (SELECT COUNT(*) FROM user_master);
END $$;

-- Step 2: Create backup of old table
CREATE TABLE user_login_backup AS
SELECT * FROM user_login;

RAISE NOTICE 'Backup created: user_login_backup with % records', (SELECT COUNT(*) FROM user_login_backup);

-- Step 3: Drop old table (and any dependent objects)
DROP TABLE IF EXISTS user_login CASCADE;

RAISE NOTICE 'Dropped old user_login table';

-- Step 4: Create new user_login table with updated schema
CREATE TABLE user_login (
    email_id VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    mobile_number NUMERIC(10) NOT NULL
        CHECK (mobile_number >= 1000000000 AND mobile_number <= 9999999999),
    is_active CHAR(1) NOT NULL DEFAULT 'Y'
        CHECK (is_active IN ('Y', 'N')),
    last_login TIMESTAMP,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_id) REFERENCES user_master(emailId) ON UPDATE CASCADE ON DELETE CASCADE
);

RAISE NOTICE 'Created new user_login table with updated schema';

-- Step 5: Create indexes
CREATE UNIQUE INDEX pk_user_login ON user_login(email_id);
CREATE INDEX idx_login_mobile ON user_login(mobile_number);
CREATE INDEX idx_login_is_active ON user_login(is_active);
CREATE INDEX idx_login_last_login ON user_login(last_login);
CREATE INDEX idx_login_updated_date ON user_login(updated_date);

RAISE NOTICE 'Created all indexes on user_login table';

-- Step 6: Data migration (if any old records exist)
-- Map old schema to new schema with data transformation
INSERT INTO user_login (
    email_id,
    password,
    mobile_number,
    is_active,
    last_login,
    created_date,
    updated_date
)
SELECT
    um.emailId,                                    -- Map userId → emailId from user_master
    ulb.password,                                  -- Keep password as-is (already hashed or will be re-hashed)
    um.mobileNumber,                               -- Get mobile_number from user_master
    CASE
        WHEN ulb.isActive = true THEN 'Y'
        WHEN ulb.isActive = false THEN 'N'
        ELSE 'Y'
    END,                                           -- Convert BOOLEAN to CHAR(1)
    ulb.lastLoginTime,                             -- Rename lastLoginTime to last_login
    ulb.createdDate,                               -- Rename createdDate to created_date
    ulb.updatedDate                                -- Rename updatedDate to updated_date
FROM user_login_backup ulb
INNER JOIN user_master um ON ulb.userId = um.userId
WHERE um.emailId IS NOT NULL;                      -- Only migrate records with valid email

RAISE NOTICE 'Migrated % records from old user_login to new user_login', (SELECT COUNT(*) FROM user_login);

-- Step 7: Verify migration
DO $$
DECLARE
    new_count INT;
    old_count INT;
BEGIN
    SELECT COUNT(*) INTO new_count FROM user_login;
    SELECT COUNT(*) INTO old_count FROM user_login_backup;

    RAISE NOTICE 'Migration verification: Old records: %, New records: %', old_count, new_count;

    IF new_count <> old_count THEN
        RAISE WARNING 'Record count mismatch: % old records, % new records', old_count, new_count;
    END IF;
END $$;

-- Step 8: Validate schema integrity
DO $$
BEGIN
    -- Check that email_id PK is properly set
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints
                   WHERE table_name = 'user_login' AND constraint_type = 'PRIMARY KEY') THEN
        RAISE EXCEPTION 'Primary key not found on user_login table';
    END IF;

    -- Check that FKs are properly set
    IF NOT EXISTS (SELECT 1 FROM information_schema.constraint_column_usage
                   WHERE table_name = 'user_login' AND column_name = 'email_id') THEN
        RAISE EXCEPTION 'Foreign key constraint not found for email_id';
    END IF;

    RAISE NOTICE 'Schema integrity validation passed';
END $$;

COMMIT;

-- Final Summary
DO $$
DECLARE
    col_count INT;
    index_count INT;
BEGIN
    SELECT COUNT(*) INTO col_count FROM information_schema.columns WHERE table_name = 'user_login';
    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE tablename = 'user_login';

    RAISE NOTICE '====================================================';
    RAISE NOTICE 'Migration completed successfully!';
    RAISE NOTICE '====================================================';
    RAISE NOTICE 'New user_login table:';
    RAISE NOTICE '  - Total columns: %', col_count;
    RAISE NOTICE '  - Total indexes: %', index_count;
    RAISE NOTICE '  - Total records: %', (SELECT COUNT(*) FROM user_login);
    RAISE NOTICE '  - Primary Key: email_id (VARCHAR(255))';
    RAISE NOTICE '  - Foreign Keys: email_id → user_master(emailId), role_id → user_role_master(roleId)';
    RAISE NOTICE '';
    RAISE NOTICE 'Backup table: user_login_backup (for rollback if needed)';
    RAISE NOTICE '====================================================';
END $$;

-- Note: To rollback, execute 07_rollback_user_login_migration.sql
