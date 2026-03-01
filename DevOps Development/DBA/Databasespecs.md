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
*   **Primary Key**: Composite (`stateId`, `cityId`, `pinCode`) or Surrogate Key.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `stateId` | VARCHAR(10) | Not Null | State Identifier |
| `stateName` | VARCHAR(100) | Not Null | Name of the State |
| `cityName` | VARCHAR(100) | Not Null | Name of the City |
| `cityId` | VARCHAR(10) | Not Null | City Identifier |
| `pinCode` | VARCHAR(10) | Not Null | Postal Code |
| `countryName` | VARCHAR(50) | Default 'India' | Country Name |
| `status` | VARCHAR(20) | Not Null | 'Active', 'Inactive' |

```sql
CREATE TABLE State_City_PinCode_Master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stateId VARCHAR(10) NOT NULL,
    stateName VARCHAR(100) NOT NULL,
    cityName VARCHAR(100) NOT NULL,
    cityId VARCHAR(10) NOT NULL,
    pinCode VARCHAR(10) NOT NULL,
    countryName VARCHAR(50) DEFAULT 'India',
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Inactive'))
);
```

#### 2.3 Table: `User_Master`
*   **Description**: Core user profile data.
*   **Primary Key**: `userId` (Email)
*   **Foreign Keys**: `currentRole` -> `User_Role_Master(roleName)`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `userId` | VARCHAR(100) | PK, Not Null | Email ID used as User ID |
| `firstName` | VARCHAR(50) | Not Null | First Name |
| `lastName` | VARCHAR(50) | Not Null | Last Name |
| `currentRole` | VARCHAR(50) | FK, Not Null | Role Name |
| `organisation` | VARCHAR(100) | | Organization Name |
| `emailId` | VARCHAR(100) | Not Null | Contact Email |
| `mobileNumber` | VARCHAR(15) | Unique, Not Null | Mobile Number |
| `address1` | VARCHAR(255) | | Address Line 1 |
| `address2` | VARCHAR(255) | | Address Line 2 |
| `stateName` | VARCHAR(100) | | State |
| `cityName` | VARCHAR(100) | | City |
| `pinCode` | VARCHAR(10) | | Pin Code |
| `status` | VARCHAR(20) | Not Null | 'Active', 'Inactive' |

```sql
CREATE TABLE User_Master (
    userId VARCHAR(100) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    organisation VARCHAR(100),
    emailId VARCHAR(100) NOT NULL,
    mobileNumber VARCHAR(15) NOT NULL UNIQUE,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateName VARCHAR(100),
    cityName VARCHAR(100),
    pinCode VARCHAR(10),
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Inactive')),
    FOREIGN KEY (currentRole) REFERENCES User_Role_Master(roleName)
);
```

#### 2.4 Table: `User_Login`
*   **Description**: Authentication details.
*   **Primary Key**: `userId`
*   **Foreign Keys**: `userId` -> `User_Master(userId)`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `userId` | VARCHAR(100) | PK, FK | Link to User Master |
| `username` | VARCHAR(100) | Not Null | Login Username (same as userId) |
| `passwordHash` | VARCHAR(255) | Not Null | Hashed Password |
| `mobilePhone` | VARCHAR(15) | | Redundant for quick access |
| `roleId` | VARCHAR(10) | FK | Link to Role ID |
| `isActive` | BOOLEAN | Default TRUE | Account Active Status |
| `lastLoginAt` | DATETIME | | Timestamp of last login |
| `passwordLastChangedAt` | DATETIME | | Timestamp of last password change |
| `createdAt` | DATETIME | | Record creation timestamp |
| `updatedAt` | DATETIME | | Record update timestamp |

```sql
CREATE TABLE User_Login (
    userId VARCHAR(100) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    mobilePhone VARCHAR(15),
    roleId VARCHAR(10),
    isActive BOOLEAN DEFAULT TRUE,
    lastLoginAt DATETIME,
    passwordLastChangedAt DATETIME,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES User_Master(userId),
    FOREIGN KEY (roleId) REFERENCES User_Role_Master(roleId)
);
```

#### 2.5 Table: `New_User_Request`
*   **Description**: Staging table for new user registrations.
*   **Primary Key**: `requestId`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `requestId` | VARCHAR(20) | PK | Unique Request ID |
| `userName` | VARCHAR(100) | Not Null | Requested Username/Email |
| `firstName` | VARCHAR(50) | Not Null | First Name |
| `lastName` | VARCHAR(50) | Not Null | Last Name |
| `currentRole` | VARCHAR(50) | Not Null | Requested Role |
| `organisation` | VARCHAR(100) | | Organization |
| `emailId` | VARCHAR(100) | Not Null | Email |
| `mobileNumber` | VARCHAR(15) | Not Null | Mobile |
| `address1` | VARCHAR(255) | | Address 1 |
| `address2` | VARCHAR(255) | | Address 2 |
| `stateName` | VARCHAR(100) | | State |
| `cityName` | VARCHAR(100) | | City |
| `pinCode` | VARCHAR(10) | | Pin Code |
| `requestStatus` | VARCHAR(20) | Not Null | 'Pending', 'Approved', 'Rejected' |

```sql
CREATE TABLE New_User_Request (
    requestId VARCHAR(20) PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    organisation VARCHAR(100),
    emailId VARCHAR(100) NOT NULL,
    mobileNumber VARCHAR(15) NOT NULL,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateName VARCHAR(100),
    cityName VARCHAR(100),
    pinCode VARCHAR(10),
    requestStatus VARCHAR(20) NOT NULL CHECK (requestStatus IN ('Pending', 'Approved', 'Rejected'))
);
```

#### 2.6 Table: `Report_History`
*   **Description**: Stores metadata and links to generated reports.
*   **Primary Key**: `id`
*   **Foreign Keys**: `userId` -> `User_Master(userId)`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR(50) | PK | Unique Report ID |
| `userId` | VARCHAR(100) | FK | Owner of the report |
| `timestamp` | DATETIME | Not Null | Upload/Generation time |
| `fileName` | VARCHAR(255) | Not Null | Original file name |
| `fileType` | VARCHAR(10) | Not Null | 'pdf' or 'image' |
| `reportType` | VARCHAR(100) | | Type of report (e.g., Blood Test) |
| `inferredDiagnosis` | TEXT | | AI inferred diagnosis |
| `pdfUrl` | TEXT | | URL to the generated PDF |
| `bucketLocation` | VARCHAR(255) | | Storage bucket path |
| `jsonData` | JSON | | Full analysis result in JSON |

```sql
CREATE TABLE Report_History (
    id VARCHAR(50) PRIMARY KEY,
    userId VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    fileName VARCHAR(255) NOT NULL,
    fileType VARCHAR(10) NOT NULL,
    reportType VARCHAR(100),
    inferredDiagnosis TEXT,
    pdfUrl TEXT,
    bucketLocation VARCHAR(255),
    jsonData JSON,
    FOREIGN KEY (userId) REFERENCES User_Master(userId)
);
```
