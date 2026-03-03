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
*   **Description**: Master table for geographic data with hierarchical structure: Country → State → District → City → PinCode.
*   **Primary Key**: `pinCode` (INTEGER - Unique 5-6 digit postal code)
*   **Hierarchy**: CountryName (India) → StateID/StateName → DistrictID/DistrictName → CityID/CityName → PinCode
*   **Updated**: March 2, 2026 - Changed to INTEGER data types, pinCode as PK
*   **Updated**: March 3, 2026 - Added District columns (districtId, districtName) with hierarchical ID assignment

**Geographic Hierarchy & ID Assignment:**
- **CountryID**: Always 0001, CountryName: India
- **StateID**: 0001-0035 (28 states + 7 UTs), sequential assignment
- **DistrictID**: 0001-N per state, resets for each state
- **CityID**: 0001-N per district, resets for each district
- **PinCode**: 6-digit unique postal code (PRIMARY KEY)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `pinCode` | INTEGER | PK, Not Null | Postal Code (5-6 digits for India, unique) |
| `stateId` | INTEGER | Not Null | State Identifier (0001-0035, same for all rows of a state) |
| `stateName` | VARCHAR(100) | Not Null | Name of the State/UT |
| `districtId` | INTEGER | Not Null | District Identifier (0001-N per state, resets per state) |
| `districtName` | VARCHAR(100) | Not Null | Name of the District |
| `cityId` | INTEGER | Not Null | City Identifier (0001-N per district, resets per district) |
| `cityName` | VARCHAR(100) | Not Null | Name of the City (proper city names, not post office names) |
| `countryName` | VARCHAR(50) | Default 'India' | Country Name |
| `status` | VARCHAR(20) | Not Null | 'Active', 'Inactive' |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Record creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Last update timestamp |

**Indexes:**
- Single column: `idx_state_id`, `idx_district_id`, `idx_city_id`, `idx_state_name`, `idx_district_name`, `idx_city_name`, `idx_status`
- Composite (Hierarchical): `idx_state_district` (stateId, districtId), `idx_district_city` (districtId, cityId), `idx_state_district_city` (stateId, districtId, cityId), `idx_district_status` (districtId, status)

```sql
CREATE TABLE State_City_PinCode_Master (
    pinCode INTEGER PRIMARY KEY,
    stateId INTEGER NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    districtId INTEGER NOT NULL,
    districtName VARCHAR(100) NOT NULL,
    cityId INTEGER NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    countryName VARCHAR(50) NOT NULL DEFAULT 'India',
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_state_id ON State_City_PinCode_Master(stateId);
CREATE INDEX idx_district_id ON State_City_PinCode_Master(districtId);
CREATE INDEX idx_city_id ON State_City_PinCode_Master(cityId);
CREATE INDEX idx_state_name ON State_City_PinCode_Master(stateName);
CREATE INDEX idx_district_name ON State_City_PinCode_Master(districtName);
CREATE INDEX idx_city_name ON State_City_PinCode_Master(cityName);
CREATE INDEX idx_status ON State_City_PinCode_Master(status);

-- Composite indexes for hierarchical queries
CREATE INDEX idx_state_district ON State_City_PinCode_Master(stateId, districtId);
CREATE INDEX idx_district_city ON State_City_PinCode_Master(districtId, cityId);
CREATE INDEX idx_state_district_city ON State_City_PinCode_Master(stateId, districtId, cityId);
CREATE INDEX idx_district_status ON State_City_PinCode_Master(districtId, status);
```

**Migration Notes:**
- Table was migrated from VARCHAR data types with SERIAL id to INTEGER types with pinCode as PRIMARY KEY on March 2, 2026
- District columns (districtId, districtName) added on March 3, 2026 with hierarchical ID assignment
- See `MIGRATION_STRATEGY.md` for migration details
- See `Data Extraction/OGD_Data_Extraction_Process.md` for data population process

