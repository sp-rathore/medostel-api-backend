# Medostel API Backend - Project Structure

## Overview

This document outlines the complete project structure for implementing all 12 APIs according to the API Development Agent specifications.

---

## Directory Tree

```
medostel-api-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Main FastAPI application
│   ├── config.py                        # Configuration management
│   ├── constants.py                     # Application constants & error codes
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py               # Database connection & pooling
│   │   └── models.py                   # SQLAlchemy ORM models
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py                     # Authentication middleware
│   │   ├── error_handler.py            # Error handling middleware
│   │   └── logging.py                  # Logging middleware
│   ├── security/
│   │   ├── __init__.py
│   │   ├── jwt.py                      # JWT token management
│   │   ├── password.py                 # Password hashing
│   │   └── rbac.py                     # Role-based access control
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py                   # Common response models
│   │   ├── user_role.py                # User_Role_Master schemas
│   │   ├── location.py                 # State_City_PinCode_Master schemas
│   │   ├── user.py                     # User_Master schemas
│   │   ├── user_login.py               # User_Login schemas
│   │   ├── registration.py             # New_User_Request schemas
│   │   └── report.py                   # Report_History schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── roles.py                # API 1 & 2: User_Role_Master routes
│   │   │   ├── locations.py            # API 3 & 4: State_City_PinCode_Master routes
│   │   │   ├── users.py                # API 5 & 6: User_Master routes
│   │   │   ├── auth.py                 # API 7 & 8: User_Login routes
│   │   │   ├── registrations.py        # API 9 & 10: New_User_Request routes
│   │   │   └── reports.py              # API 11 & 12: Report_History routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_role_service.py        # Business logic for User_Role_Master
│   │   ├── location_service.py         # Business logic for State_City_PinCode_Master
│   │   ├── user_service.py             # Business logic for User_Master
│   │   ├── auth_service.py             # Business logic for User_Login
│   │   ├── registration_service.py     # Business logic for New_User_Request
│   │   └── report_service.py           # Business logic for Report_History
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py                  # Helper functions
│   │   ├── validators.py               # Input validators
│   │   ├── formatters.py               # Response formatters
│   │   └── cache.py                    # Caching utilities
│   └── exceptions/
│       ├── __init__.py
│       └── custom_exceptions.py        # Custom exception classes
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Pytest configuration
│   ├── test_main.py                    # Main app tests
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_roles.py               # Unit tests for API 1 & 2
│   │   ├── test_locations.py           # Unit tests for API 3 & 4
│   │   ├── test_users.py               # Unit tests for API 5 & 6
│   │   ├── test_auth.py                # Unit tests for API 7 & 8
│   │   ├── test_registrations.py       # Unit tests for API 9 & 10
│   │   └── test_reports.py             # Unit tests for API 11 & 12
│   └── integration/
│       ├── __init__.py
│       ├── test_api_integration.py     # Integration tests for all APIs
│       └── test_db_integration.py      # Database integration tests
├── .env.example                        # Environment variables example
├── .env                                # Environment variables (local)
├── .gitignore
├── .dockerignore
├── Dockerfile                          # Docker container configuration
├── docker-compose.yml                  # Docker compose for local dev
├── requirements.txt                    # Python dependencies
├── README.md                           # Project README
├── PROJECT_STRUCTURE.md                # This file
├── APISETUP.md                            # Setup instructions
└── Makefile                            # Make commands for development
```

---

## Module Descriptions

### 1. `app/main.py`
**Purpose**: Main FastAPI application entry point
**Content**:
- FastAPI app initialization
- Middleware configuration (CORS, Auth, Logging)
- Router registration for all 6 route modules
- Exception handlers
- Lifespan event managers

### 2. `app/config.py`
**Purpose**: Centralized configuration management
**Content**:
- Database connection settings
- JWT secret keys
- API version information
- Feature flags
- Logging configuration

**Example**:
```python
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@host:5432/db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
```

### 3. `app/constants.py`
**Purpose**: Application constants and error codes
**Content**:
- Error codes and messages
- Status codes
- Role definitions
- Request/response constants

**Example**:
```python
class ErrorCodes:
    AUTH_001 = "Invalid credentials"
    AUTH_002 = "Token expired"
    USER_001 = "User not found"
    DB_001 = "Database connection error"

class Roles:
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    PATIENT = "Patient"
```

### 4. `app/database/connection.py`
**Purpose**: Database connection and connection pooling
**Content**:
- PostgreSQL connection pool
- Async database session management
- Connection lifecycle management

