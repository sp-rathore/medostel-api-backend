# Medostel API Development Agent

## Overview

This document outlines the API development strategy, architecture, and implementation guidelines for the Medostel AI Healthcare Assistant platform.

---

## API Architecture

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Python | 3.11+ | API server runtime |
| **Framework** | FastAPI | Latest | RESTful API framework |
| **Database** | PostgreSQL | 18 | Data persistence |
| **Authentication** | JWT/OAuth2 | Latest | Secure authentication |
| **Documentation** | OpenAPI/Swagger | 3.0 | API documentation |
| **Deployment** | Google Cloud Run | Latest | Serverless deployment |

---

## Database Connection

### Connection Details

| Property | Value |
|----------|-------|
| **Host** | 35.244.27.232 |
| **Port** | 5432 |
| **Database** | medostel |
| **Region** | asia-south1 (Mumbai) |
| **Instance** | medostel-ai-assistant-pgdev-instance |
| **Status** | 🟢 RUNNABLE |

### Authentication

**Admin User** (Development/Migration):
```
Username: medostel_admin_user
Password: Iag2bMi@0@6aA
Privileges: Full administrative access
```

**API User** (Application):
```
Username: medostel_api_user
Password: Iag2bMi@0@6aD
Privileges: SELECT, INSERT, UPDATE, DELETE (tables only)
```

### Connection Strings

```python
# Admin Connection
postgresql://medostel_admin_user:Iag2bMi@0@6aA@35.244.27.232:5432/medostel

# API Connection (Recommended for application)
postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel

# Connection with Cloud SQL Proxy
cloud_sql_proxy -instances=gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance=tcp:5432
```

**See**: `Development/DevOps Development/DBA/DBA.md` for complete database documentation

---

## API Endpoints Structure

### User Management

#### 1. User Registration
```
POST /api/v1/users/register
```
- Request: User details from new_user_request table
- Response: Registration status and request ID
- Auth: Public (no authentication required)

#### 2. User Login
```
POST /api/v1/auth/login
```
- Request: Username, password
- Response: JWT token, user details
- Auth: Public

#### 3. Get User Profile
```
GET /api/v1/users/{userId}
```
- Response: User profile from user_master table
- Auth: Required (JWT token)

#### 4. Update User Profile
```
PUT /api/v1/users/{userId}
```
- Request: Updated user information
- Response: Updated user profile
- Auth: Required (JWT token)

### Role Management

#### 1. Get All Roles
```
GET /api/v1/roles
```
- Response: List of user roles from user_role_master
- Auth: Required (Admin only)

#### 2. Create Role
```
POST /api/v1/roles
```
- Request: Role name, permissions
- Response: Created role details
- Auth: Required (Admin only)

### Report Management

#### 1. Upload Report
```
POST /api/v1/reports/upload
```
- Request: File (PDF/Image/Doc)
- Response: Report ID, processing status
- Auth: Required (JWT token)

#### 2. Get Report History
```
GET /api/v1/reports/history/{userId}
```
- Response: List of reports from report_history table
- Auth: Required (JWT token)

#### 3. Get Report Details
```
GET /api/v1/reports/{reportId}
```
- Response: Report details including analysis
- Auth: Required (JWT token)

### Geographic Data

#### 1. Get States
```
GET /api/v1/locations/states
```
- Response: List of states from state_city_pincode_master
- Auth: Not required

#### 2. Get Cities by State
```
GET /api/v1/locations/states/{stateId}/cities
```
- Response: Cities for specified state
- Auth: Not required

#### 3. Get Pin Codes
```
GET /api/v1/locations/pincodes/{pinCode}
```
- Response: Location details for pin code
- Auth: Not required

---

## Complete API Specifications for All Tables

### Summary Table: All 12 APIs

| # | Table | API Type | Method | Endpoint | Purpose |
|---|-------|----------|--------|----------|---------|
| 1 | User_Role_Master | SELECT | GET | `/api/v1/roles/all` | Retrieve all user roles |
| 2 | User_Role_Master | CRUD | POST/PUT/DELETE | `/api/v1/roles` | Create, update, delete roles |
| 3 | State_City_PinCode_Master | SELECT | GET | `/api/v1/locations/all` | Retrieve all geographic data |
| 4 | State_City_PinCode_Master | CRUD | POST/PUT/DELETE | `/api/v1/locations` | Manage geographic data |
| 5 | User_Master | SELECT | GET | `/api/v1/users/all` | Retrieve all user profiles |
| 6 | User_Master | CRUD | POST/PUT/DELETE | `/api/v1/users` | Manage user profiles |
| 7 | User_Login | SELECT | GET | `/api/v1/auth/users` | Retrieve user login records |
| 8 | User_Login | CRUD | POST/PUT/DELETE | `/api/v1/auth/credentials` | Manage login credentials |
| 9 | New_User_Request | SELECT | GET | `/api/v1/requests/all` | Retrieve registration requests |
| 10 | New_User_Request | CRUD | POST/PUT/DELETE | `/api/v1/requests` | Manage registration requests |
| 11 | Report_History | SELECT | GET | `/api/v1/reports/all` | Retrieve all report records |
| 12 | Report_History | CRUD | POST/PUT/DELETE | `/api/v1/reports` | Manage report records |

---

## System Roles Reference

### All Available Roles (8 Total)

These are the user roles available in the system. Use the **Role ID** when making API requests.

| # | Role ID | Role Name | Description |
|---|---------|-----------|-------------|
| 1 | ADMIN | System Administrator | Full system access and database management |
| 2 | DOCTOR | Doctor/Physician | Can view and manage patient records and create medical reports |
| 3 | HOSPITAL | Hospital | Hospital administrator - manages hospital operations and staff |
| 4 | NURSE | Nurse | Can assist with patient records, blood work, and vitals |
| 5 | PARTNER | Sales Partner | Sales and marketing partner - manages partnerships and revenue |
| 6 | PATIENT | Patient | Can view own medical reports and health history |
| 7 | RECEPTION | Reception Staff | Can manage appointments, check-in/check-out, and scheduling |
| 8 | TECHNICIAN | Lab Technician | Can create and upload laboratory test reports and results |

**Usage Example in API Requests:**
```json
{
  "roleId": "DOCTOR",
  "roleName": "Doctor/Physician",
  "status": "Active",
  "comments": "Can view and manage patient records and create medical reports"
}
```

---

### API 1: User_Role_Master - SELECT Operations

**Endpoint**: `GET /api/v1/roles/all`
**Purpose**: Retrieve user roles with flexible filtering options
**Authentication**: Required (Admin/Doctor)
**Rate Limit**: 100 requests/minute

