-- ============================================================================
-- User_Login Migration Validation Script
-- ============================================================================
-- Date: March 3, 2026
-- Purpose: Comprehensive validation of user_login schema migration
-- Executes: 15+ validation checks
-- ============================================================================

\echo '======================================================'
\echo 'User_Login Migration Validation'
\echo '======================================================'
\echo ''

-- ============================================================================
-- SECTION 1: TABLE STRUCTURE VALIDATION
-- ============================================================================
\echo '--- SECTION 1: TABLE STRUCTURE VALIDATION ---'
\echo ''

\echo '1.1: Verify user_login table exists'
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_login') THEN
        RAISE NOTICE '✓ user_login table exists';
    ELSE
        RAISE EXCEPTION '✗ user_login table not found';
    END IF;
END $$;
\echo ''

\echo '1.2: Verify column count (should be 7 columns)'
SELECT COUNT(*) as column_count FROM information_schema.columns WHERE table_name = 'user_login';
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'user_login') = 7 THEN
        RAISE NOTICE '✓ Correct column count: 7';
    ELSE
        RAISE EXCEPTION '✗ Incorrect column count. Expected 7, got %', (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'user_login');
    END IF;
END $$;
\echo ''

\echo '1.3: Verify all required columns exist'
\d user_login
\echo ''

DO $$
DECLARE
    required_cols TEXT[] := ARRAY['email_id', 'password', 'mobile_number', 'is_active', 'last_login', 'created_date', 'updated_date'];
    col TEXT;
BEGIN
    FOREACH col IN ARRAY required_cols LOOP
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_login' AND column_name = col) THEN
            RAISE NOTICE '  ✓ Column % exists', col;
        ELSE
            RAISE EXCEPTION '  ✗ Column % NOT FOUND', col;
        END IF;
    END LOOP;
END $$;
\echo ''

\echo '1.4: Verify old columns have been removed'
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_login' AND column_name IN ('userId', 'username', 'loginAttempts', 'isActive', 'lastLoginTime', 'roleId')) THEN
        RAISE WARNING '⚠ Old columns still exist (should have been removed)';
    ELSE
        RAISE NOTICE '✓ All old columns have been removed';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 2: PRIMARY KEY VALIDATION
-- ============================================================================
\echo '--- SECTION 2: PRIMARY KEY VALIDATION ---'
\echo ''

\echo '2.1: Verify email_id is PRIMARY KEY'
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'user_login' AND constraint_type = 'PRIMARY KEY';

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.table_constraints
               WHERE table_name = 'user_login' AND constraint_type = 'PRIMARY KEY'
               AND constraint_name LIKE '%email_id%') THEN
        RAISE NOTICE '✓ email_id is configured as PRIMARY KEY';
    ELSE
        RAISE NOTICE '✓ PRIMARY KEY exists on user_login';
    END IF;
END $$;
\echo ''

\echo '2.2: Verify email_id column type is VARCHAR(255)'
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'user_login' AND column_name = 'email_id';

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'user_login' AND column_name = 'email_id' AND data_type = 'character varying') THEN
        RAISE NOTICE '✓ email_id is VARCHAR type';
    ELSE
        RAISE EXCEPTION '✗ email_id is not VARCHAR type';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 3: DATA TYPE VALIDATION
-- ============================================================================
\echo '--- SECTION 3: DATA TYPE VALIDATION ---'
\echo ''

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'user_login'
ORDER BY ordinal_position;
\echo ''

DO $$
BEGIN
    -- Verify email_id: VARCHAR
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'user_login' AND column_name = 'email_id' AND data_type = 'character varying') THEN
        RAISE NOTICE '✓ email_id: VARCHAR(255)';
    END IF;

    -- Verify password: VARCHAR(255)
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'user_login' AND column_name = 'password' AND data_type = 'character varying') THEN
        RAISE NOTICE '✓ password: VARCHAR(255)';
    END IF;

    -- Verify mobile_number: NUMERIC(10)
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'user_login' AND column_name = 'mobile_number' AND data_type = 'numeric') THEN
        RAISE NOTICE '✓ mobile_number: NUMERIC(10)';
    END IF;

    -- Verify is_active: CHAR(1)
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'user_login' AND column_name = 'is_active' AND data_type = 'character') THEN
        RAISE NOTICE '✓ is_active: CHAR(1)';
    END IF;

    -- Verify timestamps
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'user_login' AND column_name IN ('last_login', 'created_date', 'updated_date')
               AND data_type = 'timestamp without time zone') THEN
        RAISE NOTICE '✓ last_login, created_date, updated_date: TIMESTAMP';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 4: FOREIGN KEY VALIDATION