**Example**:
```python
from psycopg2.pool import SimpleConnectionPool

db_pool = SimpleConnectionPool(
    1, 20,
    host="35.244.27.232",
    port=5432,
    database="medostel",
    user="medostel_api_user",
    password="Iag2bMi@0@6aD"
)

def get_db():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)
```

### 5. `app/database/models.py`
**Purpose**: SQLAlchemy ORM models for all 6 tables
**Content**:
- User_Role_Master model
- State_City_PinCode_Master model
- User_Master model
- User_Login model
- New_User_Request model
- Report_History model

### 6. `app/schemas/` (6 files)
**Purpose**: Pydantic models for request/response validation
**Files**:
- `user_role.py`: UserRoleCreate, UserRoleUpdate, UserRoleResponse
- `location.py`: LocationCreate, LocationUpdate, LocationResponse
- `user.py`: UserCreate, UserUpdate, UserResponse
- `user_login.py`: UserLoginCreate, UserLoginUpdate, UserLoginResponse
- `registration.py`: RegistrationCreate, RegistrationUpdate, RegistrationResponse
- `report.py`: ReportCreate, ReportUpdate, ReportResponse

### 7. `app/routes/v1/` (6 files)
**Purpose**: API route handlers for all 12 APIs
**Files**:
- `roles.py` - APIs 1 & 2 (SELECT & CRUD for User_Role_Master)
- `locations.py` - APIs 3 & 4 (SELECT & CRUD for State_City_PinCode_Master)
- `users.py` - APIs 5 & 6 (SELECT & CRUD for User_Master)
- `auth.py` - APIs 7 & 8 (SELECT & CRUD for User_Login)
- `registrations.py` - APIs 9 & 10 (SELECT & CRUD for New_User_Request)
- `reports.py` - APIs 11 & 12 (SELECT & CRUD for Report_History)

**Each file contains**:
```python
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

# SELECT API
@router.get("/all")
async def get_all_records(...):
    """Retrieve all records"""
    pass

# CRUD APIs
@router.post("")
async def create_record(...):
    """Create new record"""
    pass

@router.put("/{id}")
async def update_record(...):
    """Update record"""
    pass

@router.delete("/{id}")
async def delete_record(...):
    """Delete record"""
    pass
```

### 8. `app/services/` (6 files)
**Purpose**: Business logic layer for each table
**Files**:
- `user_role_service.py` - Business logic for User_Role_Master
- `location_service.py` - Business logic for State_City_PinCode_Master
- `user_service.py` - Business logic for User_Master
- `auth_service.py` - Business logic for User_Login
- `registration_service.py` - Business logic for New_User_Request
- `report_service.py` - Business logic for Report_History

**Each service contains**:
```python
class UserRoleService:
    @staticmethod
    async def get_all_roles(db, status=None, limit=100, offset=0):
        """Retrieve all roles with filtering"""
        pass

    @staticmethod
    async def create_role(db, role_data):
        """Create new role"""
        pass

    @staticmethod
    async def update_role(db, role_id, role_data):
        """Update role"""
        pass

    @staticmethod
    async def delete_role(db, role_id):
        """Delete role"""
        pass
```

### 9. `app/security/` (3 files)
**Purpose**: Security-related utilities
**Files**:
- `jwt.py` - JWT token creation, verification, and refresh
- `password.py` - Password hashing and verification
- `rbac.py` - Role-based access control decorators

### 10. `app/utils/` (4 files)
**Purpose**: Utility functions
**Files**:
- `helpers.py` - General helper functions
- `validators.py` - Input validation utilities
- `formatters.py` - Response formatting
- `cache.py` - Caching utilities for geographic data

### 11. `tests/` (Unit and Integration tests)
**Purpose**: Comprehensive test coverage
**Structure**:
- `unit/` - Unit tests for each API
- `integration/` - Integration tests for API chains
- `conftest.py` - Pytest fixtures and configuration

---

## API Implementation Mapping

