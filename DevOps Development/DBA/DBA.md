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
**Purpose**: Core user profile and demographic data
**Primary Key**: `userId` (Email)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `userId` | VARCHAR(100) | PK | Email ID (User ID) |
| `firstName` | VARCHAR(50) | Not Null | First name |
| `lastName` | VARCHAR(50) | Not Null | Last name |
| `currentRole` | VARCHAR(50) | FK, Not Null | References User_Role_Master |
| `organisation` | VARCHAR(100) | | Organization name |
| `emailId` | VARCHAR(100) | Not Null, Unique | Email address |
| `mobileNumber` | VARCHAR(15) | Not Null, Unique | Mobile number |
| `address1` | VARCHAR(255) | | Address line 1 |
| `address2` | VARCHAR(255) | | Address line 2 |
| `stateName` | VARCHAR(100) | | State |
| `cityName` | VARCHAR(100) | | City |
| `pinCode` | VARCHAR(10) | | Pin code |
| `status` | VARCHAR(20) | Default 'Active' | Active/Inactive |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Indexes**: `idx_user_email`, `idx_user_mobile`, `idx_user_role`, `idx_user_status`, `idx_user_created_date`
**Size**: 72 kB | **Owner**: medostel_admin_user

---

### TABLE 4: User_Login
**Purpose**: Authentication and login credentials
**Primary Key**: `userId`
**Foreign Keys**: `userId` → User_Master, `roleId` → User_Role_Master

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `userId` | VARCHAR(100) | PK, FK | User ID (references User_Master) |
| `username` | VARCHAR(100) | Not Null, Unique | Login username |
| `passwordHash` | VARCHAR(255) | Not Null | Hashed password |
| `mobilePhone` | VARCHAR(15) | | Mobile phone |
| `roleId` | VARCHAR(10) | FK | Role ID (references User_Role_Master) |
| `isActive` | BOOLEAN | Default TRUE | Account active status |
| `lastLoginAt` | TIMESTAMP | | Last login timestamp |
| `passwordLastChangedAt` | TIMESTAMP | | Password change timestamp |
| `createdAt` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedAt` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Indexes**: `idx_login_username`, `idx_login_role_id`, `idx_login_active`, `idx_login_last_login`
**Size**: 48 kB | **Owner**: medostel_admin_user

---

### TABLE 5: New_User_Request
**Purpose**: Staging table for new user registration requests
**Primary Key**: `requestId`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `requestId` | VARCHAR(20) | PK | Unique request ID |
| `userName` | VARCHAR(100) | Not Null | Requested username |
| `firstName` | VARCHAR(50) | Not Null | First name |
| `lastName` | VARCHAR(50) | Not Null | Last name |
| `currentRole` | VARCHAR(50) | Not Null | Requested role |
| `organisation` | VARCHAR(100) | | Organization |
| `emailId` | VARCHAR(100) | Not Null, Unique | Email address |
| `mobileNumber` | VARCHAR(15) | Not Null, Unique | Mobile number |
| `address1` | VARCHAR(255) | | Address line 1 |
| `address2` | VARCHAR(255) | | Address line 2 |
| `stateName` | VARCHAR(100) | | State |
| `cityName` | VARCHAR(100) | | City |
| `pinCode` | VARCHAR(10) | | Pin code |
| `requestStatus` | VARCHAR(20) | Default 'Pending' | Pending/Approved/Rejected |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |
| `approvedBy` | VARCHAR(100) | | Approver's email |
| `approvalRemarks` | TEXT | | Approval comments |

**Indexes**: `idx_new_user_email`, `idx_new_user_status`, `idx_new_user_created`
**Size**: 56 kB | **Owner**: medostel_admin_user

---

### TABLE 6: Report_History
**Purpose**: Medical report analysis and storage history
**Primary Key**: `id`
**Foreign Key**: `userId` → User_Master

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | VARCHAR(50) | PK | Unique report ID |
| `userId` | VARCHAR(100) | Not Null, FK | Report owner (references User_Master) |
| `timestamp` | TIMESTAMP | Not Null | Upload/Generation time |
| `fileName` | VARCHAR(255) | Not Null | Original file name |
| `fileType` | VARCHAR(10) | Not Null | pdf/image/doc/docx |
| `reportType` | VARCHAR(100) | | Report type (e.g., Blood Test) |
| `inferredDiagnosis` | TEXT | | AI inferred diagnosis |
| `pdfUrl` | TEXT | | URL to generated PDF |
| `bucketLocation` | VARCHAR(255) | | Storage bucket path |
| `jsonData` | JSONB | | Full analysis in JSON |
| `status` | VARCHAR(20) | Default 'Pending' | Pending/Processing/Completed/Error |
| `createdDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Creation timestamp |
| `updatedDate` | TIMESTAMP | Default CURRENT_TIMESTAMP | Update timestamp |

**Indexes**: `idx_report_user_id`, `idx_report_timestamp`, `idx_report_type`, `idx_report_status`, `idx_report_created`
**Size**: 56 kB | **Owner**: medostel_admin_user

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

**Last Updated**: 2026-02-28
**Instance**: medostel-ai-assistant-pgdev-instance
**Status**: RUNNABLE ✅
**Environment**: Development/Pre-Production
