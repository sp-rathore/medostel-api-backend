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

### Summary Table: All 15 APIs

| # | Table | API Type | Method | Endpoint | Purpose |
|---|-------|----------|--------|----------|---------|
| 1 | User_Role_Master | SELECT | GET | `/api/v1/roles/all` | Retrieve all user roles |
| 2 | User_Role_Master | CRUD | POST/PUT/DELETE | `/api/v1/roles` | Create, update, delete roles |
| 3 | State_City_PinCode_Master | SELECT | GET | `/api/v1/locations/all` | Retrieve all geographic locations with state/district filtering (numeric types, pinCode as PK) |
| 3.1 | State_City_PinCode_Master | SELECT | GET | `/api/v1/locations/pincodes` | Get pinCodes for a city by city_id or city_name |
| 3.2 | State_City_PinCode_Master | SELECT | GET | `/api/v1/locations/districts/{state_id}` | Get all districts in a state (NEW - March 3, 2026) |
| 3.3 | State_City_PinCode_Master | SELECT | GET | `/api/v1/locations/cities/{district_id}` | Get all cities in a district (NEW - March 3, 2026) |
| 3.4 | State_City_PinCode_Master | SELECT | GET | `/api/v1/locations/by-district/{district_id}` | Get all pinCodes organized by city in a district (NEW - March 3, 2026) |
| 4 | State_City_PinCode_Master | CRUD | POST/PUT | `/api/v1/locations` | Create and update locations with district hierarchy (district fields immutable) |
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
**Updated**: March 3, 2026 - roleId changed from STRING to INTEGER (1-8)

#### Overview
This endpoint supports **three different request scenarios**:

1. **Fetch by Role ID**: Get a specific role by ID (integer 1-8)
2. **Fetch by Status**: Get all roles with a specific status
3. **Fetch All**: Get all roles from the table irrespective of status

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `roleId` | integer | No | Fetch specific role by ID (1-8: ADMIN=1, DOCTOR=2, ..., TECHNICIAN=8) |
| `status` | string | No | Filter by status: Active, Inactive, Closed, Pending |
| `limit` | integer | No | Limit results (default: 100, max: 1000) |
| `offset` | integer | No | Pagination offset (default: 0) |

---

#### **Scenario 1: Fetch by Role ID (Integer 1-8)**

##### Request
```bash
# Request roleId=1 (ADMIN)
curl -X GET "http://localhost:8000/api/v1/roles/all?roleId=1" \
  -H "Authorization: Bearer <jwt_token>"

# Request roleId=2 (DOCTOR)
curl -X GET "http://localhost:8000/api/v1/roles/all?roleId=2" \
  -H "Authorization: Bearer <jwt_token>"
```

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Role ID 1 retrieved successfully",
  "data": {
    "count": 1,
    "scenario": "Fetch by Role ID",
    "roles": [
      {
        "roleId": 1,
        "roleName": "ADMIN",
        "status": "Active",
        "createdDate": "2026-03-03",
        "updatedDate": "2026-03-03",
        "comments": "System Administrator - Full system access and database management"
      }
    ]
  },
  "timestamp": "2026-03-03T16:00:00Z"
}
```

##### Response (404 - Not Found)
```json
{
  "status": "error",
  "code": 404,
  "message": "Role with ID 9 not found",
  "timestamp": "2026-03-03T16:00:00Z"
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
        "roleId": 1,
        "roleName": "ADMIN",
        "status": "Active",
        "createdDate": "2026-03-03",
        "updatedDate": "2026-03-03",
        "comments": "System Administrator - Full system access and database management"
      },
      {
        "roleId": 2,
        "roleName": "DOCTOR",
        "status": "Active",
        "createdDate": "2026-03-03",
        "updatedDate": "2026-03-03",
        "comments": "Doctor or Physician - Can view and manage patient records and create medical reports"
      },
      {
        "roleId": 3,
        "roleName": "HOSPITAL",
        "status": "Active",
        "createdDate": "2026-03-03",
        "updatedDate": "2026-03-03",
        "comments": "Hospital Administrator - Hospital-level administrative functions"
      },
      {
        "roleId": 4,
        "roleName": "NURSE",
        "status": "Active",
        "createdDate": "2026-03-03",
        "updatedDate": "2026-03-03",
        "comments": "Nursing Staff - Can update patient information and create nursing reports"
      },
      {
        "roleId": 5,
        "roleName": "PARTNER",
        "status": "Active",
        "createdDate": "2026-03-03",
        "updatedDate": "2026-03-03",
        "comments": "Sales Partner - Sales and marketing partner functions"
      }
    ]
  },
  "timestamp": "2026-03-03T16:00:00Z"
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
**Updated**: March 3, 2026 - roleId auto-generated, no longer in request

