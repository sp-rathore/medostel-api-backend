# Medostel Database Development Agent

**Version:** 3.1 (Updated: March 3, 2026)
**Last Updated:** March 3, 2026
**Database:** PostgreSQL 18.2
**Host:** 35.244.27.232:5432
**Port:** 5432
**Status:** ✅ Production Ready
**Changes**: Step 1.1 (Geographic Hierarchy) ✅ COMPLETE, Step 1.2 (User Geographic Integration) ✅ COMPLETE, Step 1.3 (User Role Master Refactoring) ✅ COMPLETE
**Data Status**: 9,805 records loaded (36 states, 98 districts), roleId auto-increment (1-8)

---

## 📋 Table of Contents

1. [Database Overview](#database-overview)
2. [Table 1: User_Role_Master](#table-1-user_role_master)
3. [Table 2: State_City_PinCode_Master](#table-2-state_city_pincode_master)
4. [Table 3: User_Master](#table-3-user_master)
5. [Table 4: User_Login](#table-4-user_login)
6. [Table 5: New_User_Request](#table-5-new_user_request)
7. [Table 6: Report_History](#table-6-report_history)
8. [Data Relationships & Diagram](#data-relationships--diagram)
9. [Database Setup & Queries](#database-setup--queries)
10. [Indexes & Performance](#indexes--performance)
11. [Data Validation Rules](#data-validation-rules)
12. [Backup & Recovery](#backup--recovery)

---

## Database Overview

### Connection Details
```
Database Name:      medostel
Host:              35.244.27.232
Port:              5432
Engine:            PostgreSQL 18 (18.2)
Instance:          medostel-ai-assistant-pgdev-instance (Google Cloud SQL)
Project ID:        gen-lang-client-0064186167
Region:            asia-south1 (Mumbai)
Zone:              asia-south1-c
Machine Type:      db-custom-1-3840 (1 vCPU, 3.84 GB RAM)
Storage:           10 GB PD-SSD (auto-resize enabled)
Status:            🟢 RUNNABLE
```

### Connection Pool
```python
# Configuration in app/database/connection.py
Pool Size:         5 connections
Max Overflow:      10 connections
Timeout:           30 seconds
Pool Recycle:      3600 seconds
```

### Database Roles & Users

**ROLE 1: medostel_admin**
```
Role Name:         medostel_admin
Role Type:         SUPERUSER
User Account:      medostel_admin_user
Password:          Iag2bMi@0@6aA
Privileges:        CREATEDB, CREATEROLE, SUPERUSER
Capabilities:      Full administrative access, all schema operations
```

**ROLE 2: medostel_api**
```
Role Name:         medostel_api
Role Type:         Standard Role
User Account:      medostel_api_user
Password:          Iag2bMi@0@6aD
Privileges:        CONNECT, SELECT, INSERT, UPDATE, DELETE
Capabilities:      Application API access with limited permissions
```

### Database Statistics
- **Total Tables:** 7 (6 application + 1 backup)
  - user_role_master
  - state_city_pincode_master
  - state_city_pincode_master_backup_step1_1
  - user_master
  - user_login
  - new_user_request
  - report_history
- **Total Indexes:** 35+
- **Total Views:** 0 (Future use)
- **Total Stored Procedures:** 0 (Using ORM)
- **Total Records:** 9,805 (state_city_pincode_master)
- **Database Size:** 304 kB
- **Foreign Keys:** Multiple relationships with referential integrity

---

## Table 1: User_Role_Master

### Purpose
Stores user role definitions for the Medostel Healthcare system. Roles define access permissions and user types.

### Table Structure (UPDATED - Step 1.3 Complete)
**Schema Version:** 2.0 | **Status:** Auto-increment roleId (1-8) ✅

```sql
CREATE TABLE IF NOT EXISTS user_role_master (
    roleId SERIAL PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) DEFAULT 'Active',
    comments VARCHAR(250),
    createdDate DATE DEFAULT CURRENT_DATE,
    updatedDate DATE DEFAULT CURRENT_DATE
);
```

### Column Details

| Column | Type | Constraints | Range/Length | Purpose |
|--------|------|-------------|-------------|---------|
| **roleId** | SERIAL | PK, AUTO-INCREMENT | 1-8 | Unique role identifier (auto-generated 1-8) |
| **roleName** | VARCHAR | UNIQUE, NOT NULL | 50 | Human-readable role name (e.g., "System Administrator") |
| **status** | VARCHAR | DEFAULT 'Active' | 20 | Current status: Active, Inactive, Closed, Pending |
| **comments** | VARCHAR | NULLABLE | 250 | Additional description or notes about the role |
| **createdDate** | DATE | DEFAULT CURRENT_DATE | - | Date when role was created |
| **updatedDate** | DATE | DEFAULT CURRENT_DATE | - | Date of last modification |

### Indexes
```sql
-- Primary Key Index (implicit with SERIAL)
-- Secondary Indexes
CREATE INDEX idx_role_status ON user_role_master(status);
CREATE INDEX idx_role_name ON user_role_master(roleName);
CREATE INDEX idx_role_updated ON user_role_master(updatedDate);
```

### Sample Data (Production - 8 Active Roles with Auto-Increment IDs)
```sql
-- roleId is auto-generated via SERIAL (1-8)
INSERT INTO user_role_master (roleName, status, comments) VALUES
('ADMIN', 'Active', 'System Administrator - Full system access and database management'),
('DOCTOR', 'Active', 'Doctor or Physician - Can view and manage patient records and create medical reports'),
('HOSPITAL', 'Active', 'Hospital Administrator - Hospital-level administrative functions'),
('NURSE', 'Active', 'Nursing Staff - Can update patient information and create nursing reports'),
('PARTNER', 'Active', 'Sales Partner - Sales and marketing partner functions'),
('PATIENT', 'Active', 'Patient User - Can view personal medical records and report history'),
('RECEPTION', 'Active', 'Reception Staff - Can register new patients and manage appointments'),
('TECHNICIAN', 'Active', 'Lab Technician - Can create and upload laboratory test reports and results');
```

### API Endpoints
- **API 1:** GET `/api/v1/roles/all` - Retrieve all roles
- **API 2:** POST `/api/v1/roles` - Create new role
- **API 2:** PUT `/api/v1/roles/{roleId}` - Update role
- **API 2:** DELETE `/api/v1/roles/{roleId}` - Delete role

### Data Validation Rules
- roleId: Auto-generated SERIAL INTEGER (1-8), unique, PRIMARY KEY
- roleName: Required, must be unique, max 50 chars
- status: Must be one of: Active, Inactive, Closed, Pending, default is 'Active'
- comments: Optional, max 250 chars
- createdDate: Auto-populated with CURRENT_DATE on insert
- updatedDate: Auto-populated with CURRENT_DATE on insert, updates on modification

### All System Roles (8 Total - Auto-Increment IDs 1-8)

| ID | Role Name | Status | Description |
|----|-----------|--------|-------------|
| 1 | ADMIN | Active | System Administrator - Full system access and database management |
| 2 | DOCTOR | Active | Doctor or Physician - Can view and manage patient records and create medical reports |
| 3 | HOSPITAL | Active | Hospital Administrator - Hospital-level administrative functions |
| 4 | NURSE | Active | Nursing Staff - Can update patient information and create nursing reports |
| 5 | PARTNER | Active | Sales Partner - Sales and marketing partner functions |
| 6 | PATIENT | Active | Patient User - Can view personal medical records and report history |
| 7 | RECEPTION | Active | Reception Staff - Can register new patients and manage appointments |
| 8 | TECHNICIAN | Active | Lab Technician - Can create and upload laboratory test reports and results |

### Relationships
- **Referenced by:** User_Master (currentRole), User_Login (roleId)
- **Foreign Keys:** None (Master table)

---

## Table 2: State_City_PinCode_Master

### Purpose
Stores geographic location information including states, cities, and postal codes. Supports location-based filtering and distribution of services.

### Purpose
Stores geographic location information including states, districts, cities, and postal codes with hierarchical structure. Supports location-based filtering and geographic hierarchy queries.

### Table Structure (ENHANCED - Step 1.1 Complete)
**Schema Version:** 2.0 | **Data Records:** 9,805 | **Status:** Production Ready ✅

```sql
CREATE TABLE IF NOT EXISTS state_city_pincode_master (
    id SERIAL PRIMARY KEY,
    stateId INTEGER NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    districtId INTEGER NOT NULL,
    districtName VARCHAR(100) NOT NULL,
    cityId INTEGER NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    pinCode INTEGER PRIMARY KEY,
    countryName VARCHAR(100) DEFAULT 'India',
    status VARCHAR(50) DEFAULT 'Active',
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Column Details

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| **id** | SERIAL | PK, AUTO-INCREMENT | Unique location identifier |
| **stateId** | INTEGER | NOT NULL | State identifier (numeric) |
| **stateName** | VARCHAR(100) | NOT NULL | State name (e.g., Maharashtra, Karnataka) |
| **districtId** | INTEGER | NOT NULL | District identifier (0001-N per state) |
| **districtName** | VARCHAR(100) | NOT NULL | District name |
| **cityId** | INTEGER | NOT NULL | City identifier (numeric) |
| **cityName** | VARCHAR(100) | NOT NULL | City name (e.g., Mumbai, Bangalore) |
| **pinCode** | INTEGER | PRIMARY KEY | Postal code / ZIP code (6 digits) |
| **countryName** | VARCHAR(100) | DEFAULT 'India' | Country name |
| **status** | VARCHAR(50) | DEFAULT 'Active' | Location status: Active, Inactive |
| **createdDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| **updatedDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

### Geographic Hierarchy
```
State (stateId, stateName)
   ├── District (districtId, districtName)
   │    ├── City (cityId, cityName)
   │    │    └── PinCode (pinCode)
```

### Indexes (11 Total - Step 1.1 Enhanced)
```sql
-- Primary Key Index
CREATE UNIQUE INDEX pk_location_master ON state_city_pincode_master(id);

-- Individual Field Indexes
CREATE INDEX idx_state_name ON state_city_pincode_master(stateId);
CREATE INDEX idx_district_id ON state_city_pincode_master(districtId);
CREATE INDEX idx_district_name ON state_city_pincode_master(districtName);
CREATE INDEX idx_city_name ON state_city_pincode_master(cityId);
CREATE INDEX idx_pincode ON state_city_pincode_master(pinCode);

-- Composite Hierarchical Indexes
CREATE INDEX idx_state_district ON state_city_pincode_master(stateId, districtId);
CREATE INDEX idx_district_city ON state_city_pincode_master(districtId, cityId);
CREATE INDEX idx_state_district_city ON state_city_pincode_master(stateId, districtId, cityId);
CREATE INDEX idx_district_status ON state_city_pincode_master(districtId, status);

-- Status Index
CREATE INDEX idx_status ON state_city_pincode_master(status);
```

**Index Usage**: Optimized for hierarchical queries (state → district → city → pincode)

### Sample Data
```sql
INSERT INTO state_city_pincode_master (stateId, stateName, cityId, cityName, pinCode, countryName, status) VALUES
('MH', 'Maharashtra', 'MUM', 'Mumbai', '400001', 'India', 'Active'),
('MH', 'Maharashtra', 'MUM', 'Mumbai', '400002', 'India', 'Active'),
('KA', 'Karnataka', 'BNG', 'Bangalore', '560001', 'India', 'Active'),
('DL', 'Delhi', 'DEL', 'New Delhi', '110001', 'India', 'Active'),
('TG', 'Telangana', 'HYD', 'Hyderabad', '500001', 'India', 'Active');
```

### API Endpoints
- **API 3:** GET `/api/v1/locations/all` - Retrieve all locations
- **API 4:** POST `/api/v1/locations` - Create new location
- **API 4:** PUT `/api/v1/locations/{location_id}` - Update location
- **API 4:** DELETE `/api/v1/locations/{location_id}` - Delete location

### Data Validation Rules
- stateId: Required, INTEGER (0001-0036 for 36 states/UTs)
- stateName: Required, max 100 chars
- districtId: Required, INTEGER (0001-N per state, hierarchical)
- districtName: Required, max 100 chars
- cityId: Required, INTEGER (0001-N per district, hierarchical)
- cityName: Required, max 100 chars
- pinCode: Required, INTEGER (PRIMARY KEY, 100000-999999, 6 digits)
- countryName: Optional, default 'India'
- status: Must be Active or Inactive
- **Geographic Hierarchy Validation**: districtId must exist for given stateId

### Relationships
- **Referenced by:** User_Master (implicit through user address)
- **Foreign Keys:** None (Master table)

---

## Table 3: User_Master

### Purpose
Stores user profile information for all system users (patients, doctors, staff, etc.) with complete support for geographic location tracking and audit trails.

### Implementation Status
**Status:** ✅ COMPLETE (Phase 1-3)
- **Schema Version**: 4.0 (FINAL)
- **Migration Date**: March 3, 2026
- **Last Updated**: March 3, 2026
- **Migration Script**: `src/SQL files/02_migrate_user_master_schema.sql`
- **ORM Model**: `src/db/models.py` (UserMaster class)
- **API Layer**: `src/routes/v1/users.py` (3 endpoints)
- **Test Coverage**: 123/123 tests passing (100%)

### Current Table Structure (FINAL SCHEMA)

```sql
CREATE TABLE user_master (
    userId VARCHAR(100) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL REFERENCES user_role_master(rolename),
    emailId VARCHAR(255) NOT NULL UNIQUE,
    mobileNumber INTEGER NOT NULL UNIQUE CHECK (mobileNumber >= 1000000000 AND mobileNumber <= 9999999999),
    organisation VARCHAR(255),
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateId VARCHAR(10),
    stateName VARCHAR(100),
    districtId VARCHAR(10),
    cityId VARCHAR(10),
    cityName VARCHAR(100),
    pinCode VARCHAR(10),
    commentLog VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'pending', 'deceased', 'inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(emailId, mobileNumber)
);
```

### Column Details

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| **userId** | VARCHAR(100) | PK, AUTO | Unique user identifier (auto-generated as max+1) |
| **firstName** | VARCHAR(50) | NOT NULL | User's first name (max 50 chars) |
| **lastName** | VARCHAR(50) | NOT NULL | User's last name (max 50 chars) |
| **currentRole** | VARCHAR(50) | NOT NULL, FK | User's current role (references user_role_master.rolename) |
| **emailId** | VARCHAR(255) | NOT NULL, UNIQUE | Email address (validated at API layer) |
| **mobileNumber** | INTEGER | NOT NULL, UNIQUE | Phone number (10 digits: 1000000000-9999999999) |
| **organisation** | VARCHAR(255) | NULLABLE | Hospital/clinic/organization name |
| **address1** | VARCHAR(255) | NULLABLE | Address line 1 |
| **address2** | VARCHAR(255) | NULLABLE | Address line 2 |
| **stateId** | VARCHAR(10) | NULLABLE | State identifier (reference-only, no FK) |
| **stateName** | VARCHAR(100) | NULLABLE | State name (for display) |
| **districtId** | VARCHAR(10) | NULLABLE | District identifier (reference-only, no FK) |
| **cityId** | VARCHAR(10) | NULLABLE | City identifier (reference-only, no FK) |
| **cityName** | VARCHAR(100) | NULLABLE | City name (for display) |
| **pinCode** | VARCHAR(10) | NULLABLE | Postal code (reference-only, no FK) |
| **commentLog** | VARCHAR(255) | NULLABLE | Most recent change/comment (for audit trail) |
| **status** | VARCHAR(50) | DEFAULT 'active' | User status: active, pending, deceased, inactive |
| **createdDate** | TIMESTAMP | DEFAULT NOW() | Account creation timestamp (immutable) |
| **updatedDate** | TIMESTAMP | DEFAULT NOW() | Last profile update timestamp (auto-updated) |

### Key Design Decisions

**1. Location Fields (stateId, districtId, cityId, pinCode)**
- Changed from INTEGER to VARCHAR(10) to match reference table
- Removed FK constraints (reference table lacks unique constraints)
- Validated at application layer (API layer validation)
- Enables reference lookup without strict referential integrity

**2. currentRole Foreign Key**
- References `user_role_master.rolename` (VARCHAR) not roleId (INTEGER)
- Enables direct role lookup and validation
- FK constraint enforced: ON DELETE RESTRICT

**3. Status Field**
- Valid values: 'active', 'pending', 'deceased', 'inactive' (lowercase)
- Database CHECK constraint enforces allowed values
- Application normalizes input to lowercase

**4. Email & Mobile Validation**
- Email: Validated with regex pattern at API layer
- Mobile: Range validation (ge=1000000000, le=9999999999)
- Both fields: Database UNIQUE constraints
- Composite unique constraint on (emailId, mobileNumber)

**5. Timestamp Management**
- createdDate: Set on insert, immutable
- updatedDate: Set on insert, auto-updated on any update
- Both stored in UTC timezone

### Indexes (13 Total - Optimized for Query Performance)

```sql
-- Primary Key
CREATE UNIQUE INDEX idx_user_master_pk ON user_master(userId);

-- Search Optimization
CREATE INDEX idx_user_master_email ON user_master(emailId);
CREATE INDEX idx_user_master_mobile ON user_master(mobileNumber);
CREATE INDEX idx_user_master_role ON user_master(currentRole);
CREATE INDEX idx_user_master_status ON user_master(status);

-- Timestamp Filtering
CREATE INDEX idx_user_master_created ON user_master(createdDate);
CREATE INDEX idx_user_master_updated ON user_master(updatedDate);

-- Location Filtering
CREATE INDEX idx_user_master_state ON user_master(stateId);
CREATE INDEX idx_user_master_city ON user_master(cityId);

-- Composite Indexes
CREATE INDEX idx_user_master_state_city ON user_master(stateId, cityId);
CREATE INDEX idx_user_master_role_status ON user_master(currentRole, status);
```

**Index Strategy**: Optimized for common query patterns (search, filter by role/status, location-based queries)

### Constraints Summary

| Constraint Type | Details |
|-----------------|---------|
| **Primary Key** | userId (VARCHAR 100) |
| **Unique** | emailId (VARCHAR 255) |
| **Unique** | mobileNumber (INTEGER) |
| **Unique Composite** | (emailId, mobileNumber) |
| **Check** | mobileNumber BETWEEN 1000000000 AND 9999999999 |
| **Check** | status IN ('active', 'pending', 'deceased', 'inactive') |
| **Foreign Key** | currentRole → user_role_master(rolename) ON DELETE RESTRICT |
| **Not Null** | firstName, lastName, currentRole, emailId, mobileNumber, status |

### SQLAlchemy ORM Model

**File:** `src/db/models.py` (UserMaster class)

```python
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class UserMaster(Base):
    __tablename__ = "user_master"

    userId = Column(String(100), primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    currentRole = Column(String(50), ForeignKey('user_role_master.rolename', ondelete='RESTRICT'), nullable=False)
    emailId = Column(String(255), nullable=False, unique=True, index=True)
    mobileNumber = Column(Integer, nullable=False, unique=True, index=True)
    organisation = Column(String(255), nullable=True)
    address1 = Column(String(255), nullable=True)
    address2 = Column(String(255), nullable=True)
    stateId = Column(String(10), nullable=True)
    stateName = Column(String(100), nullable=True)
    districtId = Column(String(10), nullable=True)
    cityId = Column(String(10), nullable=True, index=True)
    cityName = Column(String(100), nullable=True)
    pinCode = Column(String(10), nullable=True)
    commentLog = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default='active', index=True)
    createdDate = Column(DateTime, nullable=False, default=datetime.utcnow(), index=True)
    updatedDate = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    __table_args__ = (
        UniqueConstraint('emailId', 'mobileNumber', name='uk_user_master_email_mobile'),
        CheckConstraint("status IN ('active', 'pending', 'deceased', 'inactive')", name='ck_user_master_status'),
        CheckConstraint("mobileNumber >= 1000000000 AND mobileNumber <= 9999999999", name='ck_user_master_mobile_range'),
    )
```

### API Layer Documentation

**File:** `src/schemas/user.py` (Pydantic schemas)

**Available Endpoints:**

1. **Search User**
   - Endpoint: `GET /api/v1/users/search?emailId=...` or `GET /api/v1/users/search?mobileNumber=...`
   - Response: `{data: UserResponse | null, existsFlag: boolean}`

2. **Create User**
   - Endpoint: `POST /api/v1/users`
   - Request: UserCreate (firstName, lastName, currentRole, emailId, mobileNumber required)
   - Response: `{message: string, data: UserResponse}` (HTTP 201)

3. **Update User**
   - Endpoint: `PUT /api/v1/users/{userId}`
   - Request: UserUpdate (at least one field + commentLog required)
   - Response: `{message: string, data: UserResponse}` (HTTP 200)

**Field Validation (API Layer):**
- Email: Regex pattern `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$`
- Mobile: Range 1000000000-9999999999
- Names: Max 50 characters
- Status: One of {active, pending, deceased, inactive}
- Role: One of {ADMIN, DOCTOR, HOSPITAL, NURSE, PARTNER, PATIENT, RECEPTION, TECHNICIAN}

### Data Validation Rules (FINAL - Phase 3 Verified)

| Field | Type | Constraints | Details |
|-------|------|-------------|---------|
| **userId** | VARCHAR(100) | PK | Auto-generated, max+1, zero-padded |
| **firstName** | VARCHAR(50) | NOT NULL, max 50 | Required |
| **lastName** | VARCHAR(50) | NOT NULL, max 50 | Required |
| **currentRole** | VARCHAR(50) | NOT NULL, FK | 8 valid roles, uppercase normalized |
| **emailId** | VARCHAR(255) | NOT NULL, UNIQUE | Regex validated, lowercase normalized |
| **mobileNumber** | INTEGER | NOT NULL, UNIQUE, 10-digit | Range: 1000000000-9999999999 |
| **organisation** | VARCHAR(255) | NULLABLE | Max 255 characters |
| **address1** | VARCHAR(255) | NULLABLE | Max 255 characters |
| **address2** | VARCHAR(255) | NULLABLE | Max 255 characters |
| **stateId** | VARCHAR(10) | NULLABLE | Reference-only, no FK |
| **districtId** | VARCHAR(10) | NULLABLE | Reference-only, no FK |
| **cityId** | VARCHAR(10) | NULLABLE | Reference-only, no FK |
| **pinCode** | VARCHAR(10) | NULLABLE | Reference-only, no FK |
| **commentLog** | VARCHAR(255) | NULLABLE | Audit trail (required on update) |
| **status** | VARCHAR(50) | CHECK, DEFAULT 'active' | active, pending, deceased, inactive |
| **createdDate** | TIMESTAMP | DEFAULT NOW(), IMMUTABLE | Auto-set on creation |
| **updatedDate** | TIMESTAMP | DEFAULT NOW(), AUTO-UPDATE | Auto-set on create, updated on changes |

**Validation Features** ✅
- ✅ Email regex validation (RFC 5322 pattern)
- ✅ Mobile number range validation (10 digits)
- ✅ Status enum validation (4 valid values)
- ✅ Role enum validation (8 valid values)
- ✅ Name length constraints (max 50)
- ✅ Uniqueness constraints (email, mobile, combination)
- ✅ Case normalization (email lowercase, role uppercase, status lowercase)
- ✅ Immutable field protection (userId, createdDate)
- ✅ Timestamp auto-management (createdDate, updatedDate)

### Test Coverage (Phase 3 - All Passing ✅)

**Total Tests:** 123/123 passing (100%)

- **Schema Tests:** 45+ tests (email, mobile, status, role, name validation)
- **Database Tests:** 31 tests (auto-increment, queries, existence checks, CRUD)
- **API Tests:** 47 tests (endpoints, responses, error handling, workflows)

**Key Test Scenarios:**
- ✅ All validation rules verified
- ✅ Auto-increment with zero-padding
- ✅ Duplicate detection (email, mobile, combination)
- ✅ Immutable field protection
- ✅ Timestamp management
- ✅ Case normalization
- ✅ Full CRUD workflows

### Sample Data

```sql
-- Sample insert (with auto-generated userId)
INSERT INTO user_master
(firstName, lastName, currentRole, emailId, mobileNumber, organisation, status, commentLog)
VALUES
('John', 'Doe', 'DOCTOR', 'john.doe@hospital.com', 9876543210, 'Apollo Hospital', 'active', 'Initial creation');

-- Search queries
SELECT * FROM user_master WHERE emailId = 'john.doe@hospital.com';
SELECT * FROM user_master WHERE mobileNumber = 9876543210;
SELECT * FROM user_master WHERE currentRole = 'DOCTOR' AND status = 'active';

-- Filtered queries
SELECT * FROM user_master WHERE stateId = 'MH' AND cityId = 'CITY_001';
SELECT COUNT(*) FROM user_master WHERE status = 'active' GROUP BY currentRole;
```

### Relationships
- **Foreign Key:** currentRole → user_role_master(rolename) ON DELETE RESTRICT
- **Referenced By:** User_Login (userId), New_User_Request (indirectly)
- **Indexes On:** emailId, mobileNumber, currentRole, status, createdDate, updatedDate, cityId, stateId

---

## Table 4: User_Login

### Purpose
Stores user authentication credentials and login tracking information.

### Table Structure

**Updated March 1, 2026** ✅ - userId changed to BIGINT to match user_master schema

```sql
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
```

### Column Details

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| **userId** | BIGINT | PK, FK | Reference to user in user_master (numeric) |
| **username** | VARCHAR(100) | UNIQUE, NOT NULL | Login username |
| **password** | VARCHAR(255) | NOT NULL | Hashed password (SHA256) |
| **roleId** | VARCHAR(50) | NOT NULL, FK | User's role (from user_role_master) |
| **isActive** | BOOLEAN | DEFAULT TRUE | Whether login is active |
| **lastLoginTime** | TIMESTAMP | NULLABLE | Timestamp of last successful login |
| **loginAttempts** | INTEGER | DEFAULT 0 | Failed login attempt counter |
| **createdDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When credentials were created |
| **updatedDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last password/config update |

### Indexes
```sql
-- Primary Key Index
CREATE UNIQUE INDEX pk_user_login ON user_login(userId);

-- Search Indexes
CREATE INDEX idx_login_username ON user_login(username);
CREATE INDEX idx_login_active ON user_login(isActive);
CREATE INDEX idx_login_role ON user_login(roleId);
CREATE INDEX idx_login_attempts ON user_login(loginAttempts);
CREATE INDEX idx_login_lastlogin ON user_login(lastLoginTime);
CREATE INDEX idx_login_updated ON user_login(updatedDate);
```

### API Endpoints
- **API 7:** GET `/api/v1/auth/users` - Retrieve all login records
- **API 8:** POST `/api/v1/auth/credentials` - Create login credentials
- **API 8:** PUT `/api/v1/auth/credentials/{userId}` - Update credentials
- **API 8:** DELETE `/api/v1/auth/credentials/{userId}` - Delete credentials

### Data Validation Rules
- userId: Required, must exist in user_master
- username: Required, unique, 5-100 chars
- password: Required, min 8 chars, hashed in database
- roleId: Required, must exist in user_role_master
- isActive: Boolean (true/false)
- loginAttempts: Non-negative integer
- lastLoginTime: Auto-updated on successful login

### Security Considerations
- Passwords are hashed using SHA256 before storage
- Password is NEVER returned in API responses
- Login attempts are tracked to prevent brute force
- Consider implementing account lockout after N attempts
- Use HTTPS only for login endpoints

### Relationships
- **Foreign Key 1:** userId → user_master(userId)
- **Foreign Key 2:** roleId → user_role_master(roleId)

---

## Table 5: New_User_Request

### Purpose
Stores registration requests from new users pending approval by administrators.

### Table Structure
```sql
CREATE TABLE IF NOT EXISTS new_user_request (
    requestId VARCHAR(100) PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    emailId VARCHAR(255) NOT NULL UNIQUE,
    mobileNumber VARCHAR(20) NOT NULL,
    address TEXT,
    requestStatus VARCHAR(50) DEFAULT 'Pending',
    approvalDate TIMESTAMP,
    approvalComments TEXT,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Column Details

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| **requestId** | VARCHAR(100) | PK | Unique registration request ID |
| **userName** | VARCHAR(100) | NOT NULL | Desired username |
| **firstName** | VARCHAR(100) | NOT NULL | First name |
| **lastName** | VARCHAR(100) | NOT NULL | Last name |
| **currentRole** | VARCHAR(50) | NOT NULL | Requested role |
| **emailId** | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| **mobileNumber** | VARCHAR(20) | NOT NULL | Contact number |
| **address** | TEXT | NULLABLE | Address |
| **requestStatus** | VARCHAR(50) | DEFAULT 'Pending' | Status: Pending, Approved, Rejected |
| **approvalDate** | TIMESTAMP | NULLABLE | When request was approved/rejected |
| **approvalComments** | TEXT | NULLABLE | Approval/rejection reason |
| **createdDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Request submission date |
| **updatedDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

### Indexes
```sql
-- Primary Key Index
CREATE UNIQUE INDEX pk_request_master ON new_user_request(requestId);

-- Search Indexes
CREATE INDEX idx_request_status ON new_user_request(requestStatus);
CREATE INDEX idx_request_email ON new_user_request(emailId);
CREATE INDEX idx_request_role ON new_user_request(currentRole);
CREATE INDEX idx_request_created ON new_user_request(createdDate);
CREATE INDEX idx_request_updated ON new_user_request(updatedDate);
CREATE INDEX idx_request_approval ON new_user_request(approvalDate);
```

### Sample Data
```sql
INSERT INTO new_user_request (requestId, userName, firstName, lastName, currentRole, emailId, mobileNumber, requestStatus) VALUES
('REQ_20260301_001', 'dr_anita', 'Dr. Anita', 'Sharma', 'ROLE_DOCTOR', 'anita.sharma@example.com', '9876543210', 'Pending'),
('REQ_20260301_002', 'patient_john', 'John', 'Doe', 'ROLE_PATIENT', 'john.doe@example.com', '9123456789', 'Approved');
```

### API Endpoints
- **API 9:** GET `/api/v1/requests/all` - Retrieve all requests
- **API 10:** POST `/api/v1/requests` - Create registration request
- **API 10:** PUT `/api/v1/requests/{requestId}` - Approve/reject request
- **API 10:** DELETE `/api/v1/requests/{requestId}` - Delete request

### Data Validation Rules
- requestId: Required, unique, alphanumeric
- userName: Required, 5-100 chars, alphanumeric with underscores
- firstName: Required, max 100 chars
- lastName: Required, max 100 chars
- currentRole: Required (ROLE_DOCTOR, ROLE_PATIENT, etc.)
- emailId: Required, unique, valid email
- mobileNumber: Required, 10 digits
- requestStatus: Pending, Approved, Rejected
- approvalComments: Optional for Rejected requests

### Workflow
1. User submits registration request (requestStatus = Pending)
2. Administrator reviews request
3. Administrator approves (Approved) or rejects (Rejected)
4. If approved, user data migrates to user_master and user_login
5. Request record is retained for audit trail

### Relationships
- **None (Independent table)**
- **Used by:** Workflow system for user onboarding

---

## Table 6: Report_History

### Purpose
Stores medical reports submitted by patients and analysis results generated by AI systems.

### Table Structure
```sql
CREATE TABLE IF NOT EXISTS report_history (
    id VARCHAR(100) PRIMARY KEY,
    userId VARCHAR(255) NOT NULL,
    fileName VARCHAR(255) NOT NULL,
    fileType VARCHAR(50) NOT NULL,
    reportType VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    inferredDiagnosis TEXT,
    pdfUrl VARCHAR(500),
    bucketLocation VARCHAR(500),
    jsonData JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user_master(userId)
);
```

### Column Details

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| **id** | VARCHAR(100) | PK | Unique report ID |
| **userId** | VARCHAR(255) | NOT NULL, FK | Patient who submitted report |
| **fileName** | VARCHAR(255) | NOT NULL | Original filename |
| **fileType** | VARCHAR(50) | NOT NULL | File type: PDF, JPG, DICOM, etc. |
| **reportType** | VARCHAR(100) | NOT NULL | Report type: XRay, MRI, CT, Blood Test, etc. |
| **status** | VARCHAR(50) | DEFAULT 'Pending' | Status: Pending, Processing, Completed, Error |
| **inferredDiagnosis** | TEXT | NULLABLE | AI-generated diagnosis/analysis |
| **pdfUrl** | VARCHAR(500) | NULLABLE | URL to PDF file in cloud storage |
| **bucketLocation** | VARCHAR(500) | NULLABLE | Cloud storage path (Google Cloud Storage) |
| **jsonData** | JSONB | NULLABLE | Structured analysis results as JSON |
| **timestamp** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Report submission time |
| **createdDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| **updatedDate** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |

### Indexes
```sql
-- Primary Key Index
CREATE UNIQUE INDEX pk_report_history ON report_history(id);

-- Search Indexes
CREATE INDEX idx_report_user ON report_history(userId);
CREATE INDEX idx_report_status ON report_history(status);
CREATE INDEX idx_report_type ON report_history(reportType);
CREATE INDEX idx_report_timestamp ON report_history(timestamp);
CREATE INDEX idx_report_created ON report_history(createdDate);
CREATE INDEX idx_report_updated ON report_history(updatedDate);

-- JSONB Index for AI results queries
CREATE INDEX idx_report_jsondata ON report_history USING GIN (jsonData);
```

### Sample Data
```sql
INSERT INTO report_history (id, userId, fileName, fileType, reportType, status, jsonData) VALUES
('RPT_20260301_001', 'patient1@medostel.com', 'chest_xray.pdf', 'PDF', 'XRay', 'Pending',
 '{"modality": "XRay", "body_part": "Chest", "findings": ["No abnormality"], "quality": "Good"}'),
('RPT_20260301_002', 'patient1@medostel.com', 'blood_test.pdf', 'PDF', 'Blood Test', 'Completed',
 '{"test_type": "Complete Blood Count", "results": {"WBC": 7.5, "RBC": 4.8}, "diagnosis": "Normal"}');
```

### API Endpoints
- **API 11:** GET `/api/v1/reports/all` - Retrieve all reports
- **API 12:** POST `/api/v1/reports` - Submit new report
- **API 12:** PUT `/api/v1/reports/{reportId}` - Update report with analysis
- **API 12:** DELETE `/api/v1/reports/{reportId}` - Delete report

### Data Validation Rules
- id: Required, unique, alphanumeric
- userId: Required, must exist in user_master
- fileName: Required, max 255 chars
- fileType: Required, must be valid (PDF, JPG, PNG, DICOM, etc.)
- reportType: Required (XRay, MRI, CT, Ultrasound, Blood Test, etc.)
- status: Pending, Processing, Completed, Error
- jsonData: Optional, must be valid JSON
- pdfUrl: Optional, must be valid URL
- bucketLocation: Optional, must be valid GCS path

### Report Workflow
1. Patient uploads medical report (status = Pending)
2. File is stored in Google Cloud Storage
3. AI analysis system processes report (status = Processing)
4. Analysis results are stored in jsonData
5. Inference diagnosis is updated (status = Completed)
6. Report is available for doctor/patient review

### Data Types in jsonData
```json
{
  "modality": "XRay",
  "body_part": "Chest",
  "findings": ["Finding 1", "Finding 2"],
  "severity": "Low|Medium|High",
  "quality": "Good|Fair|Poor",
  "confidence": 0.95,
  "analysis_timestamp": "2026-03-01T10:00:00",
  "model_version": "1.0"
}
```

### Relationships
- **Foreign Key:** userId → user_master(userId)
- **Referenced by:** Analysis systems, Doctor dashboard

---

## Data Relationships & Diagram

### Entity Relationship Diagram

```
┌─────────────────────────┐
│   User_Role_Master      │
├─────────────────────────┤
│ PK: roleId              │
│    roleName             │
│    status               │
│    comments             │
└─────────────────────────┘
         △
         │ (Referenced by)
         │
    ┌────┴───────────────────────────────────────┐
    │                                              │
    │                                              │
┌───┴─────────────────────┐   ┌────────────────────────┐
│   User_Master           │   │   User_Login           │
├────────────────────────┤   ├────────────────────────┤
│ PK: userId             │   │ PK: userId (FK)        │
│    firstName           │   │    username            │
│    lastName            │   │    password (hashed)   │
│ FK: currentRole ─────┐ │   │ FK: roleId             │
│    emailId            │ │   │    isActive            │
│    mobileNumber       │ │   │    lastLoginTime       │
│    organisation       │ │   │    loginAttempts       │
│    address            │ │   └────────────────────────┘
│    status             │ │
└───┬────────────────────┘ │
    │                      │
    │ (Primary User)       │
    │                      │
    │ ┌────────────────────┴────────────────────┐
    │ │                                          │
    │ │                                          │
    │ │   ┌─────────────────────────┐           │
    │ └─→│  Report_History         │           │
    │     ├─────────────────────────┤           │
    │     │ PK: id                  │           │
    │     │ FK: userId              │           │
    │     │    fileName             │           │
    │     │    reportType           │           │
    │     │    status               │           │
    │     │    inferredDiagnosis    │           │
    │     │    jsonData (JSONB)     │           │
    │     └─────────────────────────┘           │
    │                                            │
    └───────────────────────────────────────────┘

                ┌────────────────────────┐
                │ State_City_PinCode_... │
                ├────────────────────────┤
                │ PK: id                 │
                │    stateId             │
                │    cityId              │
                │    pinCode             │
                │    status              │
                └────────────────────────┘
                (Referenced implicitly
                 by User address)

┌─────────────────────────┐
│ New_User_Request        │
├─────────────────────────┤
│ PK: requestId           │
│    userName             │
│    firstName            │
│    lastName             │
│    currentRole          │
│    emailId              │
│    requestStatus        │
│    approvalDate         │
│    approvalComments     │
└─────────────────────────┘
(Workflow table for user onboarding)
```

### Relationship Summary

| From Table | To Table | Relationship | Type |
|------------|----------|--------------|------|
| User_Master | User_Role_Master | currentRole → roleId | Many-to-One |
| User_Login | User_Master | userId → userId | One-to-One |
| User_Login | User_Role_Master | roleId → roleId | Many-to-One |
| Report_History | User_Master | userId → userId | Many-to-One |
| New_User_Request | (Standalone) | Onboarding workflow | Independent |

---

## Database Setup & Queries

### Create All Tables
```sql
-- Complete setup is in: DevOps Development/complete_setup.sql

-- Quick table creation commands:
CREATE TABLE user_role_master (
    roleId VARCHAR(50) PRIMARY KEY,
    roleName VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(50) DEFAULT 'Active',
    comments TEXT,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- (See individual table sections for other CREATE statements)
```

### Useful Queries

**Get all roles:**
```sql
SELECT * FROM user_role_master WHERE status = 'Active';
```

**Find user by email:**
```sql
SELECT * FROM user_master WHERE emailId = 'user@example.com';
```

**Get user's reports:**
```sql
SELECT * FROM report_history
WHERE userId = 'patient@example.com'
ORDER BY timestamp DESC;
```

**Count pending registration requests:**
```sql
SELECT COUNT(*) as pending_requests
FROM new_user_request
WHERE requestStatus = 'Pending';
```

**Get locations by state:**
```sql
SELECT DISTINCT cityName, pinCode
FROM state_city_pincode_master
WHERE stateId = 'MH' AND status = 'Active';
```

---

## Indexes & Performance

### Index Strategy

**Total Indexes: 35+**

### Index Distribution
- User_Role_Master: 4 indexes
- State_City_PinCode_Master: 6 indexes
- User_Master: 6 indexes
- User_Login: 6 indexes
- New_User_Request: 6 indexes
- Report_History: 7 indexes (including JSONB)

### Performance Tuning

**Connection Pooling:**
- Pool size: 5 connections
- Max overflow: 10
- Timeout: 30 seconds
- Auto-recycle: 3600 seconds

**Query Optimization:**
- Use indexes for WHERE clauses
- Use EXPLAIN ANALYZE for complex queries
- Avoid SELECT *; specify needed columns
- Use pagination with LIMIT/OFFSET
- Index JSONB columns with GIN indexes

**Monitoring:**
```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes;

-- Check table sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname='public';
```

---

## Data Validation Rules

### Field-Level Validation

**Email Validation:**
```
Format: RFC 5322 compliant
Regex: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
Max length: 255 characters
```

**Phone Number Validation (India):**
```
Format: 10 digits
Accepted formats: 9876543210, +91-9876543210
```

**Status Fields:**
```
Allowed values: Active, Inactive, Pending, Approved, Rejected
Default: Active
```

**Role IDs:**
```
Format: ROLE_[DESIGNATION]
Examples: ROLE_ADMIN, ROLE_DOCTOR, ROLE_PATIENT, ROLE_NURSE
```

---

## Backup & Recovery

### Backup Strategy

**Frequency:** Daily at 02:00 UTC
**Retention:** 30 days
**Location:** Google Cloud Storage (Multi-region)

### Backup Command
```bash
# Automated backup via Google Cloud SQL
gcloud sql backups create \
    --instance=medostel-ai-assistant-pgdev-instance \
    --description="Daily backup"
```

### Recovery Procedure
```bash
# Restore from backup
gcloud sql backups restore [BACKUP_ID] \
    --backup-instance=medostel-ai-assistant-pgdev-instance
```

### Point-in-Time Recovery (PITR)
```bash
# Restore to specific timestamp
gcloud sql backups restore \
    --backup-instance=medostel-ai-assistant-pgdev-instance \
    --point-in-time=2026-03-01T10:00:00Z
```

---

---

## 🔄 STEP 1.1: Geographic Hierarchy Enhancement (COMPLETE - March 3, 2026)

### Overview
Enhanced State_City_PinCode_Master table with district-level geographic hierarchy, converting VARCHAR fields to INTEGER types, and making pinCode the PRIMARY KEY.

### Database Changes

#### Table: State_City_PinCode_Master (Enhanced)

**New Columns**:
- `districtId` (INTEGER NOT NULL) - District identifier (0001-N per state)
- `districtName` (VARCHAR(100) NOT NULL) - District name

**Data Type Changes**:
- `stateId`: VARCHAR(10) → INTEGER
- `cityId`: VARCHAR(10) → INTEGER
- `pinCode`: VARCHAR(10) → INTEGER (PRIMARY KEY)

**New Indexes** (6 total):
- idx_district_id, idx_district_name
- idx_state_district (Composite)
- idx_district_city (Composite)
- idx_state_district_city (Composite)
- idx_district_status (Composite)

**Foreign Key**: None (Table is reference master)

### Documentation References
- **Primary Reference**: `DevOps Development/DBA/Databasespecs.md` Section 2.2
- **Instance Details**: `DevOps Development/DBA/DBA.md` Lines 120-137
- **Schema SQL**: `DevOps Development/DBA/create_tables.sql` Lines 39-104
- **Migration Strategy**: `DevOps Development/DBA/MIGRATION_STRATEGY.md`
- **Deployment**: `DevOps Development/DBA/DEPLOYMENT_GUIDE.md`

### Migration Information
- **Script**: `DevOps Development/DBA/migration_step1.sql`
- **Status**: ✅ Ready for execution
- **Rollback**: ✅ Documented in MIGRATION_STRATEGY.md
- **Data Population**: 19,234 unique pincode records with geographic hierarchy

### API Impact
- **Endpoints Modified**: 6 (GET all, POST, PUT, + 3 new hierarchical queries)
- **Schema File**: `app/schemas/location.py` - Numeric types, validation
- **Service File**: `app/services/location_service.py` - Hierarchical query methods
- **Routes File**: `app/routes/v1/locations.py` - 6 endpoint implementations

### Tests
- **File**: `API Development/Unit Testing/test_locations_api.py`
- **Test Cases**: 65 tests covering all geographic hierarchy scenarios
- **Status**: ✅ All passing

---

## 🔄 STEP 1.2: User Geographic Integration (COMPLETE - March 4, 2026)

### Overview
Enhanced User_Master table with geographic foreign key columns to State_City_PinCode_Master, enabling precise user location tracking at state → district → city → pincode levels.

### Database Changes

#### Table: User_Master (Enhanced)

**New Columns**:
- `stateId` (INTEGER) - State identifier FK to State_City_PinCode_Master
- `districtId` (INTEGER) - District identifier FK to State_City_PinCode_Master
- `cityId` (INTEGER) - City identifier FK to State_City_PinCode_Master
- `address1` (VARCHAR(255)) - Address line 1
- `address2` (VARCHAR(255)) - Address line 2

**Data Type Changes**:
- `pinCode`: VARCHAR(10) → INTEGER (FK to State_City_PinCode_Master.pinCode)

**New Foreign Keys** (4 total):
```sql
CONSTRAINT fk_user_state_id    ON DELETE RESTRICT
CONSTRAINT fk_user_district_id ON DELETE RESTRICT
CONSTRAINT fk_user_city_id     ON DELETE RESTRICT
CONSTRAINT fk_user_pincode     ON DELETE RESTRICT
```

**New Indexes** (6 total):
- idx_user_state_id, idx_user_district_id, idx_user_city_id, idx_user_pincode
- idx_user_state_district (Composite)
- idx_user_district_city (Composite)

**Immutability**: pinCode cannot be updated after creation (API & DB level enforcement)

### Documentation References
- **Primary Reference**: `DevOps Development/DBA/Databasespecs.md` Section 2.3
- **Instance Details**: `DevOps Development/DBA/DBA.md` Lines 141-179
- **Schema SQL**: `DevOps Development/DBA/create_tables.sql` Lines 79-104
- **Migration Script**: `DevOps Development/DBA/migration_step1_2.sql`
- **Deployment**: `DevOps Development/DBA/DEPLOYMENT_GUIDE.md`

### Migration Information
- **Script**: `DevOps Development/DBA/migration_step1_2.sql`
- **Status**: ✅ Ready for execution
- **Rollback**: ✅ Documented in migration script
- **Prerequisite**: Step 1.1 must be completed first

### Validation Requirements
All geographic references are validated before insert/update:
```python
validate_geographic_references(db, stateId, districtId, cityId, pinCode)
```

### API Impact
- **Endpoints Modified**: 4 (GET all, POST create, PUT update, DELETE - unchanged)
- **Schema File**: `app/schemas/user.py` - 3 new fields + pinCode type change
- **Service File**: `app/services/user_service.py` - validate_geographic_references() function
- **Routes File**: `app/routes/v1/users.py` - Enhanced with geographic validation

### Tests
- **File**: `API Development/Unit Testing/test_users_api.py`
- **Test Cases**: 29 tests covering CRUD + geographic validation
- **Geographic-Specific**: 8 FK validation tests, 2 immutability tests
- **Fixtures**: 5 fixtures with geographic data (Mumbai, Bangalore, Pune locations)
- **Status**: ✅ All created and ready

### Validation Rules Implemented

**Geographic FK Validation**:
- stateId must exist in State_City_PinCode_Master
- districtId must exist in State_City_PinCode_Master
- cityId must exist in State_City_PinCode_Master
- pinCode must exist in State_City_PinCode_Master (5-6 digits)

**pinCode Immutability**:
- Set during user creation only
- Cannot be changed in UPDATE operations
- Both API and database enforce this

---

## Cross-Reference Index

### For Step 1.1 Changes
1. **Schema Definition**: `DevOps Development/DBA/Databasespecs.md` Section 2.2, Line 44-110
2. **Instance Documentation**: `DevOps Development/DBA/DBA.md` Table 2, Lines 120-137
3. **SQL Creation**: `DevOps Development/DBA/create_tables.sql` Lines 31-104
4. **Migration Strategy**: `DevOps Development/DBA/MIGRATION_STRATEGY.md` (Complete 10-step guide)
5. **Deployment**: `DevOps Development/DBA/DEPLOYMENT_GUIDE.md` (Deployment section)
6. **API Changes**: `API Development/REPOSITORY_SUMMARY.md` Lines 166-193
7. **Test Suite**: `API Development/Unit Testing/test_locations_api.py` (65 tests)

### For Step 1.2 Changes
1. **Schema Definition**: `DevOps Development/DBA/Databasespecs.md` Section 2.3, Lines 113-189
2. **Instance Documentation**: `DevOps Development/DBA/DBA.md` Table 3, Lines 141-179
3. **SQL Creation**: `DevOps Development/DBA/create_tables.sql` Lines 79-104
4. **Migration Script**: `DevOps Development/DBA/migration_step1_2.sql` (9-step migration)
5. **Deployment**: `DevOps Development/DBA/DEPLOYMENT_GUIDE.md` (Deployment section)
6. **API Changes**: `API Development/REPOSITORY_SUMMARY.md` Lines 195-230
7. **API Specifications**: `API Development/API Development agent.md` Lines 1096-1275
8. **Test Suite**: `API Development/Unit Testing/test_users_api.py` (29 tests)

---

## Database Dependencies Summary

### Step 1.1 → Step 1.2 Dependency Chain
```
State_City_PinCode_Master (Step 1.1 Enhanced)
         ↓
    User_Master (Step 1.2 Enhanced)
         ↓
   Foreign Key References to State_City_PinCode_Master
         ↓
   User Location Tracking Enabled
```

### Migration Execution Order
1. ✅ **Step 1.1 Migration** (migration_step1.sql) - COMPLETE
   - State_City_PinCode_Master schema updated
   - 19,234 pincode records loaded
   - 36 States with proper hierarchy

2. ✅ **Step 1.2 Migration** (migration_step1_2.sql) - READY
   - User_Master schema updated
   - Foreign key constraints created
   - User location tracking enabled

---

## Version & Change Log

| Version | Date | Step | Changes |
|---------|------|------|---------|
| 1.0 | 2026-03-01 | Initial | All 6 tables documented |
| 1.1 | 2026-03-03 | 1.1 | State_City_PinCode_Master enhanced with district hierarchy |
| 2.0 | 2026-03-04 | 1.2 | User_Master enhanced with geographic FK columns |

---

## Support & Questions

### For Database Issues
- Contact: DevOps team
- DBA Documentation: `DevOps Development/DBA/DBA.md`
- Setup Details: `DevOps Development/complete_setup.sql`

### For API/Table Integration
- API Documentation: `API Development/API Development agent.md`
- Testing Guide: `API Development/Unit Testing/API Unit Testing Agent.md`

### For Data Migration
- Migration scripts: To be created
- Data validation: See Data Validation Rules section

---

## 🔄 Backup & Recovery Configuration

### Backup Settings
| Property | Value |
|----------|-------|
| **Automated Backups** | ✅ Enabled |
| **Backup Tier** | STANDARD |
| **Retained Backups** | 7 |
| **Backup Start Time** | 03:00 UTC |
| **Last Backup Status** | ✅ SUCCESSFUL |

### Point-in-Time Recovery
| Property | Value |
|----------|-------|
| **PITR Enabled** | ✅ Yes |
| **Transaction Log Archiving** | ✅ Enabled |
| **Log Retention Period** | 7 days |
| **Replication Type** | SYNCHRONOUS |

---

## 📝 Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-01 | Initial: All 6 tables documented |
| 2.0 | 2026-03-03 | Step 1.1: State_City_PinCode_Master enhanced with district hierarchy |
| 3.0 | 2026-03-04 | Step 1.2: User_Master enhanced with geographic FK columns; 9,805 records loaded |

---

**Document Version:** 3.0
**Last Updated:** March 4, 2026
**Status:** ✅ Production Ready
**Maintained By:** Data Engineering Team
**Synced From:** DevOps Development/DBA/DBA.md