| API # | Table | Module | Route | Service | Status |
|-------|-------|--------|-------|---------|--------|
| 1 | User_Role_Master | roles.py | GET /api/v1/roles/all | user_role_service | ✅ Enhanced |
| 2 | User_Role_Master | roles.py | POST/PUT /api/v1/roles | user_role_service | ✅ Enhanced |
| 3 | State_City_PinCode | locations.py | GET /api/v1/locations/all | location_service | ⏳ Standard |
| 4 | State_City_PinCode | locations.py | POST/PUT/DELETE /api/v1/locations | location_service | ⏳ Standard |
| 5 | User_Master | users.py | GET /api/v1/users/all | user_service | ✅ Enhanced (Schema v2.0) |
| 6 | User_Master | users.py | POST/PUT /api/v1/users | user_service | ✅ Enhanced (Schema v2.0) |
| 7 | User_Login | auth.py | GET /api/v1/auth/users | auth_service | ⏳ Standard |
| 8 | User_Login | auth.py | POST/PUT/DELETE /api/v1/auth/credentials | auth_service | ⏳ Standard |
| 9 | New_User_Request | registrations.py | GET /api/v1/requests/all | registration_service | ⏳ Standard |
| 10 | New_User_Request | registrations.py | POST/PUT/DELETE /api/v1/requests | registration_service | ⏳ Standard |
| 11 | Report_History | reports.py | GET /api/v1/reports/all | report_service | ⏳ Standard |
| 12 | Report_History | reports.py | POST/PUT/DELETE /api/v1/reports | report_service | ⏳ Standard |

---

## Detailed API Specifications: User_Role_Master (API 1 & 2)

### Overview
APIs 1 & 2 provide comprehensive role management functionality with enhanced GET endpoint supporting multiple scenarios and status-only updates via PUT. **Note**: DELETE operation is not supported.

### API 1: GET `/api/v1/roles/all` - Flexible Role Retrieval

#### Supported Request Scenarios

**Scenario 1: Fetch by Role ID (Case-Insensitive)**
```
GET /api/v1/roles/all?roleId=admin
```
- Retrieves all details for a specific role by ID
- Role ID is automatically converted to UPPERCASE for consistency
- Input: `admin` → Fetches: `ADMIN`
- Response: Single role object in array with scenario metadata

**Scenario 2: Fetch by Status Filter**
```
GET /api/v1/roles/all?status=Active
```
- Retrieves all roles matching the specified status
- Valid status values: `Active`, `Inactive`, `Pending`
- Response: Array of roles matching the status filter