---

#### **Scenario A: Insert New Role (POST)**

**Endpoint**: `POST /api/v1/roles`

##### Request Description
Insert a new role into the User_Role_Master table. **roleId is AUTO-GENERATED** (not in request body).

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `roleName` | string | Yes | Max 50 chars, unique | Human-readable role name |
| `status` | string | Yes | Active, Inactive, Closed, Pending | Role activation status |
| `comments` | string | No | Max 250 chars | Optional description |

**System-managed fields (AUTO-POPULATED):**
- `roleId`: Auto-generated SERIAL INTEGER (1-8)
- `createdDate`: Set to current system date
- `updatedDate`: Set to current system date

##### Request Example
```bash
curl -X POST http://localhost:8000/api/v1/roles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "roleName": "New Specialist Role",
    "status": "Active",
    "comments": "Role for medical specialists"
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
    "info": "roleId auto-generated, createdDate and updatedDate set to current date",
    "role": {
      "roleId": 9,
      "roleName": "New Specialist Role",
      "status": "Active",
      "createdDate": "2026-03-03",
      "updatedDate": "2026-03-03",
      "comments": "Role for medical specialists"
    }
  },
  "timestamp": "2026-03-03T16:00:00Z"
}
```

##### Response (400 - Bad Request - Invalid Status)
```json
{
  "status": "error",
  "code": 400,
  "message": "Status must be one of: Active, Inactive, Closed, Pending",
  "timestamp": "2026-03-03T16:00:00Z"
}
```

##### Response (409 - Conflict - Role Name Already Exists)
```json
{
  "status": "error",
  "code": 409,
  "message": "Role with name 'DOCTOR' already exists",
  "timestamp": "2026-03-03T16:00:00Z"
}
```

---

#### **Scenario B: Update Role Status/Comments (PUT)**

**Endpoint**: `PUT /api/v1/roles/{roleId}`

##### Request Description
Update the status and/or comments of an existing role. This endpoint updates status and/or comments fields.

**URL Parameter:**
- `roleId`: The role ID to update (INTEGER 1-8)

**Input Required (at least one):**
- `status`: New status value (must be one of: Active, Inactive, Closed, Pending)
- `comments`: Updated comments (max 250 chars)

**System-managed fields:**
- `updatedDate`: Automatically set to current system date
- Other fields (roleId, roleName): **CANNOT be modified** through this endpoint

##### Request Example
```bash
# Update DOCTOR role (roleId=2) status from Active to Inactive
curl -X PUT http://localhost:8000/api/v1/roles/2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "status": "Inactive"
  }'

# Or update comments
curl -X PUT http://localhost:8000/api/v1/roles/2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "comments": "Updated role description"
  }'
```

##### Response (200 - Updated)
```json
{
  "status": "success",
  "code": 200,
  "message": "Role ID 2 updated successfully",
  "data": {
    "scenario": "Update role status/comments",
    "info": "updatedDate set to current date. Fields roleId and roleName cannot be modified.",
    "role": {
      "roleId": 2,
      "roleName": "DOCTOR",
      "status": "Inactive",
      "createdDate": "2026-03-03",
      "updatedDate": "2026-03-03",
      "comments": "Doctor or Physician - Can view and manage patient records and create medical reports"
    }
  },
  "timestamp": "2026-03-03T16:00:00Z"
}
```

##### Response (400 - Bad Request - Invalid Status)
```json
{
  "status": "error",
  "code": 400,
  "message": "Status must be one of: Active, Inactive, Closed, Pending. Received: 'Invalid'",
  "timestamp": "2026-03-03T16:00:00Z"
}
```

##### Response (400 - Bad Request - No Fields to Update)
```json
{
  "status": "error",
  "code": 400,
  "message": "Request body must contain at least one field: 'status' or 'comments'",
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

**Updated**: March 2, 2026 - Changed to numeric data types, pinCode as Primary Key

**Endpoint**: `GET /api/v1/locations/all`
**Purpose**: Retrieve all geographic locations with filtering
**Authentication**: Not required (Public)
**Rate Limit**: 200 requests/minute

#### Request
```bash
# Get all locations in a state
curl -X GET "http://localhost:8000/api/v1/locations/all?state_id=1&status=Active" \
  -H "Accept: application/json"

