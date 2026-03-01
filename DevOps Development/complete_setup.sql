-- ============================================================================
-- Medostel Database - Complete Role & Password Setup
-- ============================================================================
-- This script:
-- 1. Creates admin and API roles
-- 2. Creates users with secure passwords
-- 3. Grants appropriate permissions
-- ============================================================================

-- Connect to the Medostel database
\c Medostel

-- ============================================================================
-- PART 1: CREATE ROLES
-- ============================================================================

CREATE ROLE medostel_admin WITH
  CREATEDB
  CREATEROLE
  SUPERUSER
  NOINHERIT;

CREATE ROLE medostel_api WITH
  NOINHERIT
  NOSUPERUSER;

-- ============================================================================
-- PART 2: CREATE USERS WITH SECURE PASSWORDS
-- ============================================================================

CREATE USER medostel_admin_user WITH
  PASSWORD 'Iag2bMi@0@6aA'
  IN ROLE medostel_admin;

CREATE USER medostel_api_user WITH
  PASSWORD 'Iag2bMi@0@6aD'
  IN ROLE medostel_api;

-- ============================================================================
-- PART 3: GRANT DATABASE PERMISSIONS
-- ============================================================================

GRANT ALL PRIVILEGES ON DATABASE "Medostel" TO medostel_admin;
GRANT CONNECT ON DATABASE "Medostel" TO medostel_api;

-- ============================================================================
-- PART 4: GRANT SCHEMA PERMISSIONS
-- ============================================================================

GRANT USAGE ON SCHEMA public TO medostel_api;
GRANT CREATE ON SCHEMA public TO medostel_api;

-- ============================================================================
-- PART 5: SET DEFAULT PRIVILEGES
-- ============================================================================

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO medostel_api;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO medostel_api;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

\du+

SELECT 'Setup complete!' as status;