**Scenario 3: Fetch All Roles (Default)**
```
GET /api/v1/roles/all
```
- Retrieves all roles from User_Role_Master table
- Returns all columns and all rows irrespective of status
- Response: Complete array of all 8 system roles

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| roleId | string | No | Fetch specific role (auto-uppercase conversion) |
| status | string | No | Filter by status (Active, Inactive, Pending) |
| limit | integer | No | Max records to return (1-1000, default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

#### Example Response (Scenario 1)
```json
{
  "status": "success",
  "code": 200,
  "message": "Role 'ADMIN' retrieved successfully",
  "data": {
    "roles": [
      {
        "roleId": "ADMIN",
        "roleName": "Administrator",
        "status": "Active",
        "comments": "System administrator with full access",
        "createdDate": "2026-01-15",
        "updatedDate": "2026-03-01"
      }
    ],
    "count": 1,
    "scenario": "Fetch by Role ID"
  },
  "timestamp": "2026-03-01T10:30:00Z"
}
```

#### Error Responses
| Status | Condition | Message |
|--------|-----------|---------|
| 404 | Role not found | Role with ID '{roleId}' not found |
| 422 | Invalid query parameter | Validation error |
| 500 | Database error | Internal server error |

---

### API 2: CRUD Operations on Roles

#### POST - Insert New Role

**Endpoint**: `POST /api/v1/roles`

**Request Body** (All fields required):
```json
{
  "roleId": "CONTRACTOR",
  "roleName": "Contractor",
  "status": "Active",
  "comments": "External contractor role with limited access"
}
```

**Required Fields**:
| Field | Type | Max Length | Description |
|-------|------|-----------|-------------|
| roleId | string | 10 chars | Unique role identifier (auto-converted to UPPERCASE) |
| roleName | string | 50 chars | Human-readable role name |
| status | string | - | Role status: **Active**, **Inactive**, or **Closed** |
| comments | string | 250 chars | Optional description of the role |

**Auto-Populated Fields** (System-generated):
- `createdDate`: Set to current system timestamp
- `updatedDate`: Set to current system timestamp

**Success Response** (HTTP 201):
```json
{
  "status": "success",
  "code": 201,
  "message": "Role created successfully",
  "data": {
    "role": {
      "roleId": "CONTRACTOR",
      "roleName": "Contractor",
      "status": "Active",
      "comments": "External contractor role with limited access",
      "createdDate": "2026-03-01",
      "updatedDate": "2026-03-01"
    },
    "scenario": "Insert new role",
    "info": "createdDate and updatedDate set to current system timestamp"
  },
  "timestamp": "2026-03-01T10:30:00Z"
}
```

**Error Responses**:
| Status | Condition | Message |
|--------|-----------|---------|
| 400 | Invalid status | Status must be one of: Active, Inactive, Closed |
| 409 | Duplicate role | Role '{roleId}' already exists |
| 422 | Validation error | Missing required field or invalid data type |
| 500 | Database error | Internal server error |

---

#### PUT - Update Role Status (Status-Only Update)

**Endpoint**: `PUT /api/v1/roles/{roleId}`

**URL Parameter**:
- `roleId`: Role identifier (auto-converted to UPPERCASE for case-insensitive matching)

**Request Body**:
```json
{
  "status": "Inactive"
}
```

**Input Validation**:
- Only field accepted: `status`
- Valid values: **Active**, **Inactive**, **Closed**
- Status field is mandatory in request body

**Protected Fields** (Cannot be modified):
- `roleId`: Cannot be changed
- `roleName`: Cannot be changed
- `comments`: Cannot be changed

**Auto-Updated Field**:
- `updatedDate`: Set to current system timestamp

**Success Response** (HTTP 200):
```json
{
  "status": "success",
  "code": 200,
  "message": "Role 'CONTRACTOR' status updated to 'Inactive' successfully",
  "data": {
    "role": {
      "roleId": "CONTRACTOR",
      "roleName": "Contractor",
      "status": "Inactive",
      "comments": "External contractor role with limited access",
      "createdDate": "2026-03-01",
      "updatedDate": "2026-03-01"
    },
    "scenario": "Update role status",
    "info": "updatedDate set to current system timestamp. Other fields cannot be modified."
  },
  "timestamp": "2026-03-01T10:35:00Z"
}
```

**Error Responses**:
| Status | Condition | Message |
|--------|-----------|---------|
| 400 | Missing status field | Request body must contain 'status' field |
| 400 | Invalid status | Status must be one of: Active, Inactive, Closed. Received: '{value}' |
| 404 | Role not found | Role '{roleId}' not found |
| 422 | Validation error | Invalid request body format |
| 500 | Database error | Internal server error |

---

#### DELETE Operation

**Status**: ❌ **NOT SUPPORTED** - Removed as of March 1, 2026
- No delete operation is available for roles
- Roles cannot be deleted from the system
- Use status update to deactivate roles instead

---

### Schema Definitions (app/schemas/user_role.py)

```python
class UserRoleCreate(BaseModel):
    """Schema for creating a new role"""
    roleId: str = Field(..., max_length=10, description="Unique role ID")
    roleName: str = Field(..., max_length=50, description="Role name")
    status: str = Field(..., regex="^(Active|Inactive|Closed)$", description="Role status")
    comments: str = Field(..., max_length=250, description="Role comments")

class UserRoleUpdate(BaseModel):
    """Schema for updating role status only"""
    status: str = Field(..., regex="^(Active|Inactive|Closed)$", description="Role status")

class UserRoleResponse(BaseModel):
    """Schema for role response"""
    roleId: str
    roleName: str
    status: str
    comments: str
    createdDate: date
    updatedDate: date

    class Config:
        from_attributes = True
```

---

### Service Methods (app/services/user_role_service.py)

```python
class UserRoleService:

    @staticmethod
    async def get_role_by_id(db, roleId: str):
        """Fetch single role by ID (case-insensitive)"""
        # Converts roleId to uppercase internally

    @staticmethod
    async def get_all_roles(db, status: str = None, limit: int = 100, offset: int = 0):
        """Fetch all roles with optional status filter and pagination"""

    @staticmethod
    async def create_role(db, role_data: dict):
        """Create new role with auto-populated timestamps"""
        # createdDate and updatedDate set to current timestamp

    @staticmethod
    async def update_role(db, roleId: str, update_data: dict):
        """Update role status only; auto-updates updatedDate"""
        # Only status field can be modified
```

---

### Database Schema (User_Role_Master)

```sql
CREATE TABLE user_role_master (
    roleId VARCHAR(10) PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Inactive', 'Closed', 'Pending')),
    comments VARCHAR(250),
    createdDate DATE NOT NULL DEFAULT CURRENT_DATE,
    updatedDate DATE NOT NULL DEFAULT CURRENT_DATE
);
```

**System Roles** (8 total):
- ADMIN: Administrator
- DOCTOR: Doctor
- HOSPITAL: Hospital administrator
- NURSE: Nurse
- PARTNER: Sales and marketing partner
- PATIENT: Patient
- RECEPTION: Reception staff
- TECHNICIAN: Technician

---

### Test Coverage (test_roles_api.py)

**GET Endpoint Tests**: 8+ test cases
- Fetch by roleId (case-insensitive)
- Fetch by status (Active, Inactive, Pending)
- Fetch all roles
- Pagination support
- Invalid parameters
- Empty results

**POST Endpoint Tests**: 5+ test cases
- Create role successfully
- Duplicate role conflict (409)
- Invalid status value (400)
- Missing required fields (422)
- Auto-timestamp population verification

**PUT Endpoint Tests**: 5+ test cases
- Update status successfully
- Case-insensitive roleId handling
- Invalid status value (400)
- Missing status field (400)
- Non-existent role (404)
- Protected field enforcement

---

## Detailed API Specifications: User_Master (API 5 & 6) - ENHANCED SCHEMA

### Overview
APIs 5 & 6 manage user profiles with **enhanced schema v2.0** (March 1, 2026):
- `userId`: BIGINT (supports up to 1 billion users)
- `emailId`: Email format validation using RFC 5322 regex
- `mobileNumber`: NUMERIC(10) with 10-digit validation (1000000000-9999999999)
- `status`: Active/Inactive/Suspended

### API 5: GET `/api/v1/users/all` - Flexible User Retrieval

#### Supported Request Scenarios

**Scenario 1: Fetch by User ID (Numeric)**
```
GET /api/v1/users/all?userId=1001
```
- Retrieves complete user profile by numeric userId
- Response: Single user object with all details

**Scenario 2: Fetch by Email**
```
GET /api/v1/users/all?email=user@example.com
```
- Retrieves user by email address
- Validates email format in query parameter

**Scenario 3: Fetch by Role**
```
GET /api/v1/users/all?role=DOCTOR&status=Active
```
- Retrieves all users with specific role and status
- Supports pagination with limit/offset

**Scenario 4: Fetch All Users**
```
GET /api/v1/users/all?limit=10&offset=0
```
- Retrieves all users with pagination
- Default limit: 100, max: 1000

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `userId` | integer | No | Numeric user ID (BIGINT) |
| `email` | string | No | Email address (RFC 5322 validated) |
| `role` | string | No | Role ID (e.g., DOCTOR, PATIENT) |
| `status` | string | No | Active, Inactive, or Suspended |
| `limit` | integer | No | Results per page (default: 100, max: 1000) |
| `offset` | integer | No | Pagination offset (default: 0) |

#### Response Schema

```json
{
  "status": "success",
  "code": 200,
  "message": "User profile retrieved successfully",
  "data": {
    "count": 1,
    "users": [
      {
        "userId": 1001,
        "firstName": "John",
        "lastName": "Doe",
        "currentRole": "DOCTOR",
        "emailId": "john.doe@medostel.com",
        "mobileNumber": "9876543210",
        "organisation": "Apollo Hospital",
        "address": "Mumbai, India",
        "status": "Active",
        "createdDate": "2026-02-28T10:00:00Z",
        "updatedDate": "2026-03-01T12:00:00Z"
      }
    ]
  },
  "timestamp": "2026-03-01T16:00:00Z"
}
```

#### Error Responses

| Code | Error | Message |
|------|-------|---------|
| 400 | Invalid email format | Email validation failed for: '{email}' |
| 400 | Invalid status | Status must be one of: Active, Inactive, Suspended |
| 404 | User not found | User with ID '{userId}' not found |
| 422 | Validation error | Invalid query parameter format |
| 500 | Database error | Internal server error |

---

### API 6: CRUD Operations on User Profiles

#### POST - Create New User

**Endpoint**: `POST /api/v1/users`

##### Request Body

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `userId` | integer | Yes | Unique, 1-1000000000 | Numeric user identifier |
| `firstName` | string | Yes | Max 100 chars | User first name |
| `lastName` | string | Yes | Max 100 chars | User last name |
| `currentRole` | string | Yes | Valid roleId | Must reference User_Role_Master |
| `emailId` | string | Yes | RFC 5322 valid, unique | Email format validation |
| `mobileNumber` | string | Yes | Exactly 10 digits | Range: 1000000000-9999999999 |
| `organisation` | string | No | Max 255 chars | Organization name |
| `address` | string | No | Max 1000 chars | Full address |
| `status` | string | No | Default: Active | Active, Inactive, or Suspended |

**System-managed fields (AUTO-POPULATED):**
- `createdDate`: Current timestamp
- `updatedDate`: Current timestamp

##### Request Example
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "userId": 1001,
    "firstName": "John",
    "lastName": "Doe",
    "currentRole": "DOCTOR",
    "emailId": "john.doe@medostel.com",
    "mobileNumber": "9876543210",
    "organisation": "Apollo Hospital",
    "address": "Mumbai, India",
    "status": "Active"
  }'