# Get all locations in a specific district
curl -X GET "http://localhost:8000/api/v1/locations/all?state_id=1&district_id=1" \
  -H "Accept: application/json"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | No | Filter by country name (e.g., "India") |
| `state_id` | integer | No | Filter by state ID (numeric, 0001-0035) |
| `district_id` | integer | No | Filter by district ID (numeric, 0001-N per state) |
| `status` | string | No | Filter by status: "Active" or "Inactive" |
| `limit` | integer | No | Limit results (default: 100, max: 1000) |
| `offset` | integer | No | Pagination offset (default: 0) |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Geographic locations retrieved successfully",
  "data": {
    "count": 2,
    "locations": [
      {
        "pinCode": 400001,
        "stateId": 27,
        "stateName": "Maharashtra",
        "districtId": 1,
        "districtName": "Mumbai",
        "cityId": 102,
        "cityName": "Mumbai",
        "countryName": "India",
        "status": "Active",
        "createdDate": "2026-02-28T10:00:00Z",
        "updatedDate": "2026-02-28T10:00:00Z"
      },
      {
        "pinCode": 400002,
        "stateId": 27,
        "stateName": "Maharashtra",
        "districtId": 1,
        "districtName": "Mumbai",
        "cityId": 102,
        "cityName": "Mumbai",
        "countryName": "India",
        "status": "Active",
        "createdDate": "2026-02-28T10:00:00Z",
        "updatedDate": "2026-02-28T10:00:00Z"
      }
    ]
  },
  "timestamp": "2026-03-03T12:00:00Z"
}
```

---

### API 3.1: State_City_PinCode_Master - GET PinCodes by City (NEW)

**Added**: March 2, 2026

**Endpoint**: `GET /api/v1/locations/pincodes`
**Purpose**: Retrieve all pinCodes for a specific city
**Authentication**: Not required (Public)
**Rate Limit**: 200 requests/minute

#### Request
```bash
# By city ID
curl -X GET "http://localhost:8000/api/v1/locations/pincodes?city_id=102" \
  -H "Accept: application/json"

# By city name
curl -X GET "http://localhost:8000/api/v1/locations/pincodes?city_name=Mumbai" \
  -H "Accept: application/json"
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `city_id` | integer | Conditional | Filter by city ID (numeric). Provide this OR city_name |
| `city_name` | string | Conditional | Filter by city name. Provide this OR city_id |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "PinCodes retrieved successfully for the city",
  "data": {
    "count": 15,
    "pincodes": [400001, 400002, 400003, 400004, 400005, 400006, 400007, 400008, 400009, 400010, 400011, 400012, 400013, 400014, 400015]
  },
  "timestamp": "2026-03-02T12:00:00Z"
}
```

#### Response (400 - Bad Request)
```json
{
  "status": "error",
  "code": 400,
  "message": "At least one of city_id or city_name must be provided",
  "timestamp": "2026-03-02T12:00:00Z"
}
```

---

### API 3.2: State_City_PinCode_Master - GET Districts by State (NEW)

**Added**: March 3, 2026

**Endpoint**: `GET /api/v1/locations/districts/{state_id}`
**Purpose**: Retrieve all districts in a specific state
**Authentication**: Not required (Public)
**Rate Limit**: 200 requests/minute

#### Request
```bash
# Get all districts in Maharashtra (state_id=27)
curl -X GET "http://localhost:8000/api/v1/locations/districts/27" \
  -H "Accept: application/json"

# Get all districts in Uttar Pradesh (state_id=22)
curl -X GET "http://localhost:8000/api/v1/locations/districts/22" \
  -H "Accept: application/json"
```

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `state_id` | integer | Yes | State ID (numeric, 0001-0035) |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Districts retrieved successfully for state 27",
  "data": {
    "count": 3,
    "districts": [
      {
        "districtId": 1,
        "districtName": "Mumbai",
        "stateName": "Maharashtra"
      },
      {
        "districtId": 2,
        "districtName": "Pune",
        "stateName": "Maharashtra"
      },
      {
        "districtId": 3,
        "districtName": "Nagpur",
        "stateName": "Maharashtra"
      }
    ]
  },
  "timestamp": "2026-03-03T10:00:00Z"
}
```

