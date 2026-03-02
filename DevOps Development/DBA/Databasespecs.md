# Database Specifications
## Project: Medostel AI

This document outlines the database schema required to support the Medostel AI application. The schema is designed for a relational database system (e.g., MySQL, PostgreSQL).

### 1. Schema Overview

The database consists of the following core tables:
1.  **`User_Role_Master`**: Defines the available user roles in the system.
2.  **`State_City_PinCode_Master`**: Stores geographic reference data.
3.  **`User_Master`**: Stores the primary demographic and profile information for users.
4.  **`User_Login`**: Manages authentication credentials and login history.
5.  **`New_User_Request`**: Tracks registration requests requiring admin approval.
6.  **`Report_History`**: Stores the history of analyzed medical reports.

---

### 2. Table Definitions & Creation Queries

#### 2.1 Table: `User_Role_Master`
*   **Description**: Master table for user roles.
*   **Primary Key**: `roleId`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `roleId` | VARCHAR(10) | PK, Not Null | Unique Role ID (e.g., DOC01) |
| `roleName` | VARCHAR(50) | Not Null, Unique | Name of the role (e.g., Doctor) |
| `status` | VARCHAR(20) | Not Null | 'Active', 'Inactive', 'Closed' |
| `createdDate` | DATE | Not Null | Date of creation |
| `updatedDate` | DATE | Not Null | Date of last update |
| `comments` | VARCHAR(50) | | Optional comments |

```sql
CREATE TABLE User_Role_Master (
    roleId VARCHAR(10) PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Inactive', 'Closed')),
    createdDate DATE NOT NULL,
    updatedDate DATE NOT NULL,
    comments VARCHAR(50)
);
```

#### 2.2 Table: `State_City_PinCode_Master`
*   **Description**: Master table for geographic data (State, City, Pin Code).
*   **Primary Key**: `pinCode` (INTEGER - Unique 5-6 digit postal code)
*   **Updated**: March 2, 2026 - Changed to INTEGER data types, pinCode as PK for better performance and data integrity

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `pinCode` | INTEGER | PK, Not Null | Postal Code (5-6 digits for India) |
| `stateId` | INTEGER | Not Null | State Identifier (numeric) |
| `stateName` | VARCHAR(100) | Not Null | Name of the State |
| `cityId` | INTEGER | Not Null | City Identifier (numeric) |
| `cityName` | VARCHAR(100) | Not Null | Name of the City |
| `countryName` | VARCHAR(50) | Default 'India' | Country Name |
| `status` | VARCHAR(20) | Not Null | 'Active', 'Inactive' |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Record creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Last update timestamp |

**Indexes:**
- `idx_state_name` on stateName
- `idx_city_name` on cityName
- `idx_state_id` on stateId
- `idx_city_id` on cityId
- `idx_state_city` on (stateId, cityId)
- `idx_status` on status

```sql
CREATE TABLE State_City_PinCode_Master (
    pinCode INTEGER PRIMARY KEY,
    stateId INTEGER NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityId INTEGER NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_state_name ON State_City_PinCode_Master(stateName);
CREATE INDEX idx_city_name ON State_City_PinCode_Master(cityName);
CREATE INDEX idx_state_id ON State_City_PinCode_Master(stateId);
CREATE INDEX idx_city_id ON State_City_PinCode_Master(cityId);
CREATE INDEX idx_state_city ON State_City_PinCode_Master(stateId, cityId);
CREATE INDEX idx_status ON State_City_PinCode_Master(status);
```

**Migration Note:** This table was migrated from using VARCHAR data types and SERIAL id to INTEGER types with pinCode as PRIMARY KEY on March 2, 2026. See `MIGRATION_STRATEGY.md` for details.

#### 2.3 Table: `User_Master`
*   **Description**: Core user profile data with enhanced numeric userId and validation.
*   **Primary Key**: `userId` (BIGINT - supports up to 1 billion users)
*   **Foreign Keys**: `currentRole` -> `User_Role_Master(roleId)`
*   **Updated**: March 1, 2026 - BIGINT userId, email validation, 10-digit mobile validation

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `userId` | BIGINT | PK, Not Null | Numeric User ID (1-1000000000) |
| `firstName` | VARCHAR(100) | Not Null | First Name |
| `lastName` | VARCHAR(100) | Not Null | Last Name |
| `currentRole` | VARCHAR(50) | FK, Not Null | Role ID (references User_Role_Master.roleId) |
| `emailId` | VARCHAR(255) | Unique, Not Null | Email with RFC 5322 validation |
| `mobileNumber` | NUMERIC(10) | Unique, Not Null | 10-digit mobile (1000000000-9999999999) |
| `organisation` | VARCHAR(255) | | Organization Name |
| `address` | TEXT | | Address |
| `status` | VARCHAR(50) | Not Null | 'Active', 'Inactive', 'Suspended' |
| `createdDate` | TIMESTAMP | Not Null | Auto-populated at creation |
| `updatedDate` | TIMESTAMP | Not Null | Auto-populated at update |