#### Overview
This endpoint supports **three different request scenarios**:

1. **Fetch by Role ID**: Get a specific role by ID (case-insensitive)
2. **Fetch by Status**: Get all roles with a specific status
3. **Fetch All**: Get all roles from the table irrespective of status

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `roleId` | string | No | Fetch specific role by ID (automatically converted to UPPERCASE) |
| `status` | string | No | Filter by status: Active, Inactive, Pending |
| `limit` | integer | No | Limit results (default: 100, max: 1000) |
| `offset` | integer | No | Pagination offset (default: 0) |

---

#### **Scenario 1: Fetch by Role ID (Case-Insensitive)**

##### Request
```bash
# Request with lowercase roleId - will be converted to ADMIN
curl -X GET "http://localhost:8000/api/v1/roles/all?roleId=admin" \
  -H "Authorization: Bearer <jwt_token>"

# Or with mixed case - will be converted to DOCTOR
curl -X GET "http://localhost:8000/api/v1/roles/all?roleId=DoCtOr" \
  -H "Authorization: Bearer <jwt_token>"
```

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Role 'ADMIN' retrieved successfully",
  "data": {
    "count": 1,
    "scenario": "Fetch by Role ID",
    "roles": [
      {
        "roleId": "ADMIN",
        "roleName": "System Administrator",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Full system access and database management"
      }
    ]
  },
  "timestamp": "2026-03-01T16:00:00Z"
}
```

##### Response (404 - Not Found)
```json
{
  "status": "error",
  "code": 404,
  "message": "Role with ID 'INVALID' not found",
  "timestamp": "2026-03-01T16:00:00Z"
}
```

---

#### **Scenario 2: Fetch by Status**

##### Request
```bash
# Fetch all ACTIVE roles
curl -X GET "http://localhost:8000/api/v1/roles/all?status=Active" \
  -H "Authorization: Bearer <jwt_token>"

# Fetch with pagination
curl -X GET "http://localhost:8000/api/v1/roles/all?status=Active&limit=5&offset=0" \
  -H "Authorization: Bearer <jwt_token>"
```

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Retrieved 8 role(s) with status 'Active'",
  "data": {
    "count": 8,
    "scenario": "Fetch all roles with status filter",
    "roles": [
      {
        "roleId": "ADMIN",
        "roleName": "System Administrator",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Full system access and database management"
      },
      {
        "roleId": "DOCTOR",
        "roleName": "Doctor/Physician",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can view and manage patient records and create medical reports"
      },
      {
        "roleId": "HOSPITAL",
        "roleName": "Hospital",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Hospital administrator - manages hospital operations and staff"
      },
      {
        "roleId": "NURSE",
        "roleName": "Nurse",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can assist with patient records, blood work, and vitals"
      },
      {
        "roleId": "PARTNER",
        "roleName": "Sales Partner",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Sales and marketing partner - manages partnerships and revenue"
      }
    ]
  },
  "timestamp": "2026-03-01T16:00:00Z"
}
```

---

#### **Scenario 3: Fetch All Roles (Irrespective of Status)**

##### Request
```bash
# Fetch all roles from User_Role_Master table
curl -X GET "http://localhost:8000/api/v1/roles/all" \
  -H "Authorization: Bearer <jwt_token>"

# With pagination
curl -X GET "http://localhost:8000/api/v1/roles/all?limit=10&offset=0" \
  -H "Authorization: Bearer <jwt_token>"
```

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Retrieved all roles from User_Role_Master",
  "data": {
    "count": 8,
    "scenario": "Fetch all roles",
    "roles": [
      {
        "roleId": "ADMIN",
        "roleName": "System Administrator",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Full system access and database management"
      },
      {
        "roleId": "DOCTOR",
        "roleName": "Doctor/Physician",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can view and manage patient records and create medical reports"
      },
      {
        "roleId": "HOSPITAL",
        "roleName": "Hospital",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Hospital administrator - manages hospital operations and staff"
      },
      {
        "roleId": "NURSE",
        "roleName": "Nurse",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can assist with patient records, blood work, and vitals"
      },
      {
        "roleId": "PARTNER",
        "roleName": "Sales Partner",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Sales and marketing partner - manages partnerships and revenue"
      },
      {
        "roleId": "PATIENT",
        "roleName": "Patient",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can view own medical reports and health history"
      },
      {
        "roleId": "RECEPTION",
        "roleName": "Reception Staff",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can manage appointments, check-in/check-out, and scheduling"
      },
      {
        "roleId": "TECHNICIAN",
        "roleName": "Lab Technician",
        "status": "Active",
        "createdDate": "2026-02-28",
        "updatedDate": "2026-02-28",
        "comments": "Can create and upload laboratory test reports and results"
      }
    ]
  },
  "timestamp": "2026-03-01T16:00:00Z"
}
```

---

### API 2: User_Role_Master - CRUD Operations

**Purpose**: Insert and Update user roles (No Delete operation)
**Authentication**: Required (Admin only)

---

#### **Scenario A: Insert New Role (POST)**

**Endpoint**: `POST /api/v1/roles`

##### Request Description
Insert a new role into the User_Role_Master table with the following required fields:

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `roleId` | string | Yes | Max 10 chars, unique, uppercase | Unique role identifier |
| `roleName` | string | Yes | Max 50 chars, unique | Human-readable role name |
| `status` | string | Yes | Active, Inactive, or Closed | Role activation status |
| `comments` | string | No | Max 250 chars | Optional description |

**System-managed fields (AUTO-POPULATED):**
- `createdDate`: Set to current system timestamp
- `updatedDate`: Set to current system timestamp

##### Request Example
```bash
curl -X POST http://localhost:8000/api/v1/roles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "roleId": "ADMIN",
    "roleName": "System Administrator",
    "status": "Active",
    "comments": "Full system access and database management"
  }'
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "Role created successfully",
  "data": {
    "scenario": "Insert new role",
    "info": "createdDate and updatedDate set to current system timestamp",
    "role": {
      "roleId": "ADMIN",
      "roleName": "System Administrator",
      "status": "Active",
      "createdDate": "2026-03-01",
      "updatedDate": "2026-03-01",
      "comments": "Full system access and database management"
    }
  },
  "timestamp": "2026-03-01T16:00:00Z"
}
```

##### Response (400 - Bad Request - Invalid Status)
```json
{
  "status": "error",
  "code": 400,
  "message": "Status must be one of: Active, Inactive, Closed",
  "timestamp": "2026-03-01T16:00:00Z"
}
```

##### Response (409 - Conflict - Role Already Exists)
```json
{
  "status": "error",
  "code": 409,
  "message": "Role 'ADMIN' already exists",
  "timestamp": "2026-03-01T16:00:00Z"
}
```

---

#### **Scenario B: Update Role Status (PUT)**

**Endpoint**: `PUT /api/v1/roles/{roleId}`

##### Request Description
Update the status of an existing role. This endpoint **ONLY** updates the status field.

**URL Parameter:**
- `roleId`: The role ID to update (will be converted to uppercase automatically)

**Input Required:**
- `status`: New status value (must be one of: Active, Inactive, or Closed)

**System-managed fields:**
- `updatedDate`: Automatically set to current system timestamp
- Other fields (roleId, roleName, comments): **CANNOT be modified** through this endpoint

##### Request Example
```bash
# Update DOCTOR role status from Active to Inactive
curl -X PUT http://localhost:8000/api/v1/roles/doctor \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "status": "Inactive"
  }'