---

### API 3.3: State_City_PinCode_Master - GET Cities by District (NEW)

**Added**: March 3, 2026

**Endpoint**: `GET /api/v1/locations/cities/{district_id}`
**Purpose**: Retrieve all cities in a specific district
**Authentication**: Not required (Public)
**Rate Limit**: 200 requests/minute

#### Request
```bash
# Get all cities in Mumbai district (district_id=1)
curl -X GET "http://localhost:8000/api/v1/locations/cities/1" \
  -H "Accept: application/json"

# Get all cities in another district
curl -X GET "http://localhost:8000/api/v1/locations/cities/5" \
  -H "Accept: application/json"
```

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `district_id` | integer | Yes | District ID (numeric, 0001-N per state) |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Cities retrieved successfully for district 1",
  "data": {
    "count": 2,
    "cities": [
      {
        "cityId": 101,
        "cityName": "Mumbai",
        "districtName": "Mumbai",
        "stateName": "Maharashtra"
      },
      {
        "cityId": 102,
        "cityName": "Navi Mumbai",
        "districtName": "Mumbai",
        "stateName": "Maharashtra"
      }
    ]
  },
  "timestamp": "2026-03-03T10:00:00Z"
}
```

---

### API 3.4: State_City_PinCode_Master - GET PinCodes by District (NEW)

**Added**: March 3, 2026

**Endpoint**: `GET /api/v1/locations/by-district/{district_id}`
**Purpose**: Retrieve all pinCodes in a specific district, organized by city
**Authentication**: Not required (Public)
**Rate Limit**: 200 requests/minute

#### Request
```bash
# Get all pincodes in Mumbai district (district_id=1)
curl -X GET "http://localhost:8000/api/v1/locations/by-district/1" \
  -H "Accept: application/json"

# Get all pincodes in another district
curl -X GET "http://localhost:8000/api/v1/locations/by-district/10" \
  -H "Accept: application/json"
```

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `district_id` | integer | Yes | District ID (numeric, 0001-N per state) |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "PinCodes retrieved successfully for district 1",
  "data": {
    "count": 8,
    "pincodes": [
      {
        "pinCode": 400001,
        "cityName": "Mumbai",
        "cityId": 101
      },
      {
        "pinCode": 400002,
        "cityName": "Mumbai",
        "cityId": 101
      },
      {
        "pinCode": 400003,
        "cityName": "Navi Mumbai",
        "cityId": 102
      },
      {
        "pinCode": 400004,
        "cityName": "Navi Mumbai",
        "cityId": 102
      },
      {
        "pinCode": 400005,
        "cityName": "Mumbai",
        "cityId": 101
      },
      {
        "pinCode": 400006,
        "cityName": "Mumbai",
        "cityId": 101
      },
      {
        "pinCode": 400007,
        "cityName": "Navi Mumbai",
        "cityId": 102
      },
      {
        "pinCode": 400008,
        "cityName": "Navi Mumbai",
        "cityId": 102
      }
    ]
  },
  "timestamp": "2026-03-03T10:00:00Z"
}
```

---

### API 4: State_City_PinCode_Master - CRUD Operations

**Updated**: March 2, 2026 - Changed to numeric data types, pinCode as Primary Key, DELETE removed

**Purpose**: Create and Update geographic locations (DELETE operation removed)

#### A. Create Location
**Endpoint**: `POST /api/v1/locations`
**Authentication**: Required (Admin only)

##### Request Body
```json
{
  "stateId": 22,
  "stateName": "Uttar Pradesh",
  "districtId": 1,
  "districtName": "Lucknow District",
  "cityId": 85,
  "cityName": "Lucknow",
  "pinCode": 226001,
  "countryName": "India",
  "status": "Active"
}
```

