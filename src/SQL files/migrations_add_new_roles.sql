-- ============================================================================
-- Medostel Database: Add New Roles Migration
-- ============================================================================
-- Date:     March 1, 2026
-- Purpose:  Add Hospital and Sales_Partner roles to user_role_master table
-- Status:   Ready for deployment
-- ============================================================================

-- Verify connection
SELECT 'Connected to Medostel Database' AS Status, NOW() AS Timestamp;

-- ============================================================================
-- Step 1: Add Hospital Role
-- ============================================================================
INSERT INTO user_role_master (roleId, roleName, status, comments)
VALUES (
    'ROLE_HOSPITAL',
    'Hospital',
    'Active',
    'Hospital administrator - manages hospital operations and staff'
)
ON CONFLICT (roleId) DO UPDATE SET
    status = EXCLUDED.status,
    comments = EXCLUDED.comments,
    updatedDate = CURRENT_TIMESTAMP;

SELECT 'Hospital role added/updated' AS Status;

-- ============================================================================
-- Step 2: Add Sales_Partner Role
-- ============================================================================
INSERT INTO user_role_master (roleId, roleName, status, comments)
VALUES (
    'ROLE_SALES_PARTNER',
    'Sales Partner',
    'Active',
    'Sales and marketing partner - manages partnerships and revenue'
)
ON CONFLICT (roleId) DO UPDATE SET
    status = EXCLUDED.status,
    comments = EXCLUDED.comments,
    updatedDate = CURRENT_TIMESTAMP;

SELECT 'Sales Partner role added/updated' AS Status;

-- ============================================================================
-- Step 3: Verify All Roles
-- ============================================================================
SELECT
    'Role Verification' AS Status,
    COUNT(*) AS TotalRoles,
    COUNT(CASE WHEN status = 'Active' THEN 1 END) AS ActiveRoles,
    COUNT(CASE WHEN status = 'Inactive' THEN 1 END) AS InactiveRoles
FROM user_role_master;

-- ============================================================================
-- Step 4: Display All Roles
-- ============================================================================
SELECT
    roleId,
    roleName,
    status,
    comments,
    createdDate,
    updatedDate
FROM user_role_master
ORDER BY createdDate ASC;

-- ============================================================================
-- Step 5: Verify Foreign Key References
-- ============================================================================
SELECT
    'User_Master References' AS Check_Type,
    COUNT(DISTINCT currentRole) AS UniqueRolesReferenced
FROM user_master;

SELECT
    'User_Login References' AS Check_Type,
    COUNT(DISTINCT roleId) AS UniqueRolesReferenced
FROM user_login;

-- ============================================================================
-- Migration Complete
-- ============================================================================
SELECT
    'Migration completed successfully!' AS Status,
    NOW() AS CompletionTime,
    'Both new roles (Hospital and Sales Partner) have been added to user_role_master' AS Details;

-- ============================================================================
-- Rollback Script (if needed)
-- ============================================================================
-- To rollback this migration, execute:
-- DELETE FROM user_role_master WHERE roleId IN ('ROLE_HOSPITAL', 'ROLE_SALES_PARTNER');
-- SELECT 'Rollback completed' AS Status;
-- ============================================================================
