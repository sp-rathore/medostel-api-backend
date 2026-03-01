-- ============================================================================
-- Medostel Database - Table Creation Script
-- Database: Medostel
-- Engine: PostgreSQL 18
-- Created: 2026-02-28
-- ============================================================================

-- Connect to the Medostel database
\c Medostel

-- ============================================================================
-- TABLE 1: User_Role_Master
-- Description: Master table for user roles
-- ============================================================================

CREATE TABLE IF NOT EXISTS User_Role_Master (
    roleId VARCHAR(10) PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
        CHECK (status IN ('Active', 'Inactive', 'Closed')),
    createdDate DATE NOT NULL DEFAULT CURRENT_DATE,
    updatedDate DATE NOT NULL DEFAULT CURRENT_DATE,
    comments VARCHAR(250)
);

-- Create indexes for User_Role_Master
CREATE INDEX IF NOT EXISTS idx_user_role_name ON User_Role_Master(roleName);
CREATE INDEX IF NOT EXISTS idx_user_role_status ON User_Role_Master(status);

-- ============================================================================
-- TABLE 2: State_City_PinCode_Master
-- Description: Master table for geographic data
-- ============================================================================

CREATE TABLE IF NOT EXISTS State_City_PinCode_Master (
    id SERIAL PRIMARY KEY,
    stateId VARCHAR(10) NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    cityId VARCHAR(10) NOT NULL,
    pinCode VARCHAR(10) NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
        CHECK (status IN ('Active', 'Inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for State_City_PinCode_Master
CREATE INDEX IF NOT EXISTS idx_state_name ON State_City_PinCode_Master(stateName);
CREATE INDEX IF NOT EXISTS idx_city_name ON State_City_PinCode_Master(cityName);
CREATE INDEX IF NOT EXISTS idx_pincode ON State_City_PinCode_Master(pinCode);
CREATE INDEX IF NOT EXISTS idx_state_city ON State_City_PinCode_Master(stateId, cityId);

-- ============================================================================
-- TABLE 3: User_Master
-- Description: Core user profile data
-- Primary Key: userId (Email)
-- ============================================================================

CREATE TABLE IF NOT EXISTS User_Master (
    userId VARCHAR(100) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    organisation VARCHAR(100),
    emailId VARCHAR(100) NOT NULL UNIQUE,
    mobileNumber VARCHAR(15) NOT NULL UNIQUE,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateName VARCHAR(100),
    cityName VARCHAR(100),
    pinCode VARCHAR(10),
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
        CHECK (status IN ('Active', 'Inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (currentRole) REFERENCES User_Role_Master(roleName) ON DELETE RESTRICT
);

-- Create indexes for User_Master
CREATE INDEX IF NOT EXISTS idx_user_email ON User_Master(emailId);
CREATE INDEX IF NOT EXISTS idx_user_mobile ON User_Master(mobileNumber);
CREATE INDEX IF NOT EXISTS idx_user_role ON User_Master(currentRole);
CREATE INDEX IF NOT EXISTS idx_user_status ON User_Master(status);
CREATE INDEX IF NOT EXISTS idx_user_created_date ON User_Master(createdDate);

-- ============================================================================
-- TABLE 4: User_Login
-- Description: Authentication and login credentials
-- Primary Key: userId
-- Foreign Keys: userId -> User_Master, roleId -> User_Role_Master
-- ============================================================================

CREATE TABLE IF NOT EXISTS User_Login (
    userId VARCHAR(100) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    passwordHash VARCHAR(255) NOT NULL,
    mobilePhone VARCHAR(15),
    roleId VARCHAR(10),
    isActive BOOLEAN DEFAULT TRUE,
    lastLoginAt TIMESTAMP,
    passwordLastChangedAt TIMESTAMP,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES User_Master(userId) ON DELETE CASCADE,
    FOREIGN KEY (roleId) REFERENCES User_Role_Master(roleId) ON DELETE SET NULL
);

-- Create indexes for User_Login
CREATE INDEX IF NOT EXISTS idx_login_username ON User_Login(username);
CREATE INDEX IF NOT EXISTS idx_login_role_id ON User_Login(roleId);
CREATE INDEX IF NOT EXISTS idx_login_active ON User_Login(isActive);
CREATE INDEX IF NOT EXISTS idx_login_last_login ON User_Login(lastLoginAt);

-- ============================================================================
-- TABLE 5: New_User_Request
-- Description: Staging table for new user registration requests
-- Primary Key: requestId
-- ============================================================================

CREATE TABLE IF NOT EXISTS New_User_Request (
    requestId VARCHAR(20) PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    organisation VARCHAR(100),
    emailId VARCHAR(100) NOT NULL UNIQUE,
    mobileNumber VARCHAR(15) NOT NULL UNIQUE,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateName VARCHAR(100),
    cityName VARCHAR(100),
    pinCode VARCHAR(10),
    requestStatus VARCHAR(20) NOT NULL DEFAULT 'Pending'
        CHECK (requestStatus IN ('Pending', 'Approved', 'Rejected')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approvedBy VARCHAR(100),
    approvalRemarks TEXT
);

-- Create indexes for New_User_Request
CREATE INDEX IF NOT EXISTS idx_new_user_email ON New_User_Request(emailId);
CREATE INDEX IF NOT EXISTS idx_new_user_status ON New_User_Request(requestStatus);
CREATE INDEX IF NOT EXISTS idx_new_user_created ON New_User_Request(createdDate);

-- ============================================================================
-- TABLE 6: Report_History
-- Description: Medical report analysis history
-- Primary Key: id
-- Foreign Key: userId -> User_Master
-- ============================================================================

CREATE TABLE IF NOT EXISTS Report_History (
    id VARCHAR(50) PRIMARY KEY,
    userId VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fileName VARCHAR(255) NOT NULL,
    fileType VARCHAR(10) NOT NULL
        CHECK (fileType IN ('pdf', 'image', 'doc', 'docx')),
    reportType VARCHAR(100),
    inferredDiagnosis TEXT,
    pdfUrl TEXT,
    bucketLocation VARCHAR(255),
    jsonData JSONB,
    status VARCHAR(20) DEFAULT 'Pending'
        CHECK (status IN ('Pending', 'Processing', 'Completed', 'Error')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES User_Master(userId) ON DELETE CASCADE
);

-- Create indexes for Report_History
CREATE INDEX IF NOT EXISTS idx_report_user_id ON Report_History(userId);
CREATE INDEX IF NOT EXISTS idx_report_timestamp ON Report_History(timestamp);
CREATE INDEX IF NOT EXISTS idx_report_type ON Report_History(reportType);
CREATE INDEX IF NOT EXISTS idx_report_status ON Report_History(status);
CREATE INDEX IF NOT EXISTS idx_report_created ON Report_History(createdDate);

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Show all tables created
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Show table row counts
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

SELECT 'Tables created successfully!' as status;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