##### Request Field Details
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| stateId | integer | Yes | State ID (numeric, 0001-0035) |
| stateName | string | Yes | State/UT name |
| districtId | integer | Yes | District ID (numeric, 0001-N per state) |
| districtName | string | Yes | District name |
| cityId | integer | Yes | City ID (numeric, 0001-N per district) |
| cityName | string | Yes | City name (proper city name, not post office name) |
| pinCode | integer | Yes | Postal code (5-6 digits for India: 100000-999999, PRIMARY KEY) |
| countryName | string | No | Country name (default: "India") |
| status | string | No | Status (default: "Active", options: "Active"/"Inactive") |

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "Location created successfully",
  "data": {
    "location": {
      "pinCode": 226001,
      "stateId": 22,
      "stateName": "Uttar Pradesh",
      "districtId": 1,
      "districtName": "Lucknow District",
      "cityId": 85,
      "cityName": "Lucknow",
      "countryName": "India",
      "status": "Active",
      "createdDate": "2026-03-03T12:30:00Z",
      "updatedDate": "2026-03-03T12:30:00Z"
    }
  },
  "timestamp": "2026-03-03T12:30:00Z"
}
```

##### Response (400 - Bad Request - Invalid pinCode)
```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid pinCode. Must be 5-6 digits (100000-999999)",
  "timestamp": "2026-03-02T12:30:00Z"
}
```

#### B. Update Location
**Endpoint**: `PUT /api/v1/locations/{pin_code}`
**Authentication**: Required (Admin only)
**Note**: pinCode, stateId, stateName, districtId, districtName, cityId, and cityName are immutable (primary key and hierarchical geographic data). Only status and countryName can be updated. To move a location to a different state/district/city, delete the current record and create a new one.

##### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| pin_code | integer | Postal code (5-6 digits, e.g., 400001) |

##### Request Body
```json
{
  "status": "Inactive",
  "countryName": "India"
}
```

##### Request Field Details (all optional)
| Field | Type | Description |
|-------|------|-------------|
| status | string | Updated status ("Active" or "Inactive") |
| countryName | string | Updated country name |

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Location updated successfully",
  "data": {
    "location": {
      "pinCode": 226001,
      "stateId": 22,
      "stateName": "Uttar Pradesh",
      "districtId": 1,
      "districtName": "Lucknow District",
      "cityId": 85,
      "cityName": "Lucknow",
      "countryName": "India",
      "status": "Inactive",
      "createdDate": "2026-03-02T12:30:00Z",
      "updatedDate": "2026-03-03T12:35:00Z"
    }
  },
  "timestamp": "2026-03-03T12:35:00Z"
}
```

##### Response (404 - Not Found)
```json
{
  "status": "error",
  "code": 404,
  "message": "Location with pinCode 226001 not found",
  "timestamp": "2026-03-02T12:35:00Z"
}
```

**Note**: DELETE operation is no longer available. Locations are managed through status field (Active/Inactive).

---

### API 5: User_Master - SELECT Operations ⭐ Enhanced Mar 4, 2026

**Endpoint**: `GET /api/v1/users/all`
**Purpose**: Retrieve all user profiles with geographic hierarchy data (read-only)
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
| `limit` | integer | No | Limit results (1-1000, default: 100) |
| `offset` | integer | No | Pagination offset (default: 0) |

#### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "Users retrieved successfully",
  "data": {
    "count": 10,
    "users": [
      {
        "userId": "john.doe@medostel.com",
        "firstName": "John",
        "lastName": "Doe",
        "currentRole": "Doctor",
        "organisation": "City Hospital",
        "emailId": "john.doe@medostel.com",
        "mobileNumber": "9876543210",
        "address1": "123 Medical Street",
        "address2": "Suite 101",
        "stateId": 1,
        "stateName": "Maharashtra",
        "districtId": 1,
        "cityId": 1,
        "cityName": "Mumbai",
        "pinCode": 400001,
        "status": "Active",
        "createdDate": "2026-02-28T10:00:00Z",
        "updatedDate": "2026-03-04T14:30:00Z"
      }
    ]
  },
  "timestamp": "2026-03-04T16:00:00Z"
}
```

**Response Fields**:
- **Geographic References**: stateId, districtId, cityId (integer FK fields)
- **Geographic Display**: stateName, cityName (for UI display)
- **Address Fields**: address1, address2
- **pinCode**: Now integer (5-6 digits), FK to State_City_PinCode_Master
- **Audit Fields**: createdDate, updatedDate (ISO 8601 format)

---

### API 6: User_Master - CRUD Operations ⭐ Enhanced Mar 4, 2026

**Purpose**: Create, Update, Delete user profiles with geographic hierarchy validation

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
  "mobileNumber": "9876543211",
  "address1": "123 Health Street",
  "address2": "Apt 4",
  "stateId": 1,
  "stateName": "Maharashtra",
  "districtId": 1,
  "cityId": 1,
  "cityName": "Mumbai",
  "pinCode": 400001,
  "status": "Active"
}
```

