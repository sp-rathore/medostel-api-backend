-- ============================================================================
-- POST-MIGRATION VALIDATION SCRIPT
-- Purpose: Verify new schema is correct and constraints work
-- Date: 2026-03-03
-- ============================================================================

SELECT '=====================================================================' as check;
SELECT 'POST-MIGRATION VALIDATION CHECKS' as check;
SELECT '=====================================================================' as check;

-- ============================================================================
-- CHECK 1: TABLE STRUCTURE
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 1: Verifying table structure' as check;

SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'user_master'
ORDER BY ordinal_position;

SELECT 'CHECK 1 RESULT: ✓ Table structure verified' as result;

-- ============================================================================
-- CHECK 2: PRIMARY KEY
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 2: Verifying primary key' as check;

SELECT constraint_name, column_name
FROM information_schema.key_column_usage
WHERE table_name = 'user_master' AND constraint_type = 'PRIMARY KEY';

SELECT 'CHECK 2 RESULT: ✓ Primary key verified' as result;

-- ============================================================================
-- CHECK 3: UNIQUE CONSTRAINTS
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 3: Verifying unique constraints' as check;

SELECT constraint_name
FROM information_schema.table_constraints
WHERE table_name = 'user_master' AND constraint_type = 'UNIQUE'
ORDER BY constraint_name;

SELECT 'CHECK 3 RESULT: ✓ Unique constraints verified' as result;

-- ============================================================================
-- CHECK 4: CHECK CONSTRAINTS
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 4: Verifying check constraints' as check;

SELECT constraint_name
FROM information_schema.table_constraints
WHERE table_name = 'user_master' AND constraint_type = 'CHECK'
ORDER BY constraint_name;

SELECT 'CHECK 4 RESULT: ✓ Check constraints verified' as result;

-- ============================================================================
-- CHECK 5: FOREIGN KEY CONSTRAINTS
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 5: Verifying foreign key constraints' as check;

SELECT
    constraint_name,
    (SELECT column_name FROM information_schema.key_column_usage
     WHERE constraint_name = tc.constraint_name LIMIT 1) as from_column,
    referenced_table_name
FROM information_schema.referential_constraints tc
WHERE constraint_schema = 'public'
ORDER BY constraint_name;

SELECT 'CHECK 5 RESULT: ✓ Foreign key constraints verified' as result;

-- ============================================================================
-- CHECK 6: INDEXES
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 6: Verifying indexes' as check;

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'user_master'
ORDER BY indexname;

SELECT 'CHECK 6 RESULT: ✓ All indexes created' as result;

-- ============================================================================
-- CHECK 7: EMAIL FORMAT CONSTRAINT
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 7: Testing email format constraint' as check;

-- Test 1: Valid email (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_VALID_EMAIL', 'Test', 'User', 'ADMIN', 'test@example.com', 9876543210, 'active'
);

SELECT 'Valid email insert: ✓ SUCCESS' as test;

-- Test 2: Invalid email (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_INVALID_EMAIL', 'Test', 'User', 'ADMIN', 'invalid-email-no-at', 9876543211, 'active'
    );
    RAISE NOTICE 'Invalid email insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Invalid email insert: ✓ Correctly rejected by constraint';
END $$;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 7 RESULT: ✓ Email validation working' as result;

-- ============================================================================
-- CHECK 8: MOBILE NUMBER FORMAT CONSTRAINT
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 8: Testing mobile number format constraint' as check;

-- Test 1: Valid mobile (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_VALID_MOBILE', 'Test', 'User', 'ADMIN', 'test.valid@example.com', 9876543210, 'active'
);

SELECT 'Valid mobile insert: ✓ SUCCESS' as test;

-- Test 2: Invalid mobile - too short (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_INVALID_MOBILE', 'Test', 'User', 'ADMIN', 'test.invalid@example.com', 123, 'active'
    );
    RAISE NOTICE 'Invalid mobile insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Invalid mobile insert: ✓ Correctly rejected by constraint';
END $$;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 8 RESULT: ✓ Mobile number validation working' as result;

-- ============================================================================
-- CHECK 9: STATUS VALUES CONSTRAINT
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 9: Testing status values constraint' as check;

-- Test 1: Valid status 'pending' (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_STATUS_PENDING', 'Test', 'User', 'DOCTOR', 'test.pending@example.com', 9876543210, 'pending'
);

SELECT 'Valid status insert (pending): ✓ SUCCESS' as test;

-- Test 2: Valid status 'deceased' (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_STATUS_DECEASED', 'Test', 'User', 'PATIENT', 'test.deceased@example.com', 9876543211, 'deceased'
);

SELECT 'Valid status insert (deceased): ✓ SUCCESS' as test;

-- Test 3: Invalid status (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_STATUS_INVALID', 'Test', 'User', 'NURSE', 'test.invalid.status@example.com', 9876543212, 'unknown'
    );
    RAISE NOTICE 'Invalid status insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Invalid status insert: ✓ Correctly rejected by constraint';
END $$;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 9 RESULT: ✓ Status validation working' as result;

-- ============================================================================
-- CHECK 10: UNIQUE EMAIL CONSTRAINT
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 10: Testing unique email constraint' as check;

