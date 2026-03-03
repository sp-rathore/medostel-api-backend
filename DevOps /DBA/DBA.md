# PostgreSQL Instance - Complete DBA Documentation

## 🔷 PostgreSQL Instance Overview

### Instance Details
| Property | Value |
|----------|-------|
| **Instance Name** | medostel-ai-assistant-pgdev-instance |
| **Instance Type** | Cloud SQL (Second Generation) |
| **Database Engine** | PostgreSQL 18 (18.2) |
| **Edition** | ENTERPRISE |
| **Status** | 🟢 RUNNABLE |
| **Project ID** | gen-lang-client-0064186167 |
| **Region** | asia-south1 (Mumbai) |
| **Zone** | asia-south1-c |
| **Created** | 2026-02-28 09:37:34 UTC |

### Network Configuration
| Property | Value |
|----------|-------|
| **Primary IP** | 35.244.27.232 |
| **Outgoing IP** | 34.100.144.210 |
| **Connection Name** | gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance |
| **IPv4 Enabled** | ✅ Yes |
| **SSL/TLS** | ALLOW_UNENCRYPTED_AND_ENCRYPTED |
| **Network Architecture** | New Network Architecture |

---

## 💾 Hardware & Storage Configuration

| Property | Value |
|----------|-------|
| **Machine Type** | db-custom-1-3840 |
| **vCPU** | 1 |
| **Memory** | 3.84 GB RAM |
| **Data Disk Type** | PD-SSD (Persistent Disk SSD) |
| **Data Disk Size** | 10 GB |
| **Storage Auto-Resize** | ✅ Enabled |
| **Backend Type** | SECOND_GEN |

---

## 🔐 Database Roles & Credentials

### ROLE 1: medostel_admin
**Purpose**: Full administrative access

| Property | Value |
|----------|-------|
| **Role Name** | `medostel_admin` |
| **Role Type** | SUPERUSER |
| **Privileges** | CREATEDB, CREATEROLE, SUPERUSER |
| **Inheritance** | NOINHERIT |
| **User Account** | `medostel_admin_user` |
| **Password** | `Iag2bMi@0@6aA` |
| **Database Privileges** | ALL PRIVILEGES on "Medostel" |

**Capabilities**:
- ✅ Create databases
- ✅ Create roles
- ✅ Full superuser access
- ✅ All schema operations
- ✅ Manage all tables and objects

---

### ROLE 2: medostel_api
**Purpose**: Application API access with limited permissions

| Property | Value |
|----------|-------|
| **Role Name** | `medostel_api` |
| **Role Type** | Standard Role |
| **Privileges** | NOINHERIT, NOSUPERUSER |
| **User Account** | `medostel_api_user` |
| **Password** | `Iag2bMi@0@6aD` |
| **Database Privileges** | CONNECT on "Medostel" |

**Capabilities**:
- ✅ Connect to "Medostel" database
- ✅ SELECT, INSERT, UPDATE, DELETE on all tables
- ✅ USAGE and SELECT on sequences
- ✅ CREATE on public schema
- ❌ No superuser privileges
- ❌ No role creation

---

## 📊 Databases in Instance

| Database | Owner | Type | Tables | Size | Status |
|----------|-------|------|--------|------|--------|
| **medostel** ⭐ | postgres | User | 6 | 304 kB | ✅ Active |
| postgres | cloudsqlsuperuser | System | 0 | - | System DB |
| cloudsqladmin | cloudsqladmin | System | 0 | - | Cloud SQL System |
| template1 | cloudsqlsuperuser | Template | 0 | - | Template |

---

## 📋 MEDOSTEL Database - Table Definitions

### TABLE 1: User_Role_Master
**Purpose**: Master table for user roles and permissions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `roleId` | VARCHAR(10) | PK, Not Null | Unique Role ID |
| `roleName` | VARCHAR(50) | Not Null, Unique | Role name |
| `status` | VARCHAR(20) | Default 'Active' | Active/Inactive/Closed |
| `createdDate` | DATE | Not Null | Creation date |
| `updatedDate` | DATE | Not Null | Last update date |
| `comments` | VARCHAR(250) | | Optional notes |