```

##### Response (201 - Created)
```json
{
  "status": "success",
  "code": 201,
  "message": "User created successfully",
  "data": {
    "userId": 1001,
    "firstName": "John",
    "lastName": "Doe",
    "currentRole": "DOCTOR",
    "emailId": "john.doe@medostel.com",
    "mobileNumber": "9876543210",
    "organisation": "Apollo Hospital",
    "address": "Mumbai, India",
    "status": "Active",
    "createdDate": "2026-03-01T16:00:00Z",
    "updatedDate": "2026-03-01T16:00:00Z"
  }
}
```

##### Error Responses
| Code | Error | Message |
|------|-------|---------|
| 400 | Invalid email | Email must be in format: name@domain.ext |
| 400 | Invalid mobile | Mobile number must be exactly 10 digits (1000000000-9999999999) |
| 400 | Invalid role | Role 'INVALID' does not exist |
| 409 | Duplicate userId | User with ID 1001 already exists |
| 409 | Duplicate email | Email 'john.doe@medostel.com' already exists |
| 409 | Duplicate mobile | Mobile number '9876543210' already exists |
| 422 | Validation error | Missing required field or invalid data type |
| 500 | Database error | Internal server error |

---

#### PUT - Update User Profile

**Endpoint**: `PUT /api/v1/users/{userId}`

##### Request Body (Any fields can be updated)

| Field | Type | Updateable | Notes |
|-------|------|-----------|-------|
| `firstName` | string | ✅ Yes | Update first name |
| `lastName` | string | ✅ Yes | Update last name |
| `currentRole` | string | ✅ Yes | Update user role |
| `emailId` | string | ✅ Yes | RFC 5322 validation applied |
| `mobileNumber` | string | ✅ Yes | 10-digit validation applied |
| `organisation` | string | ✅ Yes | Update organization |
| `address` | string | ✅ Yes | Update address |
| `status` | string | ✅ Yes | Active, Inactive, Suspended |
| `userId` | integer | ❌ No | Cannot be modified |
| `createdDate` | timestamp | ❌ No | Auto-managed |
| `updatedDate` | timestamp | ❌ No | Auto-managed (updated automatically) |

##### Request Example
```bash
curl -X PUT http://localhost:8000/api/v1/users/1001 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "firstName": "Jonathan",
    "status": "Active",
    "organisation": "Max Hospital"
  }'
