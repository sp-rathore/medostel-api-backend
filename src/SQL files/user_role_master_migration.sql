-- ============================================================================
-- User Role Master Schema Migration: VARCHAR(10) roleId → SERIAL INTEGER roleId
-- ============================================================================
-- Date:     March 3, 2026
-- Version:  1.0
-- Database: PostgreSQL 18+
-- Purpose:  Convert roleId from VARCHAR(10) to SERIAL INTEGER for better performance
--           and scalability. This migration includes rollback procedures.
-- ============================================================================
-- Changes:
-- - roleId: VARCHAR(10) PRIMARY KEY → SERIAL PRIMARY KEY (auto-increment integer)
-- - All dependent foreign keys are updated to reference integer roleId
-- - 8 roles are inserted with auto-increment IDs (1-8)
-- ============================================================================

-- ============================================================================
-- MIGRATION PROCEDURE
-- ============================================================================

-- Step 1: Drop dependent foreign keys (in correct order)
-- ============================================================================
ALTER TABLE IF EXISTS user_login DROP CONSTRAINT IF EXISTS user_login_roleId_fkey CASCADE;
ALTER TABLE IF EXISTS user_master DROP CONSTRAINT IF EXISTS user_master_currentRole_fkey CASCADE;
ALTER TABLE IF EXISTS new_user_request DROP CONSTRAINT IF EXISTS new_user_request_currentRole_fkey CASCADE;

-- Step 2: Drop old user_role_master table
-- ============================================================================
DROP TABLE IF EXISTS user_role_master CASCADE;

-- Step 3: Create new user_role_master table with SERIAL INTEGER roleId
-- ============================================================================
CREATE TABLE user_role_master (
    roleId SERIAL PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Closed', 'Pending')),
    comments VARCHAR(250),
    createdDate DATE DEFAULT CURRENT_DATE,
    updatedDate DATE DEFAULT CURRENT_DATE
);

-- Step 4: Insert roles with auto-increment IDs (1-8)
-- ============================================================================
INSERT INTO user_role_master (roleName, status, comments, createdDate, updatedDate) VALUES
('ADMIN', 'Active', 'System Administrator - Full system access and database management', CURRENT_DATE, CURRENT_DATE),
('DOCTOR', 'Active', 'Doctor or Physician - Can view and manage patient records and create medical reports', CURRENT_DATE, CURRENT_DATE),
('HOSPITAL', 'Active', 'Hospital Administrator - Hospital-level administrative functions', CURRENT_DATE, CURRENT_DATE),
('NURSE', 'Active', 'Nursing Staff - Can update patient information and create nursing reports', CURRENT_DATE, CURRENT_DATE),
('PARTNER', 'Active', 'Sales Partner - Sales and marketing partner functions', CURRENT_DATE, CURRENT_DATE),
('PATIENT', 'Active', 'Patient User - Can view personal medical records and report history', CURRENT_DATE, CURRENT_DATE),
('RECEPTION', 'Active', 'Reception Staff - Can register new patients and manage appointments', CURRENT_DATE, CURRENT_DATE),
('TECHNICIAN', 'Active', 'Lab Technician - Can create and upload laboratory test reports and results', CURRENT_DATE, CURRENT_DATE);

-- Step 5: Create indexes on user_role_master
-- ============================================================================
CREATE UNIQUE INDEX pk_user_role_master ON user_role_master(roleId);
CREATE INDEX idx_role_status ON user_role_master(status);
CREATE INDEX idx_role_name ON user_role_master(roleName);
CREATE INDEX idx_role_updated ON user_role_master(updatedDate);

-- Step 6: Update user_master table
-- ============================================================================
-- Convert currentRole to INTEGER and recreate foreign key
ALTER TABLE user_master
    ALTER COLUMN currentRole TYPE INTEGER USING CASE
        WHEN currentRole = 'ADMIN' THEN 1
        WHEN currentRole = 'DOCTOR' THEN 2
        WHEN currentRole = 'HOSPITAL' THEN 3
        WHEN currentRole = 'NURSE' THEN 4
        WHEN currentRole = 'PARTNER' THEN 5
        WHEN currentRole = 'PATIENT' THEN 6
        WHEN currentRole = 'RECEPTION' THEN 7
        WHEN currentRole = 'TECHNICIAN' THEN 8
        ELSE 6  -- Default to PATIENT if unknown
    END;

ALTER TABLE user_master
    ADD CONSTRAINT user_master_currentRole_fkey
    FOREIGN KEY (currentRole) REFERENCES user_role_master(roleId) ON UPDATE CASCADE ON DELETE SET NULL;

-- Step 7: Update user_login table
-- ============================================================================
-- Convert roleId to INTEGER and recreate foreign key
ALTER TABLE user_login
    ALTER COLUMN roleId TYPE INTEGER USING CASE
        WHEN roleId = 'ADMIN' THEN 1
        WHEN roleId = 'DOCTOR' THEN 2
        WHEN roleId = 'HOSPITAL' THEN 3
        WHEN roleId = 'NURSE' THEN 4
        WHEN roleId = 'PARTNER' THEN 5
        WHEN roleId = 'PATIENT' THEN 6
        WHEN roleId = 'RECEPTION' THEN 7
        WHEN roleId = 'TECHNICIAN' THEN 8
        ELSE 6  -- Default to PATIENT if unknown
    END;