**Indexes**: `idx_user_role_name`, `idx_user_role_status`
**Size**: 32 kB | **Owner**: medostel_admin_user

---

### TABLE 2: State_City_PinCode_Master
**Purpose**: Geographic reference data (State, City, Pin Code)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PK | Auto-increment ID |
| `stateId` | VARCHAR(10) | Not Null | State identifier |
| `stateName` | VARCHAR(100) | Not Null | State name |
| `cityName` | VARCHAR(100) | Not Null | City name |
| `cityId` | VARCHAR(10) | Not Null | City identifier |
| `pinCode` | VARCHAR(10) | Not Null | Postal code |
| `countryName` | VARCHAR(50) | Default 'India' | Country |
| `status` | VARCHAR(20) | Default 'Active' | Active/Inactive |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Indexes**: `idx_state_name`, `idx_city_name`, `idx_pincode`, `idx_state_city`
**Size**: 40 kB | **Owner**: medostel_admin_user

---

### TABLE 3: User_Master
**Purpose**: Core user profile and demographic data with geographic hierarchy integration (ENHANCED - March 4, 2026)
**Primary Key**: `userId` (VARCHAR(100) - Email address)
**Schema Version**: 3.0 (Added geographic FK columns: stateId, districtId, cityId; Changed pinCode from VARCHAR to INTEGER)
**Foreign Keys**:
- `currentRole` → User_Role_Master(roleName)
- `stateId` → State_City_PinCode_Master(stateId)
- `districtId` → State_City_PinCode_Master(districtId)
- `cityId` → State_City_PinCode_Master(cityId)
- `pinCode` → State_City_PinCode_Master(pinCode)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `userId` | VARCHAR(100) | PK, Not Null | Email address (unique user identifier) |
| `firstName` | VARCHAR(50) | Not Null | First name |
| `lastName` | VARCHAR(50) | Not Null | Last name |
| `currentRole` | VARCHAR(50) | FK, Not Null | References User_Role_Master(roleName) |
| `organisation` | VARCHAR(100) | | Organization name |
| `emailId` | VARCHAR(100) | Not Null, Unique | Email address (RFC 5322 validation) |
| `mobileNumber` | VARCHAR(15) | Not Null, Unique | Mobile number |
| `address1` | VARCHAR(255) | | Address line 1 |
| `address2` | VARCHAR(255) | | Address line 2 |
| `stateId` | INTEGER | FK | State ID (references State_City_PinCode_Master) |
| `stateName` | VARCHAR(100) | | State name (for display) |
| `districtId` | INTEGER | FK | District ID (references State_City_PinCode_Master) |
| `cityId` | INTEGER | FK | City ID (references State_City_PinCode_Master) |
| `cityName` | VARCHAR(100) | | City name (for display) |
| `pinCode` | INTEGER | FK | Postal code (references State_City_PinCode_Master) |
| `status` | VARCHAR(20) | Default 'Active' | Active/Inactive |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Geographic Hierarchy Integration**:
- Users now linked to State_City_PinCode_Master through 4 FK columns (stateId, districtId, cityId, pinCode)
- Enables precise location tracking at state → district → city → pincode levels
- All geographic field values must exist in State_City_PinCode_Master table
- ON DELETE RESTRICT prevents deletion of geographic references while users exist

**Indexes**: `idx_user_email`, `idx_user_mobile`, `idx_user_role`, `idx_user_status`, `idx_user_state_id`, `idx_user_district_id`, `idx_user_city_id`, `idx_user_pincode`, `idx_user_state_district`, `idx_user_district_city`
**Size**: ~120 kB | **Owner**: medostel_admin_user
**Migration**: See migration_step1_2.sql for geographic hierarchy enhancement

---