```

##### Response (200 - Success)
```json
{
  "status": "success",
  "code": 200,
  "message": "User profile updated successfully",
  "data": {
    "userId": 1001,
    "firstName": "Jonathan",
    "lastName": "Doe",
    "currentRole": "DOCTOR",
    "emailId": "john.doe@medostel.com",
    "mobileNumber": "9876543210",
    "organisation": "Max Hospital",
    "address": "Mumbai, India",
    "status": "Active",
    "createdDate": "2026-03-01T16:00:00Z",
    "updatedDate": "2026-03-01T17:00:00Z"
  }
}
```

##### Error Responses
| Code | Error | Message |
|------|-------|---------|
| 400 | Immutable field | Cannot modify 'userId' field |
| 400 | Invalid email | Email validation failed: 'invalid-email' |
| 400 | Invalid mobile | Mobile must be 10 digits: 1000000000-9999999999 |
| 400 | Invalid status | Status must be one of: Active, Inactive, Suspended |
| 404 | User not found | User with ID 1001 not found |
| 409 | Duplicate email | Email already in use by another user |
| 409 | Duplicate mobile | Mobile number already in use by another user |
| 422 | Validation error | Invalid request body format |
| 500 | Database error | Internal server error |

---

#### DELETE Operation

**Status**: ❌ **NOT SUPPORTED** (Standard behavior)
- User profiles can be deactivated by updating status to 'Inactive' or 'Suspended'
- Hard delete is not recommended for audit trail purposes

---

### Schema Definitions (app/schemas/user.py)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    userId: int = Field(..., ge=1, le=1000000000, description="Numeric user ID")
    firstName: str = Field(..., max_length=100)
    lastName: str = Field(..., max_length=100)
    currentRole: str = Field(..., max_length=50)
    emailId: EmailStr  # RFC 5322 validation via pydantic
    mobileNumber: str = Field(..., pattern="^[0-9]{10}$", description="10 digits")
    organisation: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = None
    status: str = Field(default="Active", pattern="^(Active|Inactive|Suspended)$")

class UserUpdate(BaseModel):
    firstName: Optional[str] = Field(None, max_length=100)
    lastName: Optional[str] = Field(None, max_length=100)
    currentRole: Optional[str] = Field(None, max_length=50)
    emailId: Optional[EmailStr] = None
    mobileNumber: Optional[str] = Field(None, pattern="^[0-9]{10}$")
    organisation: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(Active|Inactive|Suspended)$")

class UserResponse(BaseModel):
    userId: int
    firstName: str
    lastName: str
    currentRole: str
    emailId: str
    mobileNumber: str
    organisation: Optional[str]
    address: Optional[str]
    status: str
    createdDate: datetime
    updatedDate: datetime

    class Config:
        from_attributes = True
```