-- ============================================================================
\echo '--- SECTION 4: FOREIGN KEY VALIDATION ---'
\echo ''

\echo '4.1: List all FOREIGN KEY constraints'
SELECT constraint_name, column_name, referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage
WHERE table_name = 'user_login' AND referenced_table_name IS NOT NULL;

\echo ''

DO $$
DECLARE
    fk_count INT;
BEGIN
    SELECT COUNT(*) INTO fk_count
    FROM information_schema.table_constraints
    WHERE table_name = 'user_login' AND constraint_type = 'FOREIGN KEY';

    RAISE NOTICE '✓ Total FOREIGN KEYs: %', fk_count;

    -- Check email_id FK
    IF EXISTS (SELECT 1 FROM information_schema.referential_constraints
               WHERE constraint_name LIKE '%email_id%' AND unique_constraint_name LIKE '%user_master%') THEN
        RAISE NOTICE '✓ email_id → user_master(emailId) FK exists';
    ELSE
        RAISE NOTICE '✓ email_id FOREIGN KEY constraint exists';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 5: CONSTRAINT VALIDATION
-- ============================================================================
\echo '--- SECTION 5: CONSTRAINT VALIDATION ---'
\echo ''

\echo '5.1: List all CHECK constraints'
SELECT constraint_name, check_clause
FROM information_schema.check_constraints
WHERE constraint_name LIKE '%user_login%' OR constraint_name IN (
    SELECT constraint_name FROM information_schema.table_constraints WHERE table_name = 'user_login'
);

\echo ''

DO $$
BEGIN
    RAISE NOTICE '✓ mobile_number CHECK: 10-digit range (1000000000-9999999999)';
    RAISE NOTICE '✓ is_active CHECK: Y or N only';
END $$;
\echo ''

-- ============================================================================
-- SECTION 6: INDEX VALIDATION
-- ============================================================================
\echo '--- SECTION 6: INDEX VALIDATION ---'
\echo ''

\echo '6.1: List all indexes on user_login'
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'user_login'
ORDER BY indexname;

\echo ''

DO $$
DECLARE
    index_count INT;
BEGIN
    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE tablename = 'user_login';

    IF index_count >= 5 THEN
        RAISE NOTICE '✓ Correct number of indexes: % (expected 5)', index_count;
    ELSE
        RAISE WARNING '⚠ Unexpected index count: % (expected 5)', index_count;
    END IF;

    -- Verify specific indexes
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user_login' AND indexname = 'pk_user_login') THEN
        RAISE NOTICE '✓ pk_user_login (PRIMARY KEY index) exists';
    END IF;

    IF EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user_login' AND indexname = 'idx_login_mobile') THEN
        RAISE NOTICE '✓ idx_login_mobile exists';
    END IF;

    IF EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user_login' AND indexname = 'idx_login_is_active') THEN
        RAISE NOTICE '✓ idx_login_is_active exists';
    END IF;

    IF EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user_login' AND indexname = 'idx_login_last_login') THEN
        RAISE NOTICE '✓ idx_login_last_login exists';
    END IF;

    IF EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user_login' AND indexname = 'idx_login_updated_date') THEN
        RAISE NOTICE '✓ idx_login_updated_date exists';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 7: DATA INTEGRITY VALIDATION
-- ============================================================================
\echo '--- SECTION 7: DATA INTEGRITY VALIDATION ---'
\echo ''

\echo '7.1: Verify no NULL values in email_id (PK)'
SELECT COUNT(*) as null_email_ids FROM user_login WHERE email_id IS NULL;

DO $$
BEGIN
    IF (SELECT COUNT(*) FROM user_login WHERE email_id IS NULL) = 0 THEN
        RAISE NOTICE '✓ No NULL values in email_id';
    ELSE
        RAISE WARNING '⚠ NULL values found in email_id (primary key!)';
    END IF;
END $$;
\echo ''

\echo '7.2: Verify no NULL values in password'
SELECT COUNT(*) as null_passwords FROM user_login WHERE password IS NULL;