### TABLE 4: User_Login
**Purpose**: Authentication and login credentials (UPDATED - March 1, 2026)
**Primary Key**: `userId`
**Foreign Keys**: `userId` → User_Master(userId - BIGINT), `roleId` → User_Role_Master(roleId)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `userId` | BIGINT | PK, FK, Not Null | User ID (numeric, references User_Master) |
| `username` | VARCHAR(100) | Not Null, Unique | Login username |
| `password` | VARCHAR(255) | Not Null | Hashed password |
| `roleId` | VARCHAR(50) | FK, Not Null | Role ID (references User_Role_Master) |
| `isActive` | BOOLEAN | Default TRUE | Account active status |
| `lastLoginTime` | TIMESTAMP | | Last login timestamp |
| `loginAttempts` | INTEGER | Default 0 | Failed login attempts counter |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Indexes**: `idx_login_username`, `idx_login_role`, `idx_login_active`, `idx_login_attempts`, `idx_login_lastlogin`, `idx_login_updated`
**Size**: ~48 kB | **Owner**: medostel_admin_user

---

### TABLE 5: New_User_Request
**Purpose**: Staging table for new user registration requests (ENHANCED - March 1, 2026)
**Primary Key**: `requestId`
**Schema Version**: 2.0 (Added email & mobile validation matching User_Master)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `requestId` | VARCHAR(100) | PK | Unique request ID |
| `userName` | VARCHAR(100) | Not Null | Requested username |
| `firstName` | VARCHAR(100) | Not Null | First name |
| `lastName` | VARCHAR(100) | Not Null | Last name |
| `currentRole` | VARCHAR(50) | Not Null | Requested role |
| `emailId` | VARCHAR(255) | Not Null, Unique | RFC 5322 email format validation |
| `mobileNumber` | NUMERIC(10) | Not Null | 10-digit mobile (1000000000-9999999999) |
| `address` | TEXT | | Full address |
| `requestStatus` | VARCHAR(50) | Default 'Pending' | Pending/Approved/Rejected |
| `approvalDate` | TIMESTAMP | | Approval timestamp |
| `approvalComments` | TEXT | | Approval comments |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Validation Constraints**:
- `emailId`: CHECK (emailId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
- `mobileNumber`: CHECK (mobileNumber >= 1000000000 AND mobileNumber <= 9999999999)

**Indexes**: `idx_request_email`, `idx_request_mobile`, `idx_request_status`, `idx_request_role`, `idx_request_created`, `idx_request_updated`
**Size**: ~64 kB | **Owner**: medostel_admin_user

---

### TABLE 6: Report_History
**Purpose**: Medical report analysis and storage history (UPDATED - March 1, 2026)
**Primary Key**: `id`
**Foreign Key**: `userId` → User_Master(userId - BIGINT)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | VARCHAR(100) | PK | Unique report ID |
| `userId` | BIGINT | Not Null, FK | Report owner (numeric, references User_Master) |
| `fileName` | VARCHAR(255) | | Original file name |
| `fileType` | VARCHAR(50) | | File type (pdf, image, etc.) |
| `reportType` | VARCHAR(100) | | Report type (e.g., Blood Test) |
| `status` | VARCHAR(50) | Default 'Pending' | Pending/Completed/Failed |
| `diagnosis` | TEXT | | Medical diagnosis |
| `inferredDiagnosis` | TEXT | | AI inferred diagnosis |
| `pdfUrl` | VARCHAR(500) | | URL to generated PDF |
| `bucketLocation` | VARCHAR(500) | | Cloud storage bucket path |
| `jsonData` | JSONB | | Full analysis in JSONB format |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Indexes**: `idx_report_user`, `idx_report_type`, `idx_report_status`, `idx_report_created`, `idx_report_updated`
**Size**: ~64 kB | **Owner**: medostel_admin_user

---

## 🔄 Backup & Recovery Configuration

### Backup Settings
| Property | Value |
|----------|-------|
| **Automated Backups** | ✅ Enabled |
| **Backup Tier** | STANDARD |
| **Retained Backups** | 7 |
| **Backup Start Time** | 03:00 UTC |
| **Last Backup Status** | ✅ SUCCESSFUL (2026-02-28 09:41:04 UTC) |

### Point-in-Time Recovery
| Property | Value |
|----------|-------|
| **PITR Enabled** | ✅ Yes |
| **Transaction Log Archiving** | ✅ Enabled |
| **Log Retention Period** | 7 days |
| **Log Storage State** | CLOUD_STORAGE |
| **Replication Type** | SYNCHRONOUS |

---

## 🔒 Security & Availability

### Security Features
| Feature | Status |
|---------|--------|
| Server CA Certificate | ✅ Active (Valid until 2036-02-26) |
| Deletion Protection | ❌ Disabled |
| Private IP Path for GCP | ❌ Disabled |
| SSL/TLS Support | ✅ Enabled |
| Server Certificate Rotation | UNSPECIFIED |

### Availability Configuration
| Property | Value |
|----------|-------|
| **Availability Type** | ZONAL |
| **Activation Policy** | ALWAYS |
| **Replication Type** | SYNCHRONOUS |

### Advanced Features
| Feature | Status |
|---------|--------|
| Gemini AI Index Advisor | ❌ Disabled |
| Gemini Query Analysis | ❌ Disabled |
| Google ML Integration | ❌ Disabled |
| OOM Session Cancel | ✅ Enabled |
| Private Path for GCP Services | ❌ Disabled |

---

## 💰 Pricing & Maintenance

| Property | Value |
|----------|-------|
| **Pricing Plan** | PER_USE |
| **Current Version** | POSTGRES_18_2.R20260108.01_14 |
| **Maintenance Window** | Sunday 00:00 UTC |
| **Auto Repair** | ✅ Enabled |
| **Auto Upgrade** | ✅ Enabled |

---

## 📊 Summary

### ✅ medostel Database
- **Tables**: 6 application tables
- **Indexes**: 35 total
- **Size**: 304 kB
- **Owner**: medostel_admin_user
- **Status**: Complete schema with relationships and indexes, ready for production use

### ✅ Database Roles
- **medostel_admin**: Superuser for administration
- **medostel_api**: Limited API access for application

### ✅ Backup & Recovery
- Automated daily backups with 7-day retention
- Point-in-time recovery enabled
- Transaction log archiving active
- Last backup successful

### ✅ Other System Databases
- postgres (empty - default system database)
- cloudsqladmin (empty - Cloud SQL system database)
- template1 (template database)

---

## 📝 Connection Details

### For Application (medostel_api_user)
```
Host: 35.244.27.232
Port: 5432
Database: medostel
Username: medostel_api_user
Password: Iag2bMi@0@6aD
Connection String: postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel
```

### For Administration (medostel_admin_user)
```
Host: 35.244.27.232
Port: 5432
Database: medostel
Username: medostel_admin_user
Password: Iag2bMi@0@6aA
Connection String: postgresql://medostel_admin_user:Iag2bMi@0@6aA@35.244.27.232:5432/medostel
```

---

## ⚠️ Security Notes for Production

- Change default passwords before production deployment
- Store credentials in Google Secret Manager or environment variables
- Enable SSL/TLS for all connections
- Implement connection pooling
- Rotate credentials regularly
- Set up monitoring and alerting
- Review and restrict authorized networks
- Enable deletion protection for production instances

---

**Last Updated**: 2026-03-04 (Step 1.2 Geographic Hierarchy Enhancement)
**Instance**: medostel-ai-assistant-pgdev-instance
**Status**: RUNNABLE ✅
**Environment**: Development/Pre-Production

---

## 📝 Schema Update History

### Step 1.1 (Completed - March 3, 2026)
- **Table**: State_City_PinCode_Master
- **Enhancement**: Added District-level geographic hierarchy (districtId, districtName)
- **Indexes**: Created 6 new composite indexes for hierarchical queries
- **Migration**: migration_step1_1.sql

### Step 1.2 (Completed - March 4, 2026)
- **Table**: User_Master
- **Enhancement**: Added geographic FK columns (stateId, districtId, cityId, pinCode)
- **Data Type Change**: pinCode from VARCHAR(10) to INTEGER
- **Foreign Keys**: Added 4 FK constraints to State_City_PinCode_Master
- **Indexes**: Created 6 new performance indexes
- **Migration**: migration_step1_2.sql
- **Backup**: User_Master_Backup_Step1_2 table created for rollback