---

### Service Methods (app/services/user_service.py)

```python
class UserService:
    @staticmethod
    async def get_user_by_id(db, userId: int):
        """Fetch user by numeric userId"""
        # Validate userId range (1-1000000000)
        # Query user_master table
        # Return user details with timestamps

    @staticmethod
    async def get_user_by_email(db, emailId: str):
        """Fetch user by email with validation"""
        # Validate email format (RFC 5322)
        # Query user_master table
        # Return user details

    @staticmethod
    async def get_users_by_role(db, currentRole: str, status: str, limit: int, offset: int):
        """Fetch users filtered by role and status"""
        # Validate role exists in user_role_master
        # Query with pagination
        # Return users list

    @staticmethod
    async def create_user(db, user_data: dict):
        """Create new user with validation"""
        # Validate userId uniqueness (BIGINT range)
        # Validate emailId format and uniqueness
        # Validate mobileNumber (10 digits) and uniqueness
        # Validate currentRole exists
        # Auto-populate createdDate and updatedDate
        # Insert into user_master table

    @staticmethod
    async def update_user(db, userId: int, update_data: dict):
        """Update user profile with validation"""
        # Prevent modification of userId and timestamps
        # Validate emailId format if provided
        # Validate mobileNumber if provided
        # Auto-update updatedDate
        # Update user_master table
```

---

### Database Schema (User_Master)

```sql
CREATE TABLE user_master (
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

-- Indexes for performance
CREATE INDEX idx_user_email ON user_master(emailId);
CREATE INDEX idx_user_mobile ON user_master(mobileNumber);
CREATE INDEX idx_user_role ON user_master(currentRole);
CREATE INDEX idx_user_status ON user_master(status);
CREATE INDEX idx_user_name ON user_master(firstName, lastName);
```

---

### Test Coverage (test_users_api.py)

**GET Endpoint Tests**: 6+ test cases
- Fetch by userId (numeric validation)
- Fetch by email (format validation)
- Fetch by role and status (filter validation)
- Fetch all with pagination
- Invalid userId range
- Invalid email format
- Non-existent user

**POST Endpoint Tests**: 8+ test cases
- Valid user creation with all fields
- Email format validation (valid/invalid)
- Mobile number validation (10 digits, range check)
- Duplicate userId (409 error)
- Duplicate email (409 error)
- Duplicate mobile (409 error)
- Invalid role reference
- Missing required fields

**PUT Endpoint Tests**: 7+ test cases
- Update individual fields
- Email format validation on update
- Mobile number validation on update
- Status update (Active/Inactive/Suspended)
- Prevent userId modification (attempt = 400)
- Non-existent user (404)
- Concurrent update handling

---

## Configuration Management

### Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API
API_TITLE=Medostel Healthcare API
API_VERSION=1.0.0
DEBUG=False

# Logging
LOG_LEVEL=INFO

# Google Cloud
GOOGLE_PROJECT_ID=gen-lang-client-0064186167
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,https://api.medostel.com
```

---

## Development Workflow

### 1. Setup Phase
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run migrations (if using Alembic)
alembic upgrade head
```