```

##### Response (200 - Updated)
```json
{
  "status": "success",
  "code": 200,
  "message": "Role 'DOCTOR' status updated to 'Inactive' successfully",
  "data": {
    "scenario": "Update role status",
    "info": "updatedDate set to current system timestamp. Other fields cannot be modified.",
    "role": {
      "roleId": "DOCTOR",
      "roleName": "Doctor/Physician",
      "status": "Inactive",
      "createdDate": "2026-02-28",
      "updatedDate": "2026-03-01T16:15:00Z",
      "comments": "Can view and manage patient records and create medical reports"
    }
  },
  "timestamp": "2026-03-01T16:00:00Z"
}
```

##### Response (400 - Bad Request - Invalid Status)
```json
{
  "status": "error",
  "code": 400,
  "message": "Status must be one of: Active, Inactive, Closed. Received: 'Invalid'",
  "timestamp": "2026-03-01T16:00:00Z"
}
```

##### Response (400 - Bad Request - Missing Status Field)
```json
{
  "status": "error",
  "code": 400,
  "message": "Request body must contain 'status' field",
  "timestamp": "2026-03-01T16:00:00Z"
}
```

##### Response (404 - Not Found)
```json
{
  "status": "error",
  "code": 404,
  "message": "Role 'INVALID' not found",
  "timestamp": "2026-03-01T16:00:00Z"
}
```

---

#### **Note: No Delete Operation**

The `/api/v1/roles` endpoint does **NOT** support DELETE operations. Roles can only be managed through:
```json
{
  "status": "success",
  "code": 204,
  "message": "Role deleted successfully",
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

### API 3: State_City_PinCode_Master - SELECT Operations

**Endpoint**: `GET /api/v1/locations/all`
**Purpose**: Retrieve geographic data (read-only)
**Authentication**: Not required (Public)
**Rate Limit**: 200 requests/minute

#### Request
```bash
curl -X GET "http://localhost:8000/api/v1/locations/all?country=India&status=Active" \
  -H "Accept: application/json"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | No | Filter by country (default: India) |
| `status` | string | No | Filter by status: Active, Inactive |
| `stateId` | string | No | Filter by state ID |
| `limit` | integer | No | Limit results (default: 100) |
| `offset` | integer | No | Pagination offset |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Geographic data retrieved successfully",
  "data": {
    "total": 125,
    "count": 50,
    "locations": [
      {
        "id": 1,
        "stateId": "MH",
        "stateName": "Maharashtra",
        "cityId": "MUM",
        "cityName": "Mumbai",
        "pinCode": "400001",
        "countryName": "India",
        "status": "Active",
        "createdDate": "2026-02-28T10:00:00Z",
        "updatedDate": "2026-02-28T10:00:00Z"
      }
    ]
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

### API 4: State_City_PinCode_Master - CRUD Operations

**Purpose**: Create, Update, Delete geographic data

#### A. Create Location
**Endpoint**: `POST /api/v1/locations`
**Authentication**: Required (Admin only)

##### Request Body
```json
{
  "stateId": "UP",
  "stateName": "Uttar Pradesh",
  "cityId": "LKH",
  "cityName": "Lucknow",
  "pinCode": "226001",
  "countryName": "India",
  "status": "Active"
}
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "Location created successfully",
  "data": {
    "id": 126,
    "stateId": "UP",
    "stateName": "Uttar Pradesh",
    "cityId": "LKH",
    "cityName": "Lucknow",
    "pinCode": "226001",
    "countryName": "India",
    "status": "Active",
    "createdDate": "2026-02-28T16:00:00Z"
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

#### B. Update Location
**Endpoint**: `PUT /api/v1/locations/{id}`
**Authentication**: Required (Admin only)

##### Request
```json
{
  "status": "Inactive"
}
```

#### C. Delete Location
**Endpoint**: `DELETE /api/v1/locations/{id}`
**Authentication**: Required (Admin only)

---

### API 5: User_Master - SELECT Operations

**Endpoint**: `GET /api/v1/users/all`
**Purpose**: Retrieve all user profiles (read-only)
**Authentication**: Required (Admin/Doctor)
**Rate Limit**: 100 requests/minute

#### Request
```bash
curl -X GET "http://localhost:8000/api/v1/users/all?status=Active&limit=10" \
  -H "Authorization: Bearer <jwt_token>"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter by status: Active, Inactive |
| `currentRole` | string | No | Filter by role |
| `limit` | integer | No | Limit results (default: 100) |
| `offset` | integer | No | Pagination offset |
| `sort` | string | No | Sort field: firstName, createdDate |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Users retrieved successfully",
  "data": {
    "total": 45,
    "count": 10,
    "users": [
      {
        "userId": "john.doe@medostel.com",
        "firstName": "John",
        "lastName": "Doe",
        "currentRole": "Doctor",
        "organisation": "City Hospital",
        "emailId": "john.doe@medostel.com",
        "mobileNumber": "+919876543210",
        "stateName": "Maharashtra",
        "cityName": "Mumbai",
        "pinCode": "400001",
        "status": "Active",
        "createdDate": "2026-02-28T10:00:00Z"
      }
    ]
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

### API 6: User_Master - CRUD Operations

**Purpose**: Create, Update, Delete user profiles

#### A. Create User Profile
**Endpoint**: `POST /api/v1/users`
**Authentication**: Required (Admin only) or Self-registration

##### Request Body
```json
{
  "userId": "jane.smith@medostel.com",
  "firstName": "Jane",
  "lastName": "Smith",
  "currentRole": "Patient",
  "organisation": "Self",
  "emailId": "jane.smith@medostel.com",
  "mobileNumber": "+919876543211",
  "address1": "123 Health Street",
  "address2": "Apt 4",
  "stateName": "Maharashtra",
  "cityName": "Mumbai",
  "pinCode": "400001",
  "status": "Active"
}
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "User profile created successfully",
  "data": {
    "userId": "jane.smith@medostel.com",
    "firstName": "Jane",
    "lastName": "Smith",
    "currentRole": "Patient",
    "createdDate": "2026-02-28T16:00:00Z"
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

#### B. Update User Profile
**Endpoint**: `PUT /api/v1/users/{userId}`
**Authentication**: Required (Admin or Self)

##### Request Body
```json
{
  "firstName": "Jane",
  "lastName": "Smith-Johnson",
  "organisation": "City Medical Center"
}
```

#### C. Delete User Profile
**Endpoint**: `DELETE /api/v1/users/{userId}`
**Authentication**: Required (Admin only)

---

### API 7: User_Login - SELECT Operations

**Endpoint**: `GET /api/v1/auth/users`
**Purpose**: Retrieve user login records (read-only)
**Authentication**: Required (Admin only)
**Rate Limit**: 50 requests/minute

#### Request
```bash
curl -X GET "http://localhost:8000/api/v1/auth/users?isActive=true" \
  -H "Authorization: Bearer <jwt_token>"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `isActive` | boolean | No | Filter by active status |
| `roleId` | string | No | Filter by role ID |
| `limit` | integer | No | Limit results (default: 50) |
| `offset` | integer | No | Pagination offset |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "User login records retrieved successfully",
  "data": {
    "total": 20,
    "count": 10,
    "loginRecords": [
      {
        "userId": "john.doe@medostel.com",
        "username": "john.doe@medostel.com",
        "mobilePhone": "+919876543210",
        "roleId": "DOCTOR",
        "isActive": true,
        "lastLoginAt": "2026-02-28T15:30:00Z",
        "passwordLastChangedAt": "2026-02-20T10:00:00Z",
        "createdAt": "2026-02-10T08:00:00Z"
      }
    ]
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

### API 8: User_Login - CRUD Operations

**Purpose**: Manage user login credentials

#### A. Create Login Credentials
**Endpoint**: `POST /api/v1/auth/credentials`
**Authentication**: Required (Admin only) or Self-registration

##### Request Body
```json
{
  "userId": "jane.smith@medostel.com",
  "username": "jane.smith@medostel.com",
  "password": "SecurePassword@123",
  "roleId": "PATIENT"
}
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "Login credentials created successfully",
  "data": {
    "userId": "jane.smith@medostel.com",
    "username": "jane.smith@medostel.com",
    "isActive": true,
    "createdAt": "2026-02-28T16:00:00Z"
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

#### B. Update Login Credentials
**Endpoint**: `PUT /api/v1/auth/credentials/{userId}`
**Authentication**: Required (Self or Admin)

##### Request Body
```json
{
  "password": "NewSecurePassword@123",
  "isActive": true
}
```

#### C. Delete Login Credentials
**Endpoint**: `DELETE /api/v1/auth/credentials/{userId}`
**Authentication**: Required (Admin only)

---

### API 9: New_User_Request - SELECT Operations

**Endpoint**: `GET /api/v1/requests/all`
**Purpose**: Retrieve user registration requests (read-only)
**Authentication**: Required (Admin/Doctor)
**Rate Limit**: 100 requests/minute

#### Request
```bash
curl -X GET "http://localhost:8000/api/v1/requests/all?requestStatus=Pending" \
  -H "Authorization: Bearer <jwt_token>"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `requestStatus` | string | No | Filter: Pending, Approved, Rejected |
| `currentRole` | string | No | Filter by requested role |
| `limit` | integer | No | Limit results (default: 100) |
| `offset` | integer | No | Pagination offset |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Registration requests retrieved successfully",
  "data": {
    "total": 15,
    "count": 10,
    "requests": [
      {
        "requestId": "REQ20260228001",
        "userName": "robert.kumar@medostel.com",
        "firstName": "Robert",
        "lastName": "Kumar",
        "currentRole": "Patient",
        "emailId": "robert.kumar@medostel.com",
        "mobileNumber": "+919876543212",
        "requestStatus": "Pending",
        "createdDate": "2026-02-28T12:00:00Z",
        "approvedBy": null,
        "approvalRemarks": null
      }
    ]
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

### API 10: New_User_Request - CRUD Operations

**Purpose**: Manage user registration requests

#### A. Create Registration Request
**Endpoint**: `POST /api/v1/requests`
**Authentication**: Not required (Public)

##### Request Body
```json
{
  "requestId": "REQ20260228002",
  "userName": "alice.green@medostel.com",
  "firstName": "Alice",
  "lastName": "Green",
  "currentRole": "Doctor",
  "organisation": "Metro Hospital",
  "emailId": "alice.green@medostel.com",
  "mobileNumber": "+919876543213",
  "address1": "456 Medical Avenue",
  "stateName": "Maharashtra",
  "cityName": "Pune",
  "pinCode": "411001",
  "requestStatus": "Pending"
}
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "Registration request submitted successfully",
  "data": {
    "requestId": "REQ20260228002",
    "userName": "alice.green@medostel.com",
    "firstName": "Alice",
    "lastName": "Green",
    "requestStatus": "Pending",
    "createdDate": "2026-02-28T16:00:00Z"
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

#### B. Update Registration Request
**Endpoint**: `PUT /api/v1/requests/{requestId}`
**Authentication**: Required (Admin only)

##### Request Body
```json
{
  "requestStatus": "Approved",
  "approvedBy": "admin@medostel.com",
  "approvalRemarks": "Verified doctor credentials"
}
```

#### C. Delete Registration Request
**Endpoint**: `DELETE /api/v1/requests/{requestId}`
**Authentication**: Required (Admin only)

---

### API 11: Report_History - SELECT Operations

**Endpoint**: `GET /api/v1/reports/all`
**Purpose**: Retrieve medical report records (read-only)
**Authentication**: Required (Admin/Doctor)
**Rate Limit**: 100 requests/minute

#### Request
```bash
curl -X GET "http://localhost:8000/api/v1/reports/all?status=Completed&reportType=Blood Test" \
  -H "Authorization: Bearer <jwt_token>"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: Pending, Processing, Completed, Error |
| `reportType` | string | No | Filter by report type |
| `userId` | string | No | Filter by user ID |
| `limit` | integer | No | Limit results (default: 100) |
| `offset` | integer | No | Pagination offset |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Reports retrieved successfully",
  "data": {
    "total": 120,
    "count": 25,
    "reports": [
      {
        "id": "RPT20260228001",
        "userId": "john.doe@medostel.com",
        "fileName": "blood_test_report.pdf",
        "fileType": "pdf",
        "reportType": "Blood Test",
        "status": "Completed",
        "inferredDiagnosis": "Normal blood count",
        "pdfUrl": "https://storage.googleapis.com/...",
        "bucketLocation": "gs://medostel-reports/...",
        "timestamp": "2026-02-28T14:00:00Z",
        "createdDate": "2026-02-28T14:00:00Z"
      }
    ]
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

### API 12: Report_History - CRUD Operations

**Purpose**: Manage medical report records

#### A. Create Report Record
**Endpoint**: `POST /api/v1/reports`
**Authentication**: Required (Doctor/Self)

##### Request Body
```json
{
  "id": "RPT20260228002",
  "userId": "jane.smith@medostel.com",
  "fileName": "xray_chest_2026.pdf",
  "fileType": "pdf",
  "reportType": "X-Ray",
  "status": "Processing",
  "pdfUrl": "https://storage.googleapis.com/medostel-reports/xray.pdf",
  "bucketLocation": "gs://medostel-reports/xray.pdf"
}
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "Report created successfully",
  "data": {
    "id": "RPT20260228002",
    "userId": "jane.smith@medostel.com",
    "fileName": "xray_chest_2026.pdf",
    "status": "Processing",
    "createdDate": "2026-02-28T16:00:00Z"
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

#### B. Update Report Record
**Endpoint**: `PUT /api/v1/reports/{reportId}`
**Authentication**: Required (Doctor/Admin)

##### Request Body
```json
{
  "status": "Completed",
  "inferredDiagnosis": "Chest appears normal, no abnormalities detected",
  "jsonData": {
    "diagnosis": "Normal",
    "confidence": 0.95,
    "findings": []
  }
}
```

#### C. Delete Report Record
**Endpoint**: `DELETE /api/v1/reports/{reportId}`
**Authentication**: Required (Admin or Report Owner)

---

## Database Tables & Relationships

### 1. user_role_master
**Purpose**: Store user roles and permissions
```
Columns: roleId (PK), roleName, status, createdDate, updatedDate, comments
Relationships: Referenced by user_master, user_login
```

### 2. state_city_pincode_master
**Purpose**: Geographic location data
```
Columns: id (PK), stateId, stateName, cityName, cityId, pinCode, countryName, status, timestamps
Relationships: Referenced by user_master, new_user_request
```

### 3. user_master
**Purpose**: Core user profile data
```
Columns: userId (PK), firstName, lastName, currentRole, organisation, emailId, mobileNumber, address, location, status, timestamps
Relationships: FK to user_role_master, Referenced by user_login, report_history
```

### 4. user_login
**Purpose**: Authentication and login credentials
```
Columns: userId (PK/FK), username, passwordHash, mobilePhone, roleId, isActive, login timestamps
Relationships: FK to user_master, user_role_master
```

### 5. new_user_request
**Purpose**: Staging table for new user registration
```
Columns: requestId (PK), userName, firstName, lastName, currentRole, organisation, emailId, mobileNumber, address, location, requestStatus, timestamps, approvalDetails
Relationships: None (independent staging table)
```

### 6. report_history
**Purpose**: Medical report analysis and storage
```
Columns: id (PK), userId (FK), timestamp, fileName, fileType, reportType, inferredDiagnosis, pdfUrl, bucketLocation, jsonData, status, timestamps
Relationships: FK to user_master
```

---

## API Response Format

### Success Response (2xx)
```json
{
  "status": "success",
  "code": 200,
  "message": "Operation completed successfully",
  "data": {
    // Response payload
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

### Error Response (4xx, 5xx)
```json
{
  "status": "error",
  "code": 400,
  "message": "Description of error",
  "error": "ERROR_CODE",
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

## Authentication & Authorization

### JWT Token Structure
```
Header: Authorization: Bearer <token>
Payload: {
  "sub": "userId",
  "email": "user@example.com",
  "role": "user_role",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### Role-Based Access Control (RBAC)

| Role | Endpoints | Permissions |
|------|-----------|-------------|
| **Admin** | All | Full access to all resources |
| **Doctor** | Users, Reports, Profiles | Read/write patient reports |
| **Patient** | Own profile, Own reports | Read own data, upload reports |
| **Public** | Registration, Login | Register new account, login |

---

## Security Considerations

### Authentication
- ✅ Use JWT tokens for API authentication
- ✅ Implement token refresh mechanism
- ✅ Store tokens in HTTP-only cookies (not localStorage)
- ✅ Use 60-minute token expiration

### Authorization
- ✅ Implement role-based access control (RBAC)
- ✅ Validate user permissions for each endpoint
- ✅ Log all access attempts

### Data Protection
- ✅ Hash passwords using bcrypt (min 12 rounds)
- ✅ Encrypt sensitive data in transit (HTTPS/TLS)
- ✅ Implement rate limiting (100 requests/minute per user)
- ✅ Validate and sanitize all inputs

### Audit Logging
- ✅ Log all authentication attempts
- ✅ Log all data modifications
- ✅ Log all administrative actions
- ✅ Implement audit retention policy (90 days)

---

## Error Handling

### Standard Error Codes

| Code | Message | HTTP Status |
|------|---------|------------|
| AUTH_001 | Invalid credentials | 401 |
| AUTH_002 | Token expired | 401 |
| AUTH_003 | Insufficient permissions | 403 |
| USER_001 | User not found | 404 |
| USER_002 | Email already exists | 409 |
| USER_003 | Invalid input data | 400 |
| DB_001 | Database connection error | 503 |
| FILE_001 | Invalid file type | 400 |
| FILE_002 | File size exceeds limit | 413 |

---

## Development Workflow

### 1. Setup
```bash
# Install dependencies
pip install fastapi uvicorn psycopg2-binary pydantic python-jose[cryptography]

# Create virtual environment
python -m venv venv
source venv/bin/activate
```

### 2. Create API Endpoints
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import psycopg2
from psycopg2.pool import SimpleConnectionPool

app = FastAPI(
    title="Medostel API",
    description="Healthcare AI Assistant API",
    version="1.0.0"
)

# Database connection pool
db_pool = SimpleConnectionPool(
    1, 20,
    host="35.244.27.232",
    port=5432,
    database="medostel",
    user="medostel_api_user",
    password="Iag2bMi@0@6aD"
)

# Database dependency
def get_db():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

# Example SELECT endpoint
@app.get("/api/v1/users/all")
async def get_all_users(limit: int = 100, offset: int = 0, db=Depends(get_db)):
    """Retrieve all user profiles"""
    cursor = db.cursor()
    try:
        query = "SELECT * FROM user_master LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        users = cursor.fetchall()
        return {
            "status": "success",
            "code": 200,
            "data": {"users": users},
            "timestamp": "2026-02-28T16:00:00Z"
        }
    finally:
        cursor.close()

# Example CRUD endpoint
@app.post("/api/v1/users")
async def create_user(user_data: dict, db=Depends(get_db)):
    """Create new user profile"""
    cursor = db.cursor()
    try:
        query = """
            INSERT INTO user_master
            (userId, firstName, lastName, currentRole, emailId, mobileNumber, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        cursor.execute(query, (
            user_data['userId'],
            user_data['firstName'],
            user_data['lastName'],
            user_data['currentRole'],
            user_data['emailId'],
            user_data['mobileNumber'],
            'Active'
        ))
        db.commit()
        new_user = cursor.fetchone()
        return {
            "status": "success",
            "code": 201,
            "data": new_user,
            "timestamp": "2026-02-28T16:00:00Z"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
```

### 3. Testing
```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# API documentation
http://localhost:8000/docs
```

### 4. Deployment
```bash
# Deploy to Cloud Run
gcloud run deploy medostel-api \
  --source . \
  --platform managed \
  --region asia-south1 \
  --project gen-lang-client-0064186167
```

---

## Performance Optimization

### Indexing
- ✅ All tables have performance indexes created
- ✅ Total of 35 indexes optimizing common queries
- ✅ Foreign key columns indexed for joins

### Query Optimization
- ✅ Use parameterized queries to prevent SQL injection
- ✅ Implement connection pooling
- ✅ Cache frequently accessed data
- ✅ Implement pagination for large result sets

### Caching Strategy
- ✅ Cache location data (states, cities, pin codes)
- ✅ Cache user roles (frequently referenced)
- ✅ Cache duration: 1 hour for static data
- ✅ Use Redis for distributed caching

---

## Monitoring & Logging

### Metrics to Track
- Request latency (target: <200ms)
- Error rate (target: <1%)
- Database query time (target: <100ms)
- Active user count
- API endpoint usage

### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.info(f"User {userId} logged in")
logger.error(f"Database error: {error}")
logger.warning(f"Rate limit approaching for user {userId}")
```

---

## Deployment Checklist

### API Implementation
- [x] All 12 APIs designed (6 tables × 2 APIs each)
- [ ] API 1: User_Role_Master SELECT operations
- [ ] API 2: User_Role_Master CRUD operations
- [ ] API 3: State_City_PinCode_Master SELECT operations
- [ ] API 4: State_City_PinCode_Master CRUD operations
- [ ] API 5: User_Master SELECT operations
- [ ] API 6: User_Master CRUD operations
- [ ] API 7: User_Login SELECT operations
- [ ] API 8: User_Login CRUD operations
- [ ] API 9: New_User_Request SELECT operations
- [ ] API 10: New_User_Request CRUD operations
- [ ] API 11: Report_History SELECT operations
- [ ] API 12: Report_History CRUD operations

### Database & Infrastructure
- [x] Database schema verified
- [x] PostgreSQL instance running (medostel-ai-assistant-pgdev-instance)
- [x] GKE cluster operational (medostel-api-cluster)
- [x] Database connection tested

### Security & Quality
- [ ] Authentication/authorization implemented (JWT)
- [ ] Error handling implemented
- [ ] Input validation implemented (Pydantic models)
- [ ] Rate limiting configured (100-200 req/min per endpoint)
- [ ] Password hashing configured (bcrypt)
- [ ] CORS configured

### Testing & Documentation
- [ ] Unit tests written (all 12 APIs)
- [ ] Integration tests written
- [ ] Endpoint tests passing (all endpoints)
- [ ] API documentation complete (Swagger/OpenAPI)
- [ ] Tests written and passing

### Operations
- [ ] Logging configured
- [ ] Monitoring configured (Cloud Monitoring)
- [ ] Alerting configured
- [ ] Security review completed
- [ ] Performance testing completed

### Deployment
- [ ] Local testing completed
- [ ] Staging deployment completed
- [ ] Cloud Run deployment setup
- [ ] Deployment to Cloud Run (asia-south1)
- [ ] Production readiness checklist

### Post-Deployment
- [ ] Backup strategy in place
- [ ] Disaster recovery tested
- [ ] Performance monitoring active
- [ ] Log aggregation active

---

## Implementation Timeline & Phases

### Phase 1: Core API Framework
**Duration**: Week 1
**Tasks**:
- Setup FastAPI project structure
- Configure database connection pooling
- Implement authentication/JWT
- Create base response models

### Phase 2: User Management APIs (Roles)
**Duration**: Week 2
**Tasks**:
- Implement API 1: User_Role_Master SELECT
- Implement API 2: User_Role_Master CRUD
- Create Pydantic models
- Write unit tests

### Phase 3: Geographic Data APIs
**Duration**: Week 2
**Tasks**:
- Implement API 3: State_City_PinCode_Master SELECT
- Implement API 4: State_City_PinCode_Master CRUD
- Add caching for geographic data
- Performance testing

### Phase 4: User Profile APIs
**Duration**: Week 3
**Tasks**:
- Implement API 5: User_Master SELECT
- Implement API 6: User_Master CRUD
- Add input validation
- Integration testing

### Phase 5: Authentication APIs
**Duration**: Week 3
**Tasks**:
- Implement API 7: User_Login SELECT
- Implement API 8: User_Login CRUD
- Add password security
- Security testing

### Phase 6: Registration Request APIs
**Duration**: Week 4
**Tasks**:
- Implement API 9: New_User_Request SELECT
- Implement API 10: New_User_Request CRUD
- Add approval workflow
- Integration testing

### Phase 7: Report Management APIs
**Duration**: Week 4
**Tasks**:
- Implement API 11: Report_History SELECT
- Implement API 12: Report_History CRUD
- Cloud Storage integration
- Performance optimization

### Phase 8: Testing & Deployment
**Duration**: Week 5
**Tasks**:
- Full integration testing
- Load testing
- Security audit
- Production deployment
- Post-deployment monitoring

---

## Next Steps (Sequential)

1. **Week 1**: Setup FastAPI project and database connection
2. **Week 2**: Implement Role Management (APIs 1-2)
3. **Week 2**: Implement Geographic Data (APIs 3-4)
4. **Week 3**: Implement User Management (APIs 5-6)
5. **Week 3**: Implement Authentication (APIs 7-8)
6. **Week 4**: Implement Registration (APIs 9-10)
7. **Week 4**: Implement Reports (APIs 11-12)
8. **Week 5**: Testing, Security Review, Deployment to GKE

---

## API Development Quick Reference

### 12 APIs Summary

| # | Table | SELECT API | CRUD API | Status |
|---|-------|-----------|----------|--------|
| 1 | User_Role_Master | `GET /api/v1/roles/all` | `POST/PUT/DELETE /api/v1/roles` | Designed |
| 2 | State_City_PinCode | `GET /api/v1/locations/all` | `POST/PUT/DELETE /api/v1/locations` | Designed |
| 3 | User_Master | `GET /api/v1/users/all` | `POST/PUT/DELETE /api/v1/users` | Designed |
| 4 | User_Login | `GET /api/v1/auth/users` | `POST/PUT/DELETE /api/v1/auth/credentials` | Designed |
| 5 | New_User_Request | `GET /api/v1/requests/all` | `POST/PUT/DELETE /api/v1/requests` | Designed |
| 6 | Report_History | `GET /api/v1/reports/all` | `POST/PUT/DELETE /api/v1/reports` | Designed |

### Key Features of All APIs
✅ **Comprehensive Error Handling** - Standard error codes for all operations
✅ **Consistent Response Format** - Unified JSON response structure
✅ **Pagination Support** - Limit and offset parameters for large datasets
✅ **Role-Based Access Control** - RBAC implemented for security
✅ **Input Validation** - Pydantic models for request validation
✅ **Rate Limiting** - Configurable per endpoint
✅ **Audit Logging** - All operations logged for compliance
✅ **Performance Optimized** - Indexes and query optimization
✅ **API Documentation** - Full Swagger/OpenAPI docs

### Related Documentation

**Infrastructure & Database:**
- Kubernetes Cluster: `Development/API Development/Kubernetes Cluster Configuration.md`
- Database Details: `Development/DevOps Development/DBA/DBA.md`
- DevOps Configuration: `Development/DevOps Development/`

**Database Connection:**
- Host: `35.244.27.232`
- Port: `5432`
- Database: `medostel`
- Instance: `medostel-ai-assistant-pgdev-instance`

**GKE Cluster:**
- Name: `medostel-api-cluster`
- Region: `asia-south1 (Mumbai)`
- Status: `RUNNING`
- Current Nodes: `4`

---

## 📚 API Repository Documentation Reference

### Complete Documentation Files

This API specification is complemented by comprehensive documentation in the API repository. All implementation guides, structure details, and setup instructions are available in the following files:

#### 1. **PROJECT_STRUCTURE.md**
**Location**: `repositories/medostel-api-backend/PROJECT_STRUCTURE.md`
**Purpose**: Detailed directory structure and module descriptions
**Contains**:
- Complete directory tree with file descriptions
- Module-by-module breakdown
- API implementation mapping table
- Configuration management details
- Development workflow steps
- Database models and ORM setup
- Testing strategy

**Use This For**: Understanding the complete project layout and how files are organized

---

#### 2. **SETUP.md**
**Location**: `repositories/medostel-api-backend/SETUP.md`
**Purpose**: Step-by-step implementation guide with code samples
**Contains**:
- Prerequisites and initial setup
- Virtual environment creation
- Environment variables configuration
- Core configuration file samples (config.py, constants.py)
- Database connection setup code
- Complete Pydantic schema examples for all 7 schema files
- Service layer implementation examples
- Route file implementation examples
- Main application updates
- Development server startup
- Docker and deployment instructions
- Implementation checklist

**Use This For**: Actually implementing the 12 APIs following step-by-step instructions with code examples

---

#### 3. **API_STRUCTURE_GUIDE.md**
**Location**: `repositories/medostel-api-backend/API_STRUCTURE_GUIDE.md`
**Purpose**: Visual architecture and data flow diagrams
**Contains**:
- ASCII directory tree visualization
- Complete 12 APIs implementation map table
- Data flow architecture diagram
- File organization by functionality
- Development phases (Weeks 1-5)
- Key implementation points for routes and services
- Testing strategy visualization
- Deployment architecture diagram
- Quick command reference
- Database connection information

**Use This For**: Understanding the architecture, data flow, and visual organization of components

---

#### 4. **REPOSITORY_SUMMARY.md**
**Location**: `repositories/medostel-api-backend/REPOSITORY_SUMMARY.md`
**Purpose**: Quick reference guide with summary information
**Contains**:
- Technology stack details
- Project structure at a glance
- Key files and their purpose
- 12 APIs breakdown with checklist
- Documentation files overview
- Database connection information
- Architecture overview diagram
- Development workflow timeline
- Getting started guide
- Implementation priorities
- Repository statistics
- Related documentation links
- File creation checklist

**Use This For**: Quick lookup of information, implementation priorities, and overall project status

---

### Repository Path

```
/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/

Key Files:
├── PROJECT_STRUCTURE.md        ← Detailed structure & modules
├── SETUP.md                    ← Implementation guide with code
├── API_STRUCTURE_GUIDE.md      ← Visual architecture & diagrams
├── REPOSITORY_SUMMARY.md       ← Quick reference & checklist
├── README.md                   ← Project overview
├── app/                        ← Application code (to implement)
├── tests/                      ← Test suite (to implement)
└── requirements.txt            ← Dependencies (✓ complete)
```

---

## 📖 Documentation Usage Guide

### For First-Time Setup
**Follow This Order**:
1. Read **REPOSITORY_SUMMARY.md** - Get overview
2. Read **SETUP.md** (Step 1-2) - Setup environment
3. Read **PROJECT_STRUCTURE.md** - Understand structure
4. Continue **SETUP.md** - Implement step-by-step

### For Understanding Architecture
**Use These Files**:
1. **API_STRUCTURE_GUIDE.md** - See data flow diagrams
2. **PROJECT_STRUCTURE.md** - Understand module relationships
3. This **API Development agent.md** - API specifications

### For Implementation
**Reference**:
1. **SETUP.md** - Code templates and examples
2. **PROJECT_STRUCTURE.md** - Module descriptions
3. This **API Development agent.md** - API specifications

### For Quick Lookup
**Use**:
1. **REPOSITORY_SUMMARY.md** - Statistics, checklist, status
2. **API_STRUCTURE_GUIDE.md** - Visual reference

---

## 🔗 Cross-References Between Documents

### From This File (API Development agent.md)
→ For implementation details: See **SETUP.md**
→ For project structure: See **PROJECT_STRUCTURE.md**
→ For architecture diagrams: See **API_STRUCTURE_GUIDE.md**
→ For quick reference: See **REPOSITORY_SUMMARY.md**

### Database & Infrastructure
→ For PostgreSQL details: See `Development/DevOps Development/DBA/DBA.md`
→ For GKE cluster info: See `Development/API Development/Kubernetes Cluster Configuration.md`

---

## 📊 12 APIs Implementation Checklist (With Documentation Reference)

For each of the 12 APIs, follow these documentation references:

| API # | Table | Select API | CRUD API | Structure Ref | Setup Ref | Status |
|-------|-------|-----------|----------|---------------|-----------|--------|
| 1-2 | User_Role_Master | GET /roles/all | POST/PUT/DELETE /roles | PROJECT_STRUCTURE.md (API 1-2) | SETUP.md (Section 6.1) | Documented |
| 3-4 | State_City_PinCode | GET /locations/all | POST/PUT/DELETE /locations | PROJECT_STRUCTURE.md (API 3-4) | SETUP.md (Section 6.2) | Documented |
| 5-6 | User_Master | GET /users/all | POST/PUT/DELETE /users | PROJECT_STRUCTURE.md (API 5-6) | SETUP.md (Section 6.3) | Documented |
| 7-8 | User_Login | GET /auth/users | POST/PUT/DELETE /auth/credentials | PROJECT_STRUCTURE.md (API 7-8) | SETUP.md (Section 6.4) | Documented |
| 9-10 | New_User_Request | GET /requests/all | POST/PUT/DELETE /requests | PROJECT_STRUCTURE.md (API 9-10) | SETUP.md (Section 6.5) | Documented |
| 11-12 | Report_History | GET /reports/all | POST/PUT/DELETE /reports | PROJECT_STRUCTURE.md (API 11-12) | SETUP.md (Section 6.6) | Documented |

---

## 📝 Document Maintenance & Synchronization

### Documentation Files
This API Development Agent is the **SOURCE OF TRUTH** for all API specifications. The following documentation files must be kept in sync:

| Document | Purpose | Location |
|----------|---------|----------|
| **API Development Agent.md** | Master API specifications & design (THIS FILE) | `/API Development/` |
| **PROJECT_STRUCTURE.md** | Project directory structure & module descriptions | `/API Development/` |
| **API_STRUCTURE_GUIDE.md** | Visual architecture & endpoint mapping | `/API Development/` |
| **API Unit Testing Agent.md** | Comprehensive test cases & testing strategy | `/API Development/Unit Testing/` |
| **SETUP.md** | Step-by-step implementation instructions | `/API Development/` |
| **REPOSITORY_SUMMARY.md** | Quick reference & file index | `/API Development/` |
| **README.md** | Project overview & getting started | Repository root |

### 🔄 API Change Synchronization Workflow

**IMPORTANT**: Whenever ANY API is modified or changed, follow this synchronization checklist:

#### Step 1: Update API Development Agent.md (THIS FILE)
- [ ] Update API specification in relevant section
- [ ] Update request/response examples
- [ ] Update error handling codes
- [ ] Update schema definitions

#### Step 2: Update PROJECT_STRUCTURE.md
- [ ] Update API Implementation Mapping table
- [ ] Update route handler specifications
- [ ] Update schema definitions section
- [ ] Update service method signatures
- [ ] Update test coverage section if tests changed

#### Step 3: Update API_STRUCTURE_GUIDE.md
- [ ] Update endpoint URL mappings
- [ ] Update request/response diagrams
- [ ] Update flow charts (if applicable)
- [ ] Update HTTP method specifications

#### Step 4: Update API Unit Testing Agent.md
- [ ] Add/update test cases for the modified API
- [ ] Update fixtures (if schema changed)
- [ ] Update test execution examples
- [ ] Update expected response validation

#### Step 5: Update SETUP.md
- [ ] Update code implementation examples
- [ ] Update environment setup instructions (if applicable)
- [ ] Update dependency requirements (if applicable)

#### Step 6: Update REPOSITORY_SUMMARY.md
- [ ] Update API endpoint quick reference
- [ ] Update file/folder index
- [ ] Update implementation status

#### Step 7: Update README.md
- [ ] Update API summary section
- [ ] Update quick start examples
- [ ] Update feature list (if applicable)

#### Step 8: Commit & Push
```bash
# Stage all updated documentation files
git add "API Development/API Development agent.md"
git add "API Development/PROJECT_STRUCTURE.md"
git add "API Development/API_STRUCTURE_GUIDE.md"
git add "API Development/Unit Testing/API Unit Testing Agent.md"
git add "API Development/SETUP.md"
git add "API Development/REPOSITORY_SUMMARY.md"
git add README.md

# Create comprehensive commit
git commit -m "docs: Update API documentation for [API_NAME] changes

Modified APIs:
- [List changes made]

Documentation Updated:
- API Development Agent.md: [Brief change description]
- PROJECT_STRUCTURE.md: [Brief change description]
- API_STRUCTURE_GUIDE.md: [Brief change description]
- API Unit Testing Agent.md: [Brief change description]
- SETUP.md: [Brief change description]
- REPOSITORY_SUMMARY.md: [Brief change description]
- README.md: [Brief change description]"

# Push to remote
git push origin main
```

### Example: API Change Case Study
**When**: User_Role_Master GET/POST/PUT APIs were enhanced on March 1, 2026
**Changed**:
- API 1 now supports 3 request scenarios
- API 2 POST now validates status values
- API 2 PUT now only updates status field
- API 2 DELETE removed

**Synchronization**:
1. ✅ Updated API Development Agent.md with new scenarios and error codes
2. ✅ Updated PROJECT_STRUCTURE.md with detailed specifications section
3. ⏳ Updated API_STRUCTURE_GUIDE.md with new endpoint diagrams
4. ✅ Updated API Unit Testing Agent.md with new test cases
5. ⏳ Updated SETUP.md with new implementation code examples
6. ⏳ Updated REPOSITORY_SUMMARY.md with new endpoint reference
7. ⏳ Updated README.md with new feature descriptions
8. ✅ Created comprehensive commit with all changes

### Documentation Interdependencies

**API Development Agent.md** → Drives all other documentation
↓
├── PROJECT_STRUCTURE.md (Detailed specifications)
├── API Unit Testing Agent.md (Test coverage)
├── SETUP.md (Implementation steps)
├── API_STRUCTURE_GUIDE.md (Visual representation)
└── REPOSITORY_SUMMARY.md (Quick reference)
    ↓
    └── README.md (User-facing summary)

---

**Last Updated**: 2026-03-01 (Added Document Synchronization Workflow)
**Created By**: Claude Code
**Status**: Design Complete & Documented - Ready for Implementation
**Database**: PostgreSQL 18.2 (medostel instance)
**Instance**: medostel-ai-assistant-pgdev-instance
**Total APIs Designed**: 12 (6 tables × 2 APIs each)
**Platform**: GKE (Google Kubernetes Engine)
**Framework**: FastAPI with Python 3.11+
**Documentation Files**: 7 comprehensive guide files
**API Enhancement Status**: API 1 & 2 (User_Role_Master) ✅ Enhanced | APIs 3-12 ⏳ Standard