**Request Notes**:
- All geographic FK fields (stateId, districtId, cityId, pinCode) are **OPTIONAL**
- If provided, geographic references are **VALIDATED** against State_City_PinCode_Master
- pinCode must be 5-6 digit integer (100000-999999)
- stateId, districtId, cityId must be positive integers

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "User created successfully",
  "data": {
    "user": {
      "userId": "jane.smith@medostel.com",
      "firstName": "Jane",
      "lastName": "Smith",
      "currentRole": "Patient",
      "organisation": "Self",
      "emailId": "jane.smith@medostel.com",
      "mobileNumber": "9876543211",
      "address1": "123 Health Street",
      "address2": "Apt 4",
      "stateId": 1,
      "stateName": "Maharashtra",
      "districtId": 1,
      "cityId": 1,
      "cityName": "Mumbai",
      "pinCode": 400001,
      "status": "Active",
      "createdDate": "2026-03-04T16:00:00Z",
      "updatedDate": "2026-03-04T16:00:00Z"
    }
  },
  "timestamp": "2026-03-04T16:00:00Z"
}
```

**Error Responses**:
- **409 Conflict**: User already exists
- **400 Bad Request**: Invalid geographic reference or missing required fields
- **422 Unprocessable Entity**: Validation error (email format, mobile length, etc.)

#### B. Update User Profile
**Endpoint**: `PUT /api/v1/users/{userId}`
**Authentication**: Required (Admin or Self)
**Note**: pinCode is **IMMUTABLE** and cannot be updated

##### Request Body
```json
{
  "firstName": "Jane",
  "lastName": "Smith-Johnson",
  "organisation": "City Medical Center",
  "stateId": 2,
  "stateName": "Karnataka",
  "districtId": 2,
  "cityId": 2,
  "cityName": "Bangalore",
  "address1": "456 Health Ave"
}
```

**Update Notes**:
- Only provided fields are updated; omitted fields retain current values
- pinCode **CANNOT** be updated (immutable field, set during creation)
- Geographic field updates are **VALIDATED** against master table
- All geographic fields are optional during update

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "User updated successfully",
  "data": {
    "user": {
      "userId": "jane.smith@medostel.com",
      "firstName": "Jane",
      "lastName": "Smith-Johnson",
      "currentRole": "Patient",
      "organisation": "City Medical Center",
      "stateId": 2,
      "stateName": "Karnataka",
      "districtId": 2,
      "cityId": 2,
      "cityName": "Bangalore",
      "address1": "456 Health Ave",
      "pinCode": 400001,
      "updatedDate": "2026-03-04T17:30:00Z"
    }
  },
  "timestamp": "2026-03-04T17:30:00Z"
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

> **📚 Comprehensive Reference**: For complete database schema documentation, indexes, validation rules, and data relationships, see **[Medostel Tables Agent.md](../../Data%20Engineering/Medostel%20Tables%20Agent.md)** in the Data Engineering folder.
>
> This section provides a quick overview. For detailed information including:
> - Column constraints and validation rules
> - All indexes and performance optimization
> - Data relationships and foreign keys
> - Sample data and query examples
> - Backup and recovery procedures
>
> **Always refer to Medostel Tables Agent.md** for complete database documentation.

---

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
- Kubernetes Cluster: `Development/API Development/Kubernetes_Cluster/Kubernetes Cluster Configuration.md`
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

#### 2. **APISETUP.md**
**Location**: `repositories/medostel-api-backend/APISETUP.md`
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

#### 5. **Medostel Tables Agent.md** 📊 Database Schema Documentation
**Location**: `repositories/medostel-api-backend/Data Engineering/Medostel Tables Agent.md`
**Purpose**: Comprehensive database schema, tables, and relationships documentation
**Contains**:
- Complete table definitions (6 tables)
- Column specifications and constraints
- Primary keys and indexes (35+ indexes)
- Foreign key relationships and data integrity rules
- Data validation rules for each table
- Sample data and 8 system roles
- Query examples and best practices
- Backup and recovery procedures
- Performance optimization indexes
- Data relationships diagram
- Connection pool configuration

**Use This For**: Understanding database structure, table schemas, validation rules, relationships, and all database-related implementation details

**Critical Reference For**:
- Defining ORM models in `app/database/models.py`
- Understanding foreign key relationships
- Validating data integrity rules
- Setting up proper indexes
- Designing Pydantic schemas
- Writing database queries

---

### Repository Path

**Main Documentation Files** (API Development folder):
```
/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/