### 2. Development Phase
```bash
# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API Documentation available at:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### 3. Testing Phase
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/unit/test_roles.py

# Run integration tests
pytest tests/integration/
```

### 4. Deployment Phase
```bash
# Build Docker image
docker build -t medostel-api:latest .

# Push to registry
docker push gcr.io/gen-lang-client-0064186167/medostel-api:latest

# Deploy to Cloud Run
gcloud run deploy medostel-api \
  --image gcr.io/gen-lang-client-0064186167/medostel-api:latest \
  --platform managed \
  --region asia-south1 \
  --project gen-lang-client-0064186167
```

---

## Dependency Injection Pattern

All endpoints use FastAPI dependency injection:

```python
@app.get("/api/v1/roles/all")
async def get_roles(
    db = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all roles with pagination"""
    return await UserRoleService.get_all_roles(db, limit, offset)
```

---

## Key Design Patterns

### 1. Service Layer Pattern
- Routes delegate to Services
- Services contain business logic
- Services interact with database

### 2. Repository Pattern (Optional)
- Data access layer
- Separates database operations from services

### 3. Middleware Pattern
- Request/Response preprocessing
- Authentication enforcement
- Logging and error handling

### 4. Pydantic Schemas
- Request validation
- Response serialization
- OpenAPI documentation generation

---

## Response Format (Consistent)

All API responses follow this format:

```json
{
  "status": "success|error",
  "code": 200,
  "message": "Operation description",
  "data": {
    // Response payload
  },
  "timestamp": "2026-02-28T16:00:00Z"
}
```

---

## Error Handling

All errors return standardized format:

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

## Testing Strategy

### Unit Tests
- Test individual service methods
- Mock database calls
- Test business logic

### Integration Tests
- Test complete API flows
- Use test database
- Test error scenarios
- Test authentication and authorization

### End-to-End Tests
- Test full API chains
- Test with real database
- Performance testing

---

## Documentation

### API Documentation
- Automatically generated from FastAPI/Pydantic
- Available at `/docs` (Swagger UI)
- Available at `/redoc` (ReDoc)

### Code Documentation
- Docstrings for all classes and functions
- README.md in project root
- This PROJECT_STRUCTURE.md file

---

## Next Steps

1. Create all module files according to this structure
2. Implement database models (app/database/models.py)
3. Implement Pydantic schemas (app/schemas/)
4. Implement services (app/services/)
5. Implement routes (app/routes/v1/)
6. Add authentication and authorization
7. Write comprehensive tests
8. Deploy to Cloud Run on GKE

---

**Last Updated**: 2026-03-01
**Created By**: Claude Code
**Status**: API 1-2 & 5-6 Enhanced & Documented - Ready for Implementation
**Total APIs**: 12 (6 tables × 2 APIs each)
**Database Schema**: v2.0 (User_Master enhanced with BIGINT userId, email validation, 10-digit mobile)

### Recent Updates (March 1, 2026)

#### API Enhancement: User_Role_Master (API 1 & 2)
- ✅ **API 1 (GET /api/v1/roles/all)**: Enhanced with 3 request scenarios (by ID, by status, fetch all)
- ✅ **API 2 (POST /api/v1/roles)**: Status validation (Active/Inactive/Closed), auto-uppercase roleId, auto-timestamp population
- ✅ **API 2 (PUT /api/v1/roles/{roleId})**: Status-only updates, protected fields (roleId, roleName, comments), auto-timestamp updates
- ❌ **API 2 (DELETE)**: Removed - no delete operation supported

#### Database Schema Enhancement: User_Master (API 5 & 6)
- ✅ **userId**: Changed from VARCHAR to BIGINT (supports up to 1 billion users)
- ✅ **emailId**: Added RFC 5322 regex validation via CHECK constraint
- ✅ **mobileNumber**: Changed to NUMERIC(10) with 10-digit validation (1000000000-9999999999)
- ✅ **API 5 (GET /api/v1/users/all)**: 4 flexible request scenarios with comprehensive validation
- ✅ **API 6 (POST /api/v1/users)**: Full user creation with validation, auto-timestamp population
- ✅ **API 6 (PUT /api/v1/users/{userId})**: Full profile updates with field-level validation, immutable field protection
- ❌ **API 6 (DELETE)**: Not supported - use status update to deactivate

#### Documentation
- 📝 Comprehensive test cases documented (21+ tests for API 5 & 6)
- 📊 Complete schema, service methods, and database schema documentation
- 📈 Detailed API specifications with request/response examples