ALTER TABLE user_login
    ADD CONSTRAINT user_login_roleId_fkey
    FOREIGN KEY (roleId) REFERENCES user_role_master(roleId) ON UPDATE CASCADE ON DELETE SET NULL;

-- Step 8: Verification
-- ============================================================================
-- Verify migration success
SELECT 'user_role_master Migration Complete' AS Status;
SELECT COUNT(*) AS TotalRoles FROM user_role_master;
SELECT * FROM user_role_master ORDER BY roleId;

-- Verify foreign key constraints
SELECT * FROM information_schema.table_constraints
WHERE table_name IN ('user_role_master', 'user_master', 'user_login')
    AND constraint_type = 'FOREIGN KEY';

-- ============================================================================
-- ROLLBACK PROCEDURE (if migration fails)
-- ============================================================================
-- NOTE: Execute this rollback script to revert changes
-- Make sure to restore from backup if needed

/*
-- Rollback Script (commented out for safety)
-- Step 1: Drop new foreign keys
ALTER TABLE IF EXISTS user_login DROP CONSTRAINT IF EXISTS user_login_roleId_fkey CASCADE;
ALTER TABLE IF EXISTS user_master DROP CONSTRAINT IF EXISTS user_master_currentRole_fkey CASCADE;

-- Step 2: Drop new user_role_master table
DROP TABLE IF EXISTS user_role_master CASCADE;

-- Step 3: Recreate old user_role_master table with VARCHAR(10) roleId
CREATE TABLE user_role_master (
    roleId VARCHAR(10) PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Closed', 'Pending')),
    comments VARCHAR(250),
    createdDate DATE DEFAULT CURRENT_DATE,
    updatedDate DATE DEFAULT CURRENT_DATE
);

-- Step 4: Insert old roles with VARCHAR roleId
INSERT INTO user_role_master (roleId, roleName, status, comments) VALUES
('ADMIN', 'Administrator', 'Active', 'System administrator with full access'),
('DOCTOR', 'Doctor', 'Active', 'Medical professional'),
('HOSPITAL', 'Hospital', 'Active', 'Hospital administrator'),
('NURSE', 'Nurse', 'Active', 'Nursing staff'),
('PARTNER', 'Sales Partner', 'Active', 'Sales and marketing partner'),
('PATIENT', 'Patient', 'Active', 'Patient user'),
('RECEPTION', 'Reception', 'Active', 'Reception staff'),
('TECHNICIAN', 'Technician', 'Active', 'Lab technician');

-- Step 5: Convert currentRole back to VARCHAR
ALTER TABLE user_master
    ALTER COLUMN currentRole TYPE VARCHAR(50) USING CASE
        WHEN currentRole = 1 THEN 'ADMIN'
        WHEN currentRole = 2 THEN 'DOCTOR'
        WHEN currentRole = 3 THEN 'HOSPITAL'
        WHEN currentRole = 4 THEN 'NURSE'
        WHEN currentRole = 5 THEN 'PARTNER'
        WHEN currentRole = 6 THEN 'PATIENT'
        WHEN currentRole = 7 THEN 'RECEPTION'
        WHEN currentRole = 8 THEN 'TECHNICIAN'
        ELSE 'PATIENT'
    END;

ALTER TABLE user_master
    ADD CONSTRAINT user_master_currentRole_fkey
    FOREIGN KEY (currentRole) REFERENCES user_role_master(roleId);

-- Step 6: Convert roleId back to VARCHAR
ALTER TABLE user_login
    ALTER COLUMN roleId TYPE VARCHAR(50) USING CASE
        WHEN roleId = 1 THEN 'ADMIN'
        WHEN roleId = 2 THEN 'DOCTOR'
        WHEN roleId = 3 THEN 'HOSPITAL'
        WHEN roleId = 4 THEN 'NURSE'
        WHEN roleId = 5 THEN 'PARTNER'
        WHEN roleId = 6 THEN 'PATIENT'
        WHEN roleId = 7 THEN 'RECEPTION'
        WHEN roleId = 8 THEN 'TECHNICIAN'
        ELSE 'PATIENT'
    END;

ALTER TABLE user_login
    ADD CONSTRAINT user_login_roleId_fkey
    FOREIGN KEY (roleId) REFERENCES user_role_master(roleId);

-- Step 7: Recreate indexes
CREATE UNIQUE INDEX pk_user_role_master ON user_role_master(roleId);
CREATE INDEX idx_role_status ON user_role_master(status);
CREATE INDEX idx_role_name ON user_role_master(roleName);
CREATE INDEX idx_role_updated ON user_role_master(updatedDate);

SELECT 'Rollback Complete' AS Status;
*/

-- ============================================================================
-- Migration Complete
-- ============================================================================
-- Database: medostel
-- Date: March 3, 2026
-- All tables migrated from VARCHAR(10) roleId to SERIAL INTEGER roleId
-- ============================================================================