API Development/
├── README.md                          ← Navigation hub
├── API Development agent.md           ← This file (Master API specs)
├── PROJECT_STRUCTURE.md               ← Detailed structure & modules
├── APISETUP.md                        ← Implementation guide with code
├── API_STRUCTURE_GUIDE.md             ← Visual architecture & diagrams
├── REPOSITORY_SUMMARY.md              ← Quick reference & checklist
├── Kubernetes_Cluster/                ← K8s configuration
├── Unit Testing/                      ← Testing documentation
└── ...
```

**Database Documentation** (Data Engineering folder):
```
Data Engineering/
└── Medostel Tables Agent.md           ← Complete database schema reference
```

---

### Repository Path

```
/Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend/

Key Files:
├── PROJECT_STRUCTURE.md        ← Detailed structure & modules
├── APISETUP.md                    ← Implementation guide with code
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
2. Read **APISETUP.md** (Step 1-2) - Setup environment
3. Read **PROJECT_STRUCTURE.md** - Understand structure
4. Continue **APISETUP.md** - Implement step-by-step

### For Understanding Architecture
**Use These Files**:
1. **API_STRUCTURE_GUIDE.md** - See data flow diagrams
2. **PROJECT_STRUCTURE.md** - Understand module relationships
3. This **API Development agent.md** - API specifications

### For Implementation
**Reference**:
1. **APISETUP.md** - Code templates and examples
2. **PROJECT_STRUCTURE.md** - Module descriptions
3. This **API Development agent.md** - API specifications

### For Quick Lookup
**Use**:
1. **REPOSITORY_SUMMARY.md** - Statistics, checklist, status
2. **API_STRUCTURE_GUIDE.md** - Visual reference

---

## 🔗 Cross-References Between Documents

### From This File (API Development agent.md)
→ For implementation details: See **APISETUP.md**
→ For project structure: See **PROJECT_STRUCTURE.md**
→ For architecture diagrams: See **API_STRUCTURE_GUIDE.md**
→ For quick reference: See **REPOSITORY_SUMMARY.md**

### Database & Infrastructure
→ For PostgreSQL details: See `Development/DevOps Development/DBA/DBA.md`
→ For GKE cluster info: See `Development/API Development/Kubernetes_Cluster/Kubernetes Cluster Configuration.md`

---

## 📊 12 APIs Implementation Checklist (With Documentation Reference)

For each of the 12 APIs, follow these documentation references:

| API # | Table | Select API | CRUD API | Structure Ref | Setup Ref | Status |
|-------|-------|-----------|----------|---------------|-----------|--------|
| 1-2 | User_Role_Master | GET /roles/all | POST/PUT/DELETE /roles | PROJECT_STRUCTURE.md (API 1-2) | APISETUP.md (Section 6.1) | Documented |
| 3-4 | State_City_PinCode | GET /locations/all | POST/PUT/DELETE /locations | PROJECT_STRUCTURE.md (API 3-4) | APISETUP.md (Section 6.2) | Documented |
| 5-6 | User_Master | GET /users/all | POST/PUT/DELETE /users | PROJECT_STRUCTURE.md (API 5-6) | APISETUP.md (Section 6.3) | Documented |
| 7-8 | User_Login | GET /auth/users | POST/PUT/DELETE /auth/credentials | PROJECT_STRUCTURE.md (API 7-8) | APISETUP.md (Section 6.4) | Documented |
| 9-10 | New_User_Request | GET /requests/all | POST/PUT/DELETE /requests | PROJECT_STRUCTURE.md (API 9-10) | APISETUP.md (Section 6.5) | Documented |
| 11-12 | Report_History | GET /reports/all | POST/PUT/DELETE /reports | PROJECT_STRUCTURE.md (API 11-12) | APISETUP.md (Section 6.6) | Documented |

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
| **APISETUP.md** | Step-by-step implementation instructions | `/API Development/` |
| **REPOSITORY_SUMMARY.md** | Quick reference & file index | `/API Development/` |
| **Medostel Tables Agent.md** | Complete database schema & relationships | `/Data Engineering/` |
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