#### 2.3 Table: `User_Master`
*   **Description**: Core user profile data with geographic hierarchy integration
*   **Primary Key**: `userId` (VARCHAR(100) - Email address)
*   **Foreign Keys**:
    - `currentRole` -> `User_Role_Master(roleName)`
    - `stateId` -> `State_City_PinCode_Master(stateId)`
    - `districtId` -> `State_City_PinCode_Master(districtId)`
    - `cityId` -> `State_City_PinCode_Master(cityId)`
    - `pinCode` -> `State_City_PinCode_Master(pinCode)`
*   **Updated**: March 4, 2026 - Added geographic FK columns (stateId, districtId, cityId, pinCode)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `userId` | VARCHAR(100) | PK, Not Null | User ID (Email) |
| `firstName` | VARCHAR(50) | Not Null | First Name |
| `lastName` | VARCHAR(50) | Not Null | Last Name |
| `currentRole` | VARCHAR(50) | FK, Not Null | Role Name (references User_Role_Master.roleName) |
| `organisation` | VARCHAR(100) | | Organization Name |
| `emailId` | VARCHAR(100) | Unique, Not Null | Email Address |
| `mobileNumber` | VARCHAR(15) | Unique, Not Null | Mobile Number |
| `address1` | VARCHAR(255) | | Address Line 1 |
| `address2` | VARCHAR(255) | | Address Line 2 |
| `stateId` | INTEGER | FK | State ID (references State_City_PinCode_Master.stateId) |
| `stateName` | VARCHAR(100) | | State Name (for display) |
| `districtId` | INTEGER | FK | District ID (references State_City_PinCode_Master.districtId) |
| `cityId` | INTEGER | FK | City ID (references State_City_PinCode_Master.cityId) |
| `cityName` | VARCHAR(100) | | City Name (for display) |
| `pinCode` | INTEGER | FK | Pin Code (references State_City_PinCode_Master.pinCode) |
| `status` | VARCHAR(20) | Not Null | 'Active' or 'Inactive' |
| `createdDate` | TIMESTAMP | | Auto-populated at creation |
| `updatedDate` | TIMESTAMP | | Auto-populated at update |

```sql
CREATE TABLE User_Master (
    userId VARCHAR(100) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    organisation VARCHAR(100),
    emailId VARCHAR(100) NOT NULL UNIQUE,
    mobileNumber VARCHAR(15) NOT NULL UNIQUE,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateId INTEGER,
    stateName VARCHAR(100),
    districtId INTEGER,
    cityId INTEGER,
    cityName VARCHAR(100),
    pinCode INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
        CHECK (status IN ('Active', 'Inactive')),
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (currentRole) REFERENCES User_Role_Master(roleName) ON DELETE RESTRICT,
    FOREIGN KEY (stateId) REFERENCES State_City_PinCode_Master(stateId) ON DELETE RESTRICT,
    FOREIGN KEY (districtId) REFERENCES State_City_PinCode_Master(districtId) ON DELETE RESTRICT,
    FOREIGN KEY (cityId) REFERENCES State_City_PinCode_Master(cityId) ON DELETE RESTRICT,
    FOREIGN KEY (pinCode) REFERENCES State_City_PinCode_Master(pinCode) ON DELETE RESTRICT
);
```

**Geographic Hierarchy Integration** (Step 1.2):
- Users are now linked to specific geographic locations through State_City_PinCode_Master
- `stateId`, `districtId`, `cityId`, `pinCode` are foreign keys for data integrity
- Text fields (`stateName`, `cityName`) retained for display purposes
- Allows users to be precisely located at state → district → city → pincode levels
- All geographic field values must exist in State_City_PinCode_Master table

**Validation Rules**:
- `userId`: Email-based unique identifier
- `emailId`: Unique email address
- `mobileNumber`: Unique phone number
- `stateId`: Must reference valid state in State_City_PinCode_Master
- `districtId`: Must reference valid district in State_City_PinCode_Master
- `cityId`: Must reference valid city in State_City_PinCode_Master
- `pinCode`: Must reference valid pincode in State_City_PinCode_Master
- `status`: Only 'Active' or 'Inactive'

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
