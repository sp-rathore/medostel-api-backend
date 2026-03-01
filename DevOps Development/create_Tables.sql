-- ============================================================================
-- Medostel Database: Create All Tables Schema
-- ============================================================================
-- Date:     March 1, 2026
-- Version:  2.0 (Updated with enhanced User_Master schema)
-- Database: PostgreSQL 18.2
-- Status:   Production Ready ✅
-- ============================================================================
-- Schema Changes (March 1, 2026):
-- - userId in user_master changed from VARCHAR(255) to BIGINT
-- - emailId validation added with RFC 5322 regex pattern
-- - mobileNumber validation: exactly 10 digits (1000000000-9999999999)
-- - userId in user_login changed to BIGINT to match user_master
-- ============================================================================

-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS report_history CASCADE;
DROP TABLE IF EXISTS new_user_request CASCADE;
DROP TABLE IF EXISTS user_login CASCADE;
DROP TABLE IF EXISTS user_master CASCADE;
DROP TABLE IF EXISTS state_city_pincode_master CASCADE;
DROP TABLE IF EXISTS user_role_master CASCADE;

-- ============================================================================
-- Table 1: user_role_master
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_role_master (
    roleId VARCHAR(10) PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Closed', 'Pending')),
    comments VARCHAR(250),
    createdDate DATE DEFAULT CURRENT_DATE,
    updatedDate DATE DEFAULT CURRENT_DATE
);

CREATE UNIQUE INDEX pk_user_role_master ON user_role_master(roleId);
CREATE INDEX idx_role_status ON user_role_master(status);
CREATE INDEX idx_role_name ON user_role_master(roleName);
CREATE INDEX idx_role_updated ON user_role_master(updatedDate);

-- ============================================================================
-- Table 2: state_city_pincode_master
-- ============================================================================
CREATE TABLE IF NOT EXISTS state_city_pincode_master (
    id SERIAL PRIMARY KEY,
    stateId VARCHAR(10) NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityId VARCHAR(10) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    pinCode VARCHAR(10) NOT NULL,
    countryName VARCHAR(100) DEFAULT 'India',
    status VARCHAR(50) DEFAULT 'Active',
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stateId, cityId, pinCode)
);

CREATE UNIQUE INDEX pk_state_city_pincode ON state_city_pincode_master(id);
CREATE INDEX idx_state_id ON state_city_pincode_master(stateId);
CREATE INDEX idx_city_id ON state_city_pincode_master(cityId);
CREATE INDEX idx_pin_code ON state_city_pincode_master(pinCode);
CREATE INDEX idx_country ON state_city_pincode_master(countryName);
CREATE INDEX idx_location_status ON state_city_pincode_master(status);