#### Step 5: Update APISETUP.md
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
git add "API Development/APISETUP.md"
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
- APISETUP.md: [Brief change description]
- REPOSITORY_SUMMARY.md: [Brief change description]
- README.md: [Brief change description]"

# Push to remote
git push origin main
```

### Example 1: API Change Case Study (Roles APIs)
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
5. ⏳ Updated APISETUP.md with new implementation code examples
6. ⏳ Updated REPOSITORY_SUMMARY.md with new endpoint reference
7. ⏳ Updated README.md with new feature descriptions
8. ✅ Created comprehensive commit with all changes

---

### Example 2: Database Schema Enhancement (User_Master) - March 1, 2026
**When**: User_Master table schema was enhanced on March 1, 2026
**Database Changes**:
- `userId`: Changed from VARCHAR(255) to BIGINT (supports up to 1 billion users)
- `emailId`: Added RFC 5322 regex validation via CHECK constraint
- `mobileNumber`: Changed from VARCHAR(15) to NUMERIC(10) with 10-digit validation (1000000000-9999999999)
- Dependent tables updated: User_Login, New_User_Request, Report_History

**Related Files Updated**:
1. ✅ **Medostel Tables Agent.md** - Master schema documentation with validation rules
2. ✅ **create_Tables.sql** - Complete SQL schema with all constraints and indexes
3. ✅ **DevOps Development/DBA/Databasespecs.md** - Updated table definitions
4. ✅ **DevOps Development/DBA/DBA.md** - Updated instance documentation
5. ✅ **DevOps Development/DBA/DEPLOYMENT_GUIDE.md** - Updated deployment instructions
6. ⏳ **API Development Agent.md** - Needs User_Master API specification updates (APIs 5-6)
7. ⏳ **PROJECT_STRUCTURE.md** - Needs User_Master detailed specifications (APIs 5-6)
8. ⏳ **APISETUP.md** - Needs User_Master implementation code (Section 6.3)
9. ⏳ **API Unit Testing Agent.md** - Needs test cases for email/mobile validation

**Pydantic Schema Changes Required**:
```python
# User_Master schema updates needed
userId: int  # Changed from str to int (BIGINT in PostgreSQL)
emailId: EmailStr  # Add pydantic EmailStr validator
mobileNumber: int  # Changed from str to int (NUMERIC(10))
status: Literal['Active', 'Inactive', 'Suspended']  # Updated status values
```

**API Impact**:
- API 5 (GET /users/all): userId in responses will be numeric
- API 6 (POST/PUT /users): userId input validation, email format validation, 10-digit mobile validation
- Test cases: Add email format validation tests, mobile number range tests

**See Also**:
- For database details: `/Data Engineering/Medostel Tables Agent.md`
- For DBA documentation: `/DevOps Development/DBA/DBA.md`
- For schema creation: `/DevOps Development/create_Tables.sql`

### Documentation Interdependencies

**API Development Agent.md** → Drives all other documentation
↓
├── PROJECT_STRUCTURE.md (Detailed specifications)
├── API Unit Testing Agent.md (Test coverage)
├── APISETUP.md (Implementation steps)
├── API_STRUCTURE_GUIDE.md (Visual representation)
└── REPOSITORY_SUMMARY.md (Quick reference)
    ↓
    └── README.md (User-facing summary)

---

**Last Updated**: 2026-03-01 (Document Synchronization Workflow + User_Master Schema Enhancement)
**Created By**: Claude Code
**Status**: Design Complete & Documented - Schema Enhanced for Production
**Database**: PostgreSQL 18.2 (medostel instance) - Schema v2.0
**Instance**: medostel-ai-assistant-pgdev-instance
**Total APIs Designed**: 12 (6 tables × 2 APIs each)
**Platform**: GKE (Google Kubernetes Engine)
**Framework**: FastAPI with Python 3.11+
**Documentation Files**: 11 comprehensive guide files (8 in API Development + 3 in Data Engineering/DBA)
**API Enhancement Status**: API 1 & 2 (User_Role_Master) ✅ Enhanced | APIs 3-12 ⏳ Standard
**Schema Enhancement Status**: User_Master ✅ Enhanced (BIGINT userId, email validation, 10-digit mobile validation)
**Dependent Table Updates**: User_Login ✅ Updated | New_User_Request ✅ Updated | Report_History ✅ Updated