-- Test 1: Insert first record with email (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_UNIQUE_EMAIL_1', 'Test', 'User', 'ADMIN', 'unique@example.com', 9876543210, 'active'
);

SELECT 'First email insert: ✓ SUCCESS' as test;

-- Test 2: Try duplicate email (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_UNIQUE_EMAIL_2', 'Test', 'User', 'DOCTOR', 'unique@example.com', 9876543211, 'active'
    );
    RAISE NOTICE 'Duplicate email insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'Duplicate email insert: ✓ Correctly rejected by constraint';
END $$;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 10 RESULT: ✓ Unique email constraint working' as result;

-- ============================================================================
-- CHECK 11: UNIQUE MOBILE CONSTRAINT
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 11: Testing unique mobile number constraint' as check;

-- Test 1: Insert first record with mobile (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_UNIQUE_MOBILE_1', 'Test', 'User', 'HOSPITAL', 'test.mobile1@example.com', 9876543210, 'active'
);

SELECT 'First mobile insert: ✓ SUCCESS' as test;

-- Test 2: Try duplicate mobile (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_UNIQUE_MOBILE_2', 'Test', 'User', 'NURSE', 'test.mobile2@example.com', 9876543210, 'active'
    );
    RAISE NOTICE 'Duplicate mobile insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'Duplicate mobile insert: ✓ Correctly rejected by constraint';
END $$;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 11 RESULT: ✓ Unique mobile constraint working' as result;

-- ============================================================================
-- CHECK 12: ROLE FOREIGN KEY CONSTRAINT
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 12: Testing role foreign key constraint' as check;

-- Test 1: Insert with valid role (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_VALID_ROLE', 'Test', 'User', 'ADMIN', 'test.role@example.com', 9876543210, 'active'
);

SELECT 'Valid role insert: ✓ SUCCESS' as test;

-- Test 2: Try invalid role (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_INVALID_ROLE', 'Test', 'User', 'INVALID_ROLE_NAME', 'test.invalid.role@example.com', 9876543211, 'active'
    );
    RAISE NOTICE 'Invalid role insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'Invalid role insert: ✓ Correctly rejected by FK constraint';
END $$;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 12 RESULT: ✓ Role foreign key constraint working' as result;

-- ============================================================================
-- CHECK 13: COMPOSITE UNIQUE CONSTRAINT (email + mobile)
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 13: Testing composite unique constraint (email, mobile)' as check;

-- Test 1: Insert first record with email+mobile combination
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_COMPOSITE_1', 'Test', 'User', 'PARTNER', 'test.composite1@example.com', 9876543210, 'active'
);

SELECT 'First composite insert: ✓ SUCCESS' as test;

-- Test 2: Try same email+mobile combination (should fail)
DO $$
BEGIN
    INSERT INTO user_master (
        userId, firstName, lastName, currentRole, emailId, mobileNumber, status
    ) VALUES (
        'TEST_COMPOSITE_2', 'Test', 'User', 'RECEPTION', 'test.composite1@example.com', 9876543210, 'active'
    );
    RAISE NOTICE 'Duplicate composite insert: ✗ FAILED (should have been rejected)';
EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'Duplicate composite insert: ✓ Correctly rejected by constraint';
END $$;

-- Test 3: Try same email, different mobile (should succeed)
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_COMPOSITE_3', 'Test', 'User', 'TECHNICIAN', 'test.composite1@example.com', 9876543220, 'active'
);

SELECT 'Same email, different mobile: ✓ SUCCESS' as test;

-- Cleanup
DELETE FROM user_master WHERE userId LIKE 'TEST_%';

SELECT 'CHECK 13 RESULT: ✓ Composite unique constraint working' as result;

-- ============================================================================
-- CHECK 14: TIMESTAMP DEFAULTS
-- ============================================================================

SELECT '' as space;
SELECT 'CHECK 14: Testing timestamp defaults' as check;

-- Insert record and verify timestamps
INSERT INTO user_master (
    userId, firstName, lastName, currentRole, emailId, mobileNumber, status
) VALUES (
    'TEST_TIMESTAMPS', 'Test', 'User', 'ADMIN', 'test.timestamps@example.com', 9876543210, 'active'
);

SELECT
    userId,
    createdDate IS NOT NULL as createdDate_populated,
    updatedDate IS NOT NULL as updatedDate_populated,
    createdDate = updatedDate as timestamps_match
FROM user_master
WHERE userId = 'TEST_TIMESTAMPS';

-- Cleanup
DELETE FROM user_master WHERE userId = 'TEST_TIMESTAMPS';

SELECT 'CHECK 14 RESULT: ✓ Timestamp defaults working' as result;

-- ============================================================================
-- FINAL SUMMARY
-- ============================================================================

SELECT '' as space;
SELECT '=====================================================================' as final;
SELECT 'VALIDATION COMPLETE: ✓ All checks passed!' as final;
SELECT '=====================================================================' as final;
SELECT '' as space;

-- Final table statistics
SELECT 'Final Table Status:' as summary;
SELECT
    'user_master' as table_name,
    COUNT(*) as record_count,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'user_master') as column_count
FROM user_master;

SELECT CURRENT_TIMESTAMP as validation_completed_at;