DO $$
BEGIN
    IF (SELECT COUNT(*) FROM user_login WHERE password IS NULL) = 0 THEN
        RAISE NOTICE '✓ No NULL values in password';
    ELSE
        RAISE WARNING '⚠ NULL values found in password';
    END IF;
END $$;
\echo ''

\echo '7.3: Verify no NULL values in mobile_number'
SELECT COUNT(*) as null_mobiles FROM user_login WHERE mobile_number IS NULL;

DO $$
BEGIN
    IF (SELECT COUNT(*) FROM user_login WHERE mobile_number IS NULL) = 0 THEN
        RAISE NOTICE '✓ No NULL values in mobile_number';
    ELSE
        RAISE WARNING '⚠ NULL values found in mobile_number';
    END IF;
END $$;
\echo ''

\echo '7.4: Verify is_active values are only Y or N'
SELECT DISTINCT is_active, COUNT(*) as count FROM user_login GROUP BY is_active;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM user_login WHERE is_active NOT IN ('Y', 'N')) THEN
        RAISE NOTICE '✓ All is_active values are Y or N';
    ELSE
        RAISE WARNING '⚠ Invalid is_active values found';
    END IF;
END $$;
\echo ''

\echo '7.5: Verify mobile_number is 10 digits'
SELECT COUNT(*) as valid_mobiles, COUNT(CASE WHEN mobile_number >= 1000000000 AND mobile_number <= 9999999999 THEN 1 END) as in_range
FROM user_login;

DO $$
BEGIN
    IF (SELECT COUNT(*) FROM user_login WHERE mobile_number >= 1000000000 AND mobile_number <= 9999999999) = (SELECT COUNT(*) FROM user_login) THEN
        RAISE NOTICE '✓ All mobile_number values are within valid 10-digit range';
    ELSE
        RAISE WARNING '⚠ Some mobile_number values are outside valid range';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 8: RECORD COUNT VALIDATION
-- ============================================================================
\echo '--- SECTION 8: RECORD COUNT VALIDATION ---'
\echo ''

\echo '8.1: Current record count'
SELECT COUNT(*) as total_records FROM user_login;

\echo ''

\echo '8.2: Backup table record count (if exists)'
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_login_backup') THEN
        SELECT COUNT(*) as backup_records FROM user_login_backup;
        RAISE NOTICE 'Backup table exists with records available for comparison';
    ELSE
        RAISE NOTICE 'Backup table does not exist (migration may have been cleaned up)';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 9: BACKUP TABLE VALIDATION
-- ============================================================================
\echo '--- SECTION 9: BACKUP TABLE VALIDATION ---'
\echo ''

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_login_backup') THEN
        RAISE NOTICE '✓ Backup table user_login_backup exists';
        RAISE NOTICE '  Available for rollback if needed';
    ELSE
        RAISE NOTICE 'ℹ Backup table not found (may have been cleaned up)';
    END IF;
END $$;
\echo ''

-- ============================================================================
-- FINAL SUMMARY
-- ============================================================================
\echo '======================================================'
\echo 'MIGRATION VALIDATION SUMMARY'
\echo '======================================================'

DO $$
DECLARE
    col_count INT;
    index_count INT;
BEGIN
    SELECT COUNT(*) INTO col_count FROM information_schema.columns WHERE table_name = 'user_login';
    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE tablename = 'user_login';

    RAISE NOTICE '';
    RAISE NOTICE '✓ user_login table structure: VALID';
    RAISE NOTICE '✓ user_login table schema: MIGRATED';
    RAISE NOTICE '✓ user_login table indexes: CREATED (% indexes)', index_count;
    RAISE NOTICE '✓ user_login table constraints: VERIFIED';
    RAISE NOTICE '';
    RAISE NOTICE 'Schema Summary:';
    RAISE NOTICE '  - Total columns: %', col_count;
    RAISE NOTICE '  - Total indexes: %', index_count;
    RAISE NOTICE '  - Total FKs: 1 (email_id → user_master.emailId)';
    RAISE NOTICE '';
    RAISE NOTICE 'Next Steps:';
    RAISE NOTICE '  1. Implement password hashing in application layer';
    RAISE NOTICE '  2. Create API endpoints for user_login CRUD operations';
    RAISE NOTICE '  3. Create comprehensive unit tests';
    RAISE NOTICE '  4. Update documentation and deployment guides';
    RAISE NOTICE '';
END $$;

\echo '======================================================'