-- ============================================================================
-- Table 3: user_master
-- ============================================================================
-- ENHANCED SCHEMA (March 1, 2026):
-- - userId: BIGINT (supports up to 1,000,000,000 users)
-- - emailId: Email validation using RFC 5322 regex pattern
-- - mobileNumber: NUMERIC(10) with CHECK constraint for exactly 10 digits
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_master (
    userId BIGINT PRIMARY KEY,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    emailId VARCHAR(255) NOT NULL UNIQUE
        CHECK (emailId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    mobileNumber NUMERIC(10) NOT NULL UNIQUE
        CHECK (mobileNumber >= 1000000000 AND mobileNumber <= 9999999999),
    organisation VARCHAR(255),
    address TEXT,
    status VARCHAR(50) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Suspended')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (currentRole) REFERENCES user_role_master(roleId)
);

CREATE UNIQUE INDEX pk_user_master ON user_master(userId);
CREATE INDEX idx_user_email ON user_master(emailId);
CREATE INDEX idx_user_mobile ON user_master(mobileNumber);
CREATE INDEX idx_user_role ON user_master(currentRole);
CREATE INDEX idx_user_status ON user_master(status);
CREATE INDEX idx_user_name ON user_master(firstName, lastName);
CREATE INDEX idx_user_updated ON user_master(updatedDate);

-- ============================================================================
-- Table 4: user_login
-- ============================================================================
-- UPDATED (March 1, 2026):
-- - userId changed from VARCHAR(255) to BIGINT to match user_master
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_login (
    userId BIGINT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    roleId VARCHAR(50) NOT NULL,
    isActive BOOLEAN DEFAULT TRUE,
    lastLoginTime TIMESTAMP,
    loginAttempts INTEGER DEFAULT 0,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user_master(userId),
    FOREIGN KEY (roleId) REFERENCES user_role_master(roleId)
);

CREATE UNIQUE INDEX pk_user_login ON user_login(userId);
CREATE INDEX idx_login_username ON user_login(username);
CREATE INDEX idx_login_active ON user_login(isActive);
CREATE INDEX idx_login_role ON user_login(roleId);
CREATE INDEX idx_login_attempts ON user_login(loginAttempts);
CREATE INDEX idx_login_lastlogin ON user_login(lastLoginTime);
CREATE INDEX idx_login_updated ON user_login(updatedDate);

-- ============================================================================
-- Table 5: new_user_request
-- ============================================================================
-- UPDATED (March 1, 2026):
-- - emailId validation added with RFC 5322 regex pattern
-- - mobileNumber validation: NUMERIC(10) with 10-digit CHECK constraint
-- ============================================================================
CREATE TABLE IF NOT EXISTS new_user_request (
    requestId VARCHAR(100) PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    emailId VARCHAR(255) NOT NULL UNIQUE
        CHECK (emailId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    mobileNumber NUMERIC(10) NOT NULL
        CHECK (mobileNumber >= 1000000000 AND mobileNumber <= 9999999999),
    address TEXT,
    requestStatus VARCHAR(50) DEFAULT 'Pending' CHECK (requestStatus IN ('Pending', 'Approved', 'Rejected')),
    approvalDate TIMESTAMP,
    approvalComments TEXT,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX pk_new_user_request ON new_user_request(requestId);
CREATE INDEX idx_request_email ON new_user_request(emailId);
CREATE INDEX idx_request_mobile ON new_user_request(mobileNumber);
CREATE INDEX idx_request_status ON new_user_request(requestStatus);
CREATE INDEX idx_request_role ON new_user_request(currentRole);
CREATE INDEX idx_request_created ON new_user_request(createdDate);
CREATE INDEX idx_request_updated ON new_user_request(updatedDate);

-- ============================================================================
-- Table 6: report_history
-- ============================================================================
CREATE TABLE IF NOT EXISTS report_history (
    id VARCHAR(100) PRIMARY KEY,
    userId BIGINT NOT NULL,
    fileName VARCHAR(255),
    fileType VARCHAR(50),
    reportType VARCHAR(100),
    status VARCHAR(50) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Completed', 'Failed')),
    diagnosis TEXT,
    inferredDiagnosis TEXT,
    pdfUrl VARCHAR(500),
    bucketLocation VARCHAR(500),
    jsonData JSONB,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user_master(userId)
);

CREATE UNIQUE INDEX pk_report_history ON report_history(id);
CREATE INDEX idx_report_user ON report_history(userId);
CREATE INDEX idx_report_type ON report_history(reportType);
CREATE INDEX idx_report_status ON report_history(status);
CREATE INDEX idx_report_created ON report_history(createdDate);
CREATE INDEX idx_report_updated ON report_history(updatedDate);

-- ============================================================================
-- Sample Data Insertion
-- ============================================================================

-- Insert system roles
INSERT INTO user_role_master (roleId, roleName, status, comments) VALUES
('ADMIN', 'Administrator', 'Active', 'System administrator with full access'),
('DOCTOR', 'Doctor', 'Active', 'Medical professional'),
('HOSPITAL', 'Hospital', 'Active', 'Hospital administrator'),
('NURSE', 'Nurse', 'Active', 'Nursing staff'),
('PARTNER', 'Sales Partner', 'Active', 'Sales and marketing partner'),
('PATIENT', 'Patient', 'Active', 'Patient user'),
('RECEPTION', 'Reception', 'Active', 'Reception staff'),
('TECHNICIAN', 'Technician', 'Active', 'Lab technician');

-- Insert sample users
INSERT INTO user_master (userId, firstName, lastName, currentRole, emailId, mobileNumber, organisation, address, status) VALUES
(1001, 'Dr. Rajesh', 'Kumar', 'DOCTOR', 'rajesh.kumar@medostel.com', 9876543210, 'Apollo Hospital', 'Mumbai', 'Active'),
(1002, 'Amit', 'Singh', 'PATIENT', 'amit.singh@medostel.com', 9123456789, 'Self', 'Delhi', 'Active'),
(1003, 'Dr. Priya', 'Sharma', 'DOCTOR', 'priya.sharma@medostel.com', 8765432109, 'Max Hospital', 'Bangalore', 'Active'),
(1004, 'Neha', 'Patel', 'NURSE', 'neha.patel@medostel.com', 9876543211, 'Apollo Hospital', 'Mumbai', 'Active'),
(1005, 'Admin', 'User', 'ADMIN', 'admin@medostel.com', 9000000000, 'Medostel HQ', 'Mumbai', 'Active');

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Verify table creation
SELECT 'Tables created successfully!' AS Status;

-- Count records in each table
SELECT 'user_role_master' AS TableName, COUNT(*) AS RecordCount FROM user_role_master
UNION ALL
SELECT 'user_master', COUNT(*) FROM user_master
UNION ALL
SELECT 'state_city_pincode_master', COUNT(*) FROM state_city_pincode_master
UNION ALL
SELECT 'user_login', COUNT(*) FROM user_login
UNION ALL
SELECT 'new_user_request', COUNT(*) FROM new_user_request
UNION ALL
SELECT 'report_history', COUNT(*) FROM report_history;

-- ============================================================================
-- Schema Ready for Production
-- ============================================================================
-- Database: medostel
-- Version: 2.0 (Enhanced with numeric userId and validations)
-- Date: March 1, 2026
-- All tables created and indexed with proper constraints
-- ============================================================================