```sql
CREATE TABLE User_Master (
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
    FOREIGN KEY (currentRole) REFERENCES User_Role_Master(roleId)
);
```

**Validation Rules**:
- `userId`: BIGINT supports 1 to 1,000,000,000 users
- `emailId`: RFC 5322 regex pattern validation (standard email format)
- `mobileNumber`: Exactly 10 digits in range 1000000000-9999999999
- `status`: Only 'Active', 'Inactive', or 'Suspended'

#### 2.4 Table: `User_Login`
*   **Description**: Authentication details.
*   **Primary Key**: `userId`
*   **Foreign Keys**: `userId` -> `User_Master(userId)`, `roleId` -> `User_Role_Master(roleId)`
*   **Updated**: March 1, 2026 - Changed userId to BIGINT to match User_Master

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `userId` | BIGINT | PK, FK | Link to User Master (Numeric ID) |
| `username` | VARCHAR(100) | Not Null, Unique | Login Username |
| `password` | VARCHAR(255) | Not Null | Hashed Password |
| `roleId` | VARCHAR(50) | FK, Not Null | Link to Role ID |
| `isActive` | BOOLEAN | Default TRUE | Account Active Status |
| `lastLoginTime` | TIMESTAMP | | Timestamp of last login |
| `loginAttempts` | INTEGER | Default 0 | Failed login attempts counter |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Record creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Record update timestamp |

```sql
CREATE TABLE User_Login (
    userId BIGINT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    roleId VARCHAR(50) NOT NULL,
    isActive BOOLEAN DEFAULT TRUE,
    lastLoginTime TIMESTAMP,
    loginAttempts INTEGER DEFAULT 0,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES User_Master(userId),
    FOREIGN KEY (roleId) REFERENCES User_Role_Master(roleId)
);
```

#### 2.5 Table: `New_User_Request`
*   **Description**: Staging table for new user registrations with validation matching User_Master.
*   **Primary Key**: `requestId`
*   **Updated**: March 1, 2026 - Added email format validation and 10-digit mobile validation

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `requestId` | VARCHAR(100) | PK | Unique Request ID |
| `userName` | VARCHAR(100) | Not Null | Requested Username |
| `firstName` | VARCHAR(100) | Not Null | First Name |
| `lastName` | VARCHAR(100) | Not Null | Last Name |
| `currentRole` | VARCHAR(50) | Not Null | Requested Role |
| `emailId` | VARCHAR(255) | Unique, Not Null | Email with RFC 5322 validation |
| `mobileNumber` | NUMERIC(10) | Not Null | 10-digit mobile (1000000000-9999999999) |
| `address` | TEXT | | Address |
| `requestStatus` | VARCHAR(50) | Default 'Pending' | 'Pending', 'Approved', 'Rejected' |
| `approvalDate` | TIMESTAMP | | Approval timestamp |
| `approvalComments` | TEXT | | Approval comments |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

```sql
CREATE TABLE New_User_Request (
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
```

**Validation Rules**:
- `emailId`: RFC 5322 regex pattern (same as User_Master)
- `mobileNumber`: NUMERIC(10) with exactly 10 digits (1000000000-9999999999)

#### 2.6 Table: `Report_History`
*   **Description**: Stores metadata and links to generated medical reports.
*   **Primary Key**: `id`
*   **Foreign Keys**: `userId` -> `User_Master(userId)`
*   **Updated**: March 1, 2026 - Changed userId to BIGINT to match User_Master

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR(100) | PK | Unique Report ID |
| `userId` | BIGINT | FK, Not Null | Report owner (Numeric User ID) |
| `fileName` | VARCHAR(255) | | Original file name |
| `fileType` | VARCHAR(50) | | File type (pdf, image, etc.) |
| `reportType` | VARCHAR(100) | | Type of report (e.g., Blood Test) |
| `status` | VARCHAR(50) | Default 'Pending' | 'Pending', 'Completed', 'Failed' |
| `diagnosis` | TEXT | | Medical diagnosis |
| `inferredDiagnosis` | TEXT | | AI inferred diagnosis |
| `pdfUrl` | VARCHAR(500) | | URL to the generated PDF |
| `bucketLocation` | VARCHAR(500) | | Cloud storage bucket path |
| `jsonData` | JSONB | | Full analysis result in JSONB |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

```sql
CREATE TABLE Report_History (
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
    FOREIGN KEY (userId) REFERENCES User_Master(userId)
);
```
