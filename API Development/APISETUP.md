# Medostel API Backend - Setup & Implementation Guide

---

## ⭐ Latest Enhancements

### Phase 1: Location APIs - Schema Refactoring (March 2, 2026) 🆕

**State_City_PinCode_Master (API 3 & 4) - Numeric Data Types & pinCode as Primary Key**

Major refactoring completed to improve data integrity and API design:

#### **Changes Made**:
✅ **Data Type Improvements**:
- stateId: VARCHAR(10) → INTEGER (numeric state identifiers)
- cityId: VARCHAR(10) → INTEGER (numeric city identifiers)
- pinCode: VARCHAR(10) → INTEGER (5-6 digit postal codes)

✅ **Primary Key Restructuring**:
- Removed: Surrogate key `id` (SERIAL)
- Added: Natural key `pinCode` (INTEGER PRIMARY KEY)
- Benefits: Better data integrity, direct pinCode identification

✅ **API Endpoint Changes**:
- PUT endpoint: `/api/v1/locations/{id}` → `/api/v1/locations/{pin_code}`
- DELETE endpoint: **REMOVED** (status field used instead)
- NEW endpoint: `GET /api/v1/locations/pincodes` for city-based lookups

✅ **Query Parameter Updates**:
- state_id: Now accepts INTEGER (numeric) instead of string

✅ **New Endpoint - API 3.1**:
```
GET /api/v1/locations/pincodes?city_id=102
GET /api/v1/locations/pincodes?city_name=Mumbai
```
- Fetch all pinCodes for a specific city
- Supports both city_id (numeric) and city_name (string) parameters

#### **Migration Details**:
- Database: See `DevOps Development/DBA/MIGRATION_STRATEGY.md` for comprehensive migration guide
- Migration Script: `DevOps Development/DBA/migration_step1.sql` (ready for execution)
- Pre/post-migration validation included

---

### Phase 2: Earlier Enhancements (March 1, 2026)

### Dual API Enhancement: User_Role_Master (API 1 & 2) + User_Master (API 5 & 6)

Two major API implementations with comprehensive implementation code, schemas, and services.

---

## API 1 & 2: User_Role_Master - Flexible Role Management

The User_Role_Master implementation provides flexible role management:

#### **API 1: GET /api/v1/roles/all - Three Request Scenarios**
✅ **Scenario 1**: Fetch by roleId with case-insensitive handling
- Example: `GET /api/v1/roles/all?roleId=admin` → Returns `ADMIN` role
- Auto-converts lowercase input to uppercase

✅ **Scenario 2**: Fetch by status filter
- Example: `GET /api/v1/roles/all?status=Active` → Returns all active roles
- Filters by status (Active, Inactive, Pending)

✅ **Scenario 3**: Fetch all roles (default)
- Example: `GET /api/v1/roles/all` → Returns all 8 system roles
- No filtering applied

#### **API 2: POST /api/v1/roles - Create Role with Validation**
✅ **Input validation**:
- Required fields: roleId, roleName, status, comments
- Status validation: Must be one of (Active, Inactive, Closed)

✅ **Auto-conversion**:
- roleId automatically converted to UPPERCASE

✅ **Auto-population**:
- createdDate: Set to current system date
- updatedDate: Set to current system date

✅ **Error handling**:
- 409 Conflict if role already exists
- 400 Bad Request if status is invalid
- 422 Validation error for missing/invalid fields

#### **API 2: PUT /api/v1/roles/{roleId} - Status-Only Updates**
✅ **Status-only update**: Only the `status` field can be modified
- Other fields protected: roleId, roleName, comments

✅ **Case-insensitive**: URL parameter `roleId` auto-converted to uppercase

✅ **Auto-updated**:
- updatedDate: Set to current system date

✅ **Error handling**:
- 400 Bad Request if status field missing
- 400 Bad Request if status value invalid
- 404 Not Found if role doesn't exist

#### **API 2: DELETE - NOT SUPPORTED**
❌ Delete operation has been removed
- Use status update to deactivate roles instead

---

## API 5 & 6: User_Master - Enhanced Schema v2.0

The User_Master implementation with enhanced schema featuring BIGINT userId, email validation, and mobile number validation.

#### **API 5: GET /api/v1/users/all - Four Flexible Scenarios**
✅ **Scenario 1**: Fetch by numeric userId (BIGINT)
- Example: `GET /api/v1/users/all?userId=1001` → Returns user with that numeric ID
- Validates userId range: 1-1000000000

✅ **Scenario 2**: Fetch by email (RFC 5322 validated)
- Example: `GET /api/v1/users/all?email=john.doe@medostel.com` → Returns user with matching email
- Validates email format on query parameter

✅ **Scenario 3**: Filter by role and status
- Example: `GET /api/v1/users/all?role=DOCTOR&status=Active` → Returns filtered users
- Optional role and status filters

✅ **Scenario 4**: Fetch all with pagination
- Example: `GET /api/v1/users/all?limit=10&offset=0` → Paginated results
- Default limit: 100, max: 1000

#### **API 6: POST /api/v1/users - Create User with Enhanced Validation**
✅ **BIGINT userId**: Supports 1 billion users (1-1000000000)

✅ **Email RFC 5322 Validation**:
- Pattern: `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$`
- Uniqueness enforced

✅ **Mobile Number Validation**:
- Exactly 10 digits
- Range: 1000000000-9999999999
- Uniqueness enforced

✅ **Auto-population**:
- createdDate: Set to current timestamp
- updatedDate: Set to current timestamp

✅ **Error handling**:
- 409 Conflict if userId/email/mobile already exists
- 400 Bad Request for validation failures
- 422 Validation error for missing/invalid fields

#### **API 6: PUT /api/v1/users/{userId} - Update with Field-Level Validation**
✅ **Updateable Fields**: firstName, lastName, currentRole, emailId, mobileNumber, organisation, address, status

✅ **Immutable Field Protection**:
- userId: Cannot be modified
- createdDate: Preserved

✅ **Field Validation on Update**:
- Email: RFC 5322 format
- Mobile: 10 digits in range 1000000000-9999999999
- Status: Active/Inactive/Suspended

✅ **Auto-updated**:
- updatedDate: Set to current timestamp

✅ **Error handling**:
- 400 Bad Request if userId modification attempted
- 404 Not Found if user doesn't exist
- 409 Conflict if email/mobile duplicate

#### **API 6: DELETE - NOT SUPPORTED**
❌ Delete operation not supported
- Use status update to deactivate users instead

---

## Prerequisites

- Python 3.11+
- PostgreSQL 18.2 (already running on 35.244.27.232:5432)
- Docker & Docker Compose (for containerization)
- Git (for version control)
- Google Cloud SDK (for Cloud Run deployment)

---

## Step 1: Initial Setup

### 1.1 Clone and Navigate
```bash
cd /Users/shishupals/Documents/Claude/projects/Medostel/repositories/medostel-api-backend
```

### 1.2 Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.3 Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 1.4 Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with actual values
```

**Edit `.`.env with**:
```bash
# Database Configuration
DATABASE_URL=postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel

# JWT Configuration
SECRET_KEY=your-super-secret-key-minimum-32-characters-long-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API Configuration
API_TITLE=Medostel Healthcare API
API_VERSION=1.0.0
DEBUG=False

# Logging
LOG_LEVEL=INFO

# Google Cloud
GOOGLE_PROJECT_ID=gen-lang-client-0064186167
GOOGLE_REGION=asia-south1

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,https://api.medostel.com

# Database Connection Pool
DB_POOL_SIZE=5
DB_POOL_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
```

---

## Step 2: Create Directory Structure

Create all necessary directories:

```bash
mkdir -p app/database
mkdir -p app/middleware
mkdir -p app/security
mkdir -p app/schemas
mkdir -p app/routes/v1
mkdir -p app/services
mkdir -p app/utils
mkdir -p app/exceptions
mkdir -p tests/unit
mkdir -p tests/integration
```

---

## Step 3: Create Core Configuration Files

### 3.1 `app/config.py`
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "Medostel Healthcare API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel"
    DB_POOL_SIZE: int = 5
    DB_POOL_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"

    # Google Cloud
    GOOGLE_PROJECT_ID: str = "gen-lang-client-0064186167"
    GOOGLE_REGION: str = "asia-south1"

    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://api.medostel.com"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 3.2 `app/constants.py`
```python
# Error Codes
class ErrorCodes:
    AUTH_001 = "Invalid credentials"
    AUTH_002 = "Token expired"
    AUTH_003 = "Insufficient permissions"
    USER_001 = "User not found"
    USER_002 = "Email already exists"
    USER_003 = "Invalid input data"
    DB_001 = "Database connection error"
    FILE_001 = "Invalid file type"
    FILE_002 = "File size exceeds limit"
    ROLE_001 = "Role not found"
    ROLE_002 = "Role already exists"
    LOCATION_001 = "Location not found"
    REPORT_001 = "Report not found"
    REQUEST_001 = "Registration request not found"

# User Roles
class Roles:
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    PATIENT = "Patient"

# Status Codes
class StatusCodes:
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    CLOSED = "Closed"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    ERROR = "Error"

# Database Table Names
class TableNames:
    USER_ROLE_MASTER = "user_role_master"
    STATE_CITY_PINCODE_MASTER = "state_city_pincode_master"
    USER_MASTER = "user_master"
    USER_LOGIN = "user_login"
    NEW_USER_REQUEST = "new_user_request"
    REPORT_HISTORY = "report_history"
```

---

## Step 4: Create Database Connection

### 4.1 `app/database/connection.py`
```python
import logging
from psycopg2.pool import SimpleConnectionPool
from app.config import settings

logger = logging.getLogger(__name__)

# Create connection pool
try:
    db_pool = SimpleConnectionPool(
        settings.DB_POOL_SIZE,
        settings.DB_POOL_SIZE + settings.DB_POOL_MAX_OVERFLOW,
        settings.DATABASE_URL,
        timeout=settings.DB_POOL_TIMEOUT
    )
    logger.info("Database connection pool created successfully")
except Exception as e:
    logger.error(f"Failed to create database connection pool: {e}")
    raise

def get_db():
    """Database dependency for FastAPI"""
    conn = db_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db_pool.putconn(conn)

def close_db():
    """Close all database connections"""
    db_pool.closeall()
    logger.info("Database connection pool closed")
```

### 4.2 `app/database/__init__.py`
```python
from app.database.connection import get_db, close_db

__all__ = ["get_db", "close_db"]
```

---

## Step 5: Create Pydantic Schemas

### 5.1 `app/schemas/common.py`
```python
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class APIResponse(BaseModel):
    """Standard API response model"""
    status: str  # "success" or "error"
    code: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime

class ErrorResponse(APIResponse):
    """Error response model"""
    status: str = "error"
```

### 5.2 `app/schemas/user_role.py` - Enhanced with Status-Only Updates

**Updated March 1, 2026** ✅ - UserRoleUpdate now only allows status field updates

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UserRoleBase(BaseModel):
    roleId: str = Field(..., max_length=10, description="Unique role ID (auto-converted to uppercase)")
    roleName: str = Field(..., max_length=50, description="Human-readable role name")
    status: str = Field(default="Active", description="Role status: Active, Inactive, or Closed")
    comments: Optional[str] = Field(None, max_length=250, description="Role description/comments")

class UserRoleCreate(UserRoleBase):
    """Schema for creating a new role - all fields required"""
    pass

class UserRoleUpdate(BaseModel):
    """Schema for updating role - ONLY status field is editable"""
    status: str = Field(..., description="New status value (Active, Inactive, or Closed)")

    class Config:
        json_schema_extra = {
            "description": "Update role status only. Other fields (roleId, roleName, comments) are protected and cannot be modified."
        }

class UserRoleResponse(UserRoleBase):
    """Schema for role response with metadata"""
    createdDate: date = Field(..., description="Role creation date (auto-populated)")
    updatedDate: date = Field(..., description="Role last update date (auto-updated)")

    class Config:
        from_attributes = True
```

### 5.3 `app/schemas/location.py`
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    stateId: str = Field(..., max_length=10)
    stateName: str = Field(..., max_length=100)
    cityId: str = Field(..., max_length=10)
    cityName: str = Field(..., max_length=100)
    pinCode: str = Field(..., max_length=10)
    countryName: str = Field(default="India")
    status: str = Field(default="Active")

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    status: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    createdDate: datetime
    updatedDate: datetime

    class Config:
        from_attributes = True
```

### 5.4 `app/schemas/user.py`
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    firstName: str = Field(..., max_length=50)
    lastName: str = Field(..., max_length=50)
    currentRole: str = Field(..., max_length=50)
    emailId: EmailStr
    mobileNumber: str = Field(..., max_length=15)
    organisation: Optional[str] = None
    status: str = Field(default="Active")

class UserCreate(UserBase):
    userId: str = Field(..., max_length=100)
    address1: Optional[str] = None
    address2: Optional[str] = None
    stateName: Optional[str] = None
    cityName: Optional[str] = None
    pinCode: Optional[str] = None

class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    organisation: Optional[str] = None
    status: Optional[str] = None

class UserResponse(UserBase):
    userId: str
    address1: Optional[str]
    address2: Optional[str]
    stateName: Optional[str]
    cityName: Optional[str]
    pinCode: Optional[str]
    createdDate: datetime

    class Config:
        from_attributes = True
```

### 5.5 `app/schemas/user_login.py`
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserLoginBase(BaseModel):
    username: str = Field(..., max_length=100)
    roleId: Optional[str] = None
    isActive: bool = Field(default=True)

class UserLoginCreate(UserLoginBase):
    userId: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8)

class UserLoginUpdate(BaseModel):
    password: Optional[str] = None
    isActive: Optional[bool] = None

class UserLoginResponse(UserLoginBase):
    userId: str
    lastLoginAt: Optional[datetime] = None
    passwordLastChangedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
```

### 5.6 `app/schemas/registration.py`
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class RegistrationBase(BaseModel):
    userName: str = Field(..., max_length=100)
    firstName: str = Field(..., max_length=50)
    lastName: str = Field(..., max_length=50)
    currentRole: str = Field(..., max_length=50)
    emailId: EmailStr
    mobileNumber: str = Field(..., max_length=15)
    requestStatus: str = Field(default="Pending")

class RegistrationCreate(RegistrationBase):
    requestId: str = Field(..., max_length=20)
    organisation: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    stateName: Optional[str] = None
    cityName: Optional[str] = None
    pinCode: Optional[str] = None

class RegistrationUpdate(BaseModel):
    requestStatus: Optional[str] = None
    approvedBy: Optional[str] = None
    approvalRemarks: Optional[str] = None

class RegistrationResponse(RegistrationBase):
    requestId: str
    organisation: Optional[str]
    address1: Optional[str]
    createdDate: datetime

    class Config:
        from_attributes = True
```

### 5.7 `app/schemas/report.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class ReportBase(BaseModel):
    userId: str = Field(..., max_length=100)
    fileName: str = Field(..., max_length=255)
    fileType: str = Field(..., max_length=10)
    reportType: Optional[str] = None
    status: str = Field(default="Pending")

class ReportCreate(ReportBase):
    id: str = Field(..., max_length=50)
    inferredDiagnosis: Optional[str] = None
    pdfUrl: Optional[str] = None
    bucketLocation: Optional[str] = None
    jsonData: Optional[Any] = None

class ReportUpdate(BaseModel):
    status: Optional[str] = None
    inferredDiagnosis: Optional[str] = None
    jsonData: Optional[Any] = None

class ReportResponse(ReportBase):
    id: str
    timestamp: datetime
    inferredDiagnosis: Optional[str]
    pdfUrl: Optional[str]

    class Config:
        from_attributes = True
```

### 5.8 `app/schemas/__init__.py`
```python
from app.schemas.common import APIResponse, ErrorResponse
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate, UserRoleResponse
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.user_login import UserLoginCreate, UserLoginUpdate, UserLoginResponse
from app.schemas.registration import RegistrationCreate, RegistrationUpdate, RegistrationResponse
from app.schemas.report import ReportCreate, ReportUpdate, ReportResponse

__all__ = [
    "APIResponse",
    "ErrorResponse",
    "UserRoleCreate",
    "UserRoleUpdate",
    "UserRoleResponse",
    "LocationCreate",
    "LocationUpdate",
    "LocationResponse",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLoginCreate",
    "UserLoginUpdate",
    "UserLoginResponse",
    "RegistrationCreate",
    "RegistrationUpdate",
    "RegistrationResponse",
    "ReportCreate",
    "ReportUpdate",
    "ReportResponse",
]
```

### 5.3 `app/schemas/user.py` - User_Master Schemas (Enhanced Schema v2.0)

**Updated March 1, 2026** ✅ - BIGINT userId, Email RFC 5322 validation, 10-digit mobile

```python
"""
User_Master Pydantic Schemas - Enhanced Schema v2.0
- Email validation: RFC 5322 regex pattern
- Mobile validation: NUMERIC(10), range 1000000000-9999999999 (10 digits)
- userId: BIGINT (1-1000000000)
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# ============================================================================
# Schema 1: UserCreate (POST request)
# ============================================================================
class UserCreate(BaseModel):
    """
    Create user request schema with enhanced validation.
    System-managed fields are auto-populated:
    - createdDate: Set to current timestamp
    - updatedDate: Set to current timestamp
    """
    userId: int = Field(..., ge=1, le=1000000000, description="Numeric User ID (BIGINT, 1-1000000000)")
    firstName: str = Field(..., max_length=100, description="First name")
    lastName: str = Field(..., max_length=100, description="Last name")
    currentRole: str = Field(..., max_length=50, description="Role ID (must reference User_Role_Master)")
    emailId: EmailStr = Field(..., description="Email address (RFC 5322 validated)")
    mobileNumber: str = Field(..., description="Mobile number (exactly 10 digits)")
    organisation: Optional[str] = Field(None, max_length=255, description="Organization name")
    address: Optional[str] = Field(None, description="Full address")
    status: str = Field(default="Active", pattern="^(Active|Inactive|Suspended)$", description="Account status")

    @field_validator('mobileNumber')
    @classmethod
    def validate_mobile(cls, v):
        """Validate mobile: exactly 10 digits in range 1000000000-9999999999"""
        if len(v) != 10 or not v.isdigit():
            raise ValueError('Mobile number must be exactly 10 digits')

        mobile_int = int(v)
        if mobile_int < 1000000000 or mobile_int > 9999999999:
            raise ValueError('Mobile number must be in range 1000000000-9999999999')

        return v

    class Config:
        schema_extra = {
            "example": {
                "userId": 1001,
                "firstName": "John",
                "lastName": "Doe",
                "currentRole": "DOCTOR",
                "emailId": "john.doe@medostel.com",
                "mobileNumber": "9876543210",
                "organisation": "Apollo Hospital",
                "address": "Mumbai, India",
                "status": "Active"
            }
        }


# ============================================================================
# Schema 2: UserUpdate (PUT request - all fields optional)
# ============================================================================
class UserUpdate(BaseModel):
    """
    Update user request schema.

    Updateable Fields: All except userId, createdDate, updatedDate
    - updatedDate: Auto-set to current timestamp

    Immutable Fields: Cannot be modified
    - userId: BIGINT primary key cannot change
    - createdDate: Original creation timestamp preserved
    """
    firstName: Optional[str] = Field(None, max_length=100)
    lastName: Optional[str] = Field(None, max_length=100)
    currentRole: Optional[str] = Field(None, max_length=50)
    emailId: Optional[EmailStr] = Field(None, description="Email (RFC 5322 validated)")
    mobileNumber: Optional[str] = Field(None, description="Mobile (exactly 10 digits)")
    organisation: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None)
    status: Optional[str] = Field(None, pattern="^(Active|Inactive|Suspended)$")
    userId: Optional[int] = Field(None, description="⚠️ IMMUTABLE - Cannot be modified")

    @field_validator('mobileNumber')
    @classmethod
    def validate_mobile(cls, v):
        """Validate mobile if provided: exactly 10 digits in range 1000000000-9999999999"""
        if v is not None:
            if len(v) != 10 or not v.isdigit():
                raise ValueError('Mobile number must be exactly 10 digits')

            mobile_int = int(v)
            if mobile_int < 1000000000 or mobile_int > 9999999999:
                raise ValueError('Mobile number must be in range 1000000000-9999999999')

        return v

    class Config:
        schema_extra = {
            "example": {
                "firstName": "Jonathan",
                "emailId": "jonathan.doe@medostel.com",
                "status": "Active"
            }
        }


# ============================================================================
# Schema 3: UserResponse (API response)
# ============================================================================
class UserResponse(BaseModel):
    """
    User response schema - returned from API calls.
    Includes all fields plus auto-managed timestamps.
    """
    userId: int = Field(..., description="Numeric User ID (BIGINT)")
    firstName: str
    lastName: str
    currentRole: str
    emailId: str
    mobileNumber: str = Field(..., description="10-digit mobile")
    organisation: Optional[str]
    address: Optional[str]
    status: str
    createdDate: datetime = Field(..., description="Auto-populated at creation")
    updatedDate: datetime = Field(..., description="Auto-updated on modifications")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "userId": 1001,
                "firstName": "John",
                "lastName": "Doe",
                "currentRole": "DOCTOR",
                "emailId": "john.doe@medostel.com",
                "mobileNumber": "9876543210",
                "organisation": "Apollo Hospital",
                "address": "Mumbai, India",
                "status": "Active",
                "createdDate": "2026-03-01T10:00:00",
                "updatedDate": "2026-03-01T12:00:00"
            }
        }
```

---

## Step 6: Create Services Layer

### 6.1 `app/services/user_role_service.py` - Enhanced User_Role_Master Service

**Updated March 1, 2026** ✅ - Status-only updates, no delete operation

```python
"""
Service layer for User_Role_Master operations
Handles business logic for role management APIs
"""

import logging
from typing import List, Optional
from datetime import date

logger = logging.getLogger(__name__)

class UserRoleService:
    """Service for User_Role_Master operations with enhanced validation"""

    @staticmethod
    async def get_role_by_id(db, role_id: str):
        """
        Fetch a single role by ID (case-sensitive, assumes ID already converted to uppercase)

        Args:
            db: Database connection
            role_id: Role ID to fetch (should be uppercase)

        Returns:
            Role record or None if not found
        """
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_role_master WHERE roleId = %s"
            cursor.execute(query, (role_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error retrieving role by ID {role_id}: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_all_roles(db, status: Optional[str] = None, limit: int = 100, offset: int = 0):
        """
        Retrieve all user roles with optional status filtering and pagination

        Supports two scenarios:
        1. Filter by status (Active, Inactive, Pending)
        2. Return all roles regardless of status

        Args:
            db: Database connection
            status: Optional status filter (Active, Inactive, Pending)
            limit: Maximum records to return (1-1000, default 100)
            offset: Pagination offset (default 0)

        Returns:
            List of role records
        """
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_role_master"
            params = []

            # Add status filter if provided
            if status:
                query += " WHERE status = %s"
                params.append(status)

            # Add pagination
            query += " ORDER BY createdDate DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            roles = cursor.fetchall()
            return roles
        except Exception as e:
            logger.error(f"Error retrieving roles: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_role(db, role_data: dict):
        """
        Create a new user role with auto-populated timestamps

        Auto-populated fields:
        - createdDate: Set to CURRENT_DATE
        - updatedDate: Set to CURRENT_DATE

        Args:
            db: Database connection
            role_data: Dictionary containing:
                - roleId: Unique role ID (should already be uppercase)
                - roleName: Human-readable role name
                - status: Role status (Active, Inactive, Closed)
                - comments: Optional role description

        Returns:
            Created role record with all fields

        Raises:
            Exception: If role creation fails
        """
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO user_role_master
                (roleId, roleName, status, comments, createdDate, updatedDate)
                VALUES (%s, %s, %s, %s, CURRENT_DATE, CURRENT_DATE)
                RETURNING *
            """
            cursor.execute(query, (
                role_data['roleId'],           # Already uppercase from route
                role_data['roleName'],
                role_data.get('status', 'Active'),
                role_data.get('comments')
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Role '{role_data['roleId']}' created successfully")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_role(db, role_id: str, role_data: dict):
        """
        Update user role - STATUS FIELD ONLY

        Protected fields (cannot be updated):
        - roleId: Cannot be changed
        - roleName: Cannot be changed
        - comments: Cannot be changed

        Auto-updated field:
        - updatedDate: Set to CURRENT_DATE

        Args:
            db: Database connection
            role_id: Role ID to update (should already be uppercase)
            role_data: Dictionary containing ONLY:
                - status: New status value (Active, Inactive, Closed)

        Returns:
            Updated role record with new status and updatedDate

        Raises:
            Exception: If update fails
        """
        cursor = db.cursor()
        try:
            # Only status field is allowed to be updated
            if 'status' not in role_data:
                raise ValueError("status field is required for role update")

            query = """
                UPDATE user_role_master
                SET status = %s, updatedDate = CURRENT_DATE
                WHERE roleId = %s
                RETURNING *
            """

            cursor.execute(query, (
                role_data['status'],
                role_id
            ))
            db.commit()
            result = cursor.fetchone()

            if result:
                logger.info(f"Role '{role_id}' status updated to '{role_data['status']}'")
            else:
                logger.warning(f"Role '{role_id}' not found for update")

            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating role {role_id}: {e}")
            raise
        finally:
            cursor.close()

    # ========================================================================
    # DELETE OPERATION NOT SUPPORTED
    # ========================================================================
    # Roles cannot be deleted from the system. Use status update to deactivate.
    # The delete_role method has been removed as of March 1, 2026.
```

### 6.2 `app/services/user_service.py` - User_Master Service (Enhanced Schema v2.0)

**Updated March 1, 2026** ✅ - BIGINT userId, Email RFC 5322, 10-digit mobile

```python
"""
User_Master Service Layer - Business Logic for User Management
Handles all database operations for User_Master table with enhanced schema v2.0
"""

from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service class for User_Master operations"""

    @staticmethod
    async def get_user_by_id(db, userId: int):
        """
        Fetch user by numeric userId (BIGINT)
        Args:
            db: Database connection
            userId: Numeric user ID (1-1000000000)
        Returns:
            User object or None
        """
        try:
            cursor = db.cursor()
            cursor.execute(
                """
                SELECT userId, firstName, lastName, currentRole, emailId, mobileNumber,
                       organisation, address, status, createdDate, updatedDate
                FROM user_master
                WHERE userId = %s
                """
            , (userId,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return {
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching user {userId}: {e}")
            raise

    @staticmethod
    async def get_user_by_email(db, email: str):
        """
        Fetch user by email (RFC 5322 validated)
        Args:
            db: Database connection
            email: Email address
        Returns:
            User object or None
        """
        try:
            cursor = db.cursor()
            cursor.execute(
                """
                SELECT userId, firstName, lastName, currentRole, emailId, mobileNumber,
                       organisation, address, status, createdDate, updatedDate
                FROM user_master
                WHERE emailId = %s
                """
            , (email,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return {
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching user with email {email}: {e}")
            raise

    @staticmethod
    async def get_user_by_mobile(db, mobile: str):
        """
        Fetch user by mobile number (10 digits)
        Args:
            db: Database connection
            mobile: Mobile number (exactly 10 digits)
        Returns:
            User object or None
        """
        try:
            cursor = db.cursor()
            cursor.execute(
                """
                SELECT userId, firstName, lastName, currentRole, emailId, mobileNumber,
                       organisation, address, status, createdDate, updatedDate
                FROM user_master
                WHERE mobileNumber = %s
                """
            , (int(mobile),))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return {
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching user with mobile {mobile}: {e}")
            raise

    @staticmethod
    async def get_all_users(db, limit: int = 100, offset: int = 0):
        """
        Fetch all users with pagination
        Args:
            db: Database connection
            limit: Maximum number of records (default: 100, max: 1000)
            offset: Pagination offset (default: 0)
        Returns:
            List of user objects
        """
        try:
            cursor = db.cursor()
            cursor.execute(
                """
                SELECT userId, firstName, lastName, currentRole, emailId, mobileNumber,
                       organisation, address, status, createdDate, updatedDate
                FROM user_master
                ORDER BY userId DESC
                LIMIT %s OFFSET %s
                """
            , (limit, offset))
            results = cursor.fetchall()
            cursor.close()

            users = []
            for result in results:
                users.append({
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                })
            return users
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            raise

    @staticmethod
    async def get_users_by_role_status(db, role: Optional[str] = None, status: Optional[str] = None,
                                       limit: int = 100, offset: int = 0):
        """
        Fetch users filtered by role and/or status
        Args:
            db: Database connection
            role: Role ID to filter by
            status: Status to filter by (Active/Inactive/Suspended)
            limit: Maximum number of records
            offset: Pagination offset
        Returns:
            List of user objects
        """
        try:
            query = """
                SELECT userId, firstName, lastName, currentRole, emailId, mobileNumber,
                       organisation, address, status, createdDate, updatedDate
                FROM user_master
                WHERE 1=1
            """
            params = []

            if role:
                query += " AND currentRole = %s"
                params.append(role)

            if status:
                query += " AND status = %s"
                params.append(status)

            query += " ORDER BY userId DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor = db.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            users = []
            for result in results:
                users.append({
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                })
            return users
        except Exception as e:
            logger.error(f"Error fetching users by role/status: {e}")
            raise

    @staticmethod
    async def create_user(db, user_data: dict):
        """
        Create new user with schema v2.0 validation
        System-managed fields auto-populated:
        - createdDate: Current timestamp
        - updatedDate: Current timestamp

        Args:
            db: Database connection
            user_data: User data dict with validated fields
        Returns:
            Created user object
        """
        try:
            now = datetime.now()
            cursor = db.cursor()

            cursor.execute(
                """
                INSERT INTO user_master
                (userId, firstName, lastName, currentRole, emailId, mobileNumber,
                 organisation, address, status, createdDate, updatedDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING userId, firstName, lastName, currentRole, emailId, mobileNumber,
                          organisation, address, status, createdDate, updatedDate
                """,
                (
                    user_data["userId"],
                    user_data["firstName"],
                    user_data["lastName"],
                    user_data["currentRole"],
                    user_data["emailId"],
                    int(user_data["mobileNumber"]),
                    user_data.get("organisation"),
                    user_data.get("address"),
                    user_data.get("status", "Active"),
                    now,
                    now
                )
            )

            result = cursor.fetchone()
            cursor.close()
            db.commit()

            if result:
                return {
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                }
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {e}")
            raise

    @staticmethod
    async def update_user(db, userId: int, update_data: dict):
        """
        Update user profile with field validation
        - Prevents userId modification (immutable)
        - Auto-updates updatedDate to current timestamp
        - Other fields validated per schema v2.0

        Args:
            db: Database connection
            userId: Numeric user ID (BIGINT)
            update_data: Fields to update
        Returns:
            Updated user object
        """
        try:
            now = datetime.now()
            cursor = db.cursor()

            # Build dynamic update query
            update_fields = []
            params = []

            if "firstName" in update_data and update_data["firstName"] is not None:
                update_fields.append("firstName = %s")
                params.append(update_data["firstName"])

            if "lastName" in update_data and update_data["lastName"] is not None:
                update_fields.append("lastName = %s")
                params.append(update_data["lastName"])

            if "currentRole" in update_data and update_data["currentRole"] is not None:
                update_fields.append("currentRole = %s")
                params.append(update_data["currentRole"])

            if "emailId" in update_data and update_data["emailId"] is not None:
                update_fields.append("emailId = %s")
                params.append(update_data["emailId"])

            if "mobileNumber" in update_data and update_data["mobileNumber"] is not None:
                update_fields.append("mobileNumber = %s")
                params.append(int(update_data["mobileNumber"]))

            if "organisation" in update_data and update_data["organisation"] is not None:
                update_fields.append("organisation = %s")
                params.append(update_data["organisation"])

            if "address" in update_data and update_data["address"] is not None:
                update_fields.append("address = %s")
                params.append(update_data["address"])

            if "status" in update_data and update_data["status"] is not None:
                update_fields.append("status = %s")
                params.append(update_data["status"])

            # Always update updatedDate
            update_fields.append("updatedDate = %s")
            params.append(now)

            params.append(userId)

            query = f"""
                UPDATE user_master
                SET {', '.join(update_fields)}
                WHERE userId = %s
                RETURNING userId, firstName, lastName, currentRole, emailId, mobileNumber,
                          organisation, address, status, createdDate, updatedDate
            """

            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            db.commit()

            if result:
                return {
                    "userId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "currentRole": result[3],
                    "emailId": result[4],
                    "mobileNumber": str(result[5]),
                    "organisation": result[6],
                    "address": result[7],
                    "status": result[8],
                    "createdDate": result[9],
                    "updatedDate": result[10]
                }
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user {userId}: {e}")
            raise
```

### 6.3 `app/services/__init__.py`
```python
from app.services.user_role_service import UserRoleService
from app.services.user_service import UserService

__all__ = [
    "UserRoleService",
    "UserService",
]
```

---

## Step 7: Create Routes

### 7.1 `app/routes/v1/roles.py` - Enhanced User_Role_Master APIs

**Updated March 1, 2026** ✅ - Enhanced with flexible GET scenarios and status-only updates

```python
"""
API routes for User_Role_Master table (APIs 1 & 2)
SELECT operations (API 1) and CRUD operations (API 2)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime
from app.database import get_db
from app.services.user_role_service import UserRoleService
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate, UserRoleResponse
from app.schemas.common import APIResponse
from app.constants import ErrorCodes, HTTPStatus

router = APIRouter(prefix="/roles", tags=["User Roles"])


# ============================================================================
# API 1: SELECT - Get all user roles with flexible filtering
# ============================================================================

@router.get("/all", response_model=APIResponse)
async def get_all_roles(
    db=Depends(get_db),
    roleId: str = Query(None, description="Fetch by specific Role ID (converted to uppercase)"),
    status: str = Query(None, description="Filter by role status (Active, Inactive, Pending)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    API 1: SELECT Operation - Retrieve user roles with flexible filtering

    Supports three request scenarios:

    1. **Request with roleId parameter**:
       - Fetch all details for a specific role by ID
       - Role ID is automatically converted to UPPERCASE for case-insensitive matching
       - Example: ?roleId=admin → fetches ADMIN role

    2. **Request with status parameter**:
       - Fetch all roles with a specific status
       - Valid values: Active, Inactive, Pending
       - Example: ?status=Active → fetches all active roles

    3. **Request with no parameters**:
       - Fetch all roles from User_Role_Master table
       - Returns all columns and all rows irrespective of status
       - Example: /api/v1/roles/all → fetches all roles
    """
    try:
        # Scenario 1: Fetch by specific Role ID (case-insensitive)
        if roleId:
            # Convert roleId to uppercase for case-insensitive matching
            roleId_upper = roleId.upper()
            role = await UserRoleService.get_role_by_id(db, roleId_upper)

            if not role:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Role with ID '{roleId}' not found"
                )

            return APIResponse(
                status="success",
                code=HTTPStatus.OK,
                message=f"Role '{roleId_upper}' retrieved successfully",
                data={"roles": [role], "count": 1, "scenario": "Fetch by Role ID"},
                timestamp=datetime.now()
            )

        # Scenario 2: Fetch by status or Scenario 3: Fetch all
        roles = await UserRoleService.get_all_roles(db, status, limit, offset)

        scenario_message = "Fetch all roles with status filter" if status else "Fetch all roles"
        detail_message = f"Retrieved {len(roles)} role(s) with status '{status}'" if status else "Retrieved all roles from User_Role_Master"

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=detail_message,
            data={"roles": roles, "count": len(roles), "scenario": scenario_message},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# API 2: CRUD - Create role (Insert)
# ============================================================================

@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_role(
    role: UserRoleCreate,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Insert new user role

    **Request Scenario: Insert New Role**

    Input required:
    - roleId: Unique role identifier (max 10 chars, uppercase)
    - roleName: Human-readable role name (max 50 chars)
    - status: Role status (Active, Inactive, or Closed)
    - comments: Optional description (max 250 chars)

    System-generated fields (auto-populated):
    - createdDate: Set to current system timestamp
    - updatedDate: Set to current system timestamp

    Returns: Created role with all fields including timestamps
    """
    try:
        # Check if role already exists
        role_id_upper = role.roleId.upper()
        existing = await UserRoleService.get_role_by_id(db, role_id_upper)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Role '{role_id_upper}' already exists"
            )

        # Validate status is one of the allowed values
        allowed_statuses = ["Active", "Inactive", "Closed"]
        if role.status not in allowed_statuses:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(allowed_statuses)}"
            )

        # Create role data with uppercase roleId
        role_data = role.dict()
        role_data['roleId'] = role_id_upper

        # createdDate and updatedDate are auto-set to current timestamp in the service layer
        new_role = await UserRoleService.create_role(db, role_data)

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Role created successfully",
            data={
                "role": new_role,
                "scenario": "Insert new role",
                "info": "createdDate and updatedDate set to current system timestamp"
            },
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# ============================================================================
# API 2: CRUD - Update role (Status Update only)
# ============================================================================

@router.put("/{roleId}", response_model=APIResponse)
async def update_role(
    roleId: str,
    status_update: dict,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Update user role status

    **Request Scenario: Update Role Status**

    URL Parameter:
    - roleId: The role ID to update (will be converted to uppercase)

    Input required:
    - status: New status value (must be one of: Active, Inactive, Closed)

    System-managed fields:
    - updatedDate: Automatically set to current system timestamp
    - Other fields (roleId, roleName, comments): Cannot be updated through this endpoint

    Returns: Updated role with new status and updated timestamp
    """
    try:
        # Convert roleId to uppercase for consistency
        role_id_upper = roleId.upper()

        # Check if role exists
        existing = await UserRoleService.get_role_by_id(db, role_id_upper)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Role '{role_id_upper}' not found"
            )

        # Extract status from request body
        if "status" not in status_update:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Request body must contain 'status' field"
            )

        new_status = status_update.get("status")

        # Validate status is one of the allowed values
        allowed_statuses = ["Active", "Inactive", "Closed"]
        if new_status not in allowed_statuses:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(allowed_statuses)}. Received: '{new_status}'"
            )

        # Update only the status field
        update_data = {"status": new_status}
        updated_role = await UserRoleService.update_role(db, role_id_upper, update_data)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"Role '{role_id_upper}' status updated to '{new_status}' successfully",
            data={
                "role": updated_role,
                "scenario": "Update role status",
                "info": "updatedDate set to current system timestamp. Other fields cannot be modified."
            },
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# ============================================================================
# API 2: DELETE Operation
# ============================================================================
# ❌ DELETE operation is NOT SUPPORTED as of March 1, 2026
# Roles cannot be deleted from the system. Use status update to deactivate roles instead.
```

### 7.2 `app/routes/v1/users.py` - User_Master APIs (API 5 & 6 - Enhanced Schema v2.0)

**Updated March 1, 2026** ✅ - BIGINT userId, Email RFC 5322 validation, 10-digit mobile validation

```python
"""
User_Master API Routes - Enhanced Schema v2.0
- API 5: GET /api/v1/users/all (Flexible retrieval with filtering)
- API 6: POST /api/v1/users (Create user with validation)
- API 6: PUT /api/v1/users/{userId} (Update with field validation)
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional, List
from datetime import datetime
from http import HTTPStatus
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.schemas.common import APIResponse
from app.database.connection import get_db

router = APIRouter(prefix="/api/v1/users", tags=["User_Master"])

# ============================================================================
# API 5: GET /api/v1/users/all - Flexible User Retrieval (4 Scenarios)
# ============================================================================

@router.get("/all", response_model=APIResponse, status_code=HTTPStatus.OK)
async def get_users(
    userId: Optional[int] = Query(None, ge=1, le=1000000000, description="Numeric User ID (BIGINT)"),
    email: Optional[str] = Query(None, description="Email address (RFC 5322)"),
    role: Optional[str] = Query(None, description="Role ID"),
    status: Optional[str] = Query(None, pattern="^(Active|Inactive|Suspended)$"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db = Depends(get_db)
):
    """
    Retrieve users with flexible filtering options (4 scenarios):

    Scenario 1: Fetch by userId
    - GET /api/v1/users/all?userId=1001

    Scenario 2: Fetch by email (RFC 5322 validated)
    - GET /api/v1/users/all?email=john.doe@medostel.com

    Scenario 3: Filter by role and status
    - GET /api/v1/users/all?role=DOCTOR&status=Active

    Scenario 4: Fetch all with pagination
    - GET /api/v1/users/all?limit=10&offset=0
    """
    try:
        # Validate email format if provided
        if email:
            import re
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            if not re.match(email_pattern, email):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Email validation failed for: '{email}'"
                )

        # Determine which scenario to execute
        users = []
        count = 0
        scenario = "Fetch all users"

        if userId is not None:
            # Scenario 1: Fetch by userId
            users = await UserService.get_user_by_id(db, userId)
            if not users:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"User with ID '{userId}' not found"
                )
            users = [users]
            count = 1
            scenario = f"Fetch by userId {userId}"

        elif email:
            # Scenario 2: Fetch by email
            user = await UserService.get_user_by_email(db, email)
            if not user:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"User with email '{email}' not found"
                )
            users = [user]
            count = 1
            scenario = f"Fetch by email {email}"

        elif role or status:
            # Scenario 3: Filter by role and/or status
            users = await UserService.get_users_by_role_status(
                db, role, status, limit, offset
            )
            count = len(users)
            scenario = f"Filter by role={role}, status={status}"

        else:
            # Scenario 4: Fetch all with pagination
            users = await UserService.get_all_users(db, limit, offset)
            count = len(users)
            scenario = "Fetch all users with pagination"

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"Retrieved {count} user(s) successfully",
            data={
                "count": count,
                "scenario": scenario,
                "users": users
            },
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# API 6: POST /api/v1/users - Create User (Schema v2.0 Validation)
# ============================================================================

@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_user(
    user_data: UserCreate,
    db = Depends(get_db)
):
    """
    Create a new user with enhanced schema validation:

    Required Fields:
    - userId: BIGINT (1-1000000000)
    - firstName: str (max 100 chars)
    - lastName: str (max 100 chars)
    - currentRole: str (must reference User_Role_Master)
    - emailId: str (RFC 5322 format, unique)
    - mobileNumber: str (exactly 10 digits, 1000000000-9999999999)

    Optional Fields:
    - organisation: str
    - address: str
    - status: str (default: Active, values: Active/Inactive/Suspended)

    System-managed Fields (AUTO-POPULATED):
    - createdDate: current timestamp
    - updatedDate: current timestamp
    """
    try:
        # Validate userId range
        if user_data.userId < 1 or user_data.userId > 1000000000:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"userId must be between 1 and 1000000000"
            )

        # Validate mobile number (10 digits, range 1000000000-9999999999)
        if len(user_data.mobileNumber) != 10 or not user_data.mobileNumber.isdigit():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Mobile number must be exactly 10 digits"
            )

        mobile_int = int(user_data.mobileNumber)
        if mobile_int < 1000000000 or mobile_int > 9999999999:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Mobile number must be in range 1000000000-9999999999"
            )

        # Check for duplicate userId
        existing = await UserService.get_user_by_id(db, user_data.userId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User with ID {user_data.userId} already exists"
            )

        # Check for duplicate email
        existing = await UserService.get_user_by_email(db, user_data.emailId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Email '{user_data.emailId}' already in use"
            )

        # Check for duplicate mobile
        existing = await UserService.get_user_by_mobile(db, user_data.mobileNumber)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Mobile number '{user_data.mobileNumber}' already in use"
            )

        # Create user
        new_user = await UserService.create_user(db, user_data)

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message=f"User with ID {new_user.userId} created successfully",
            data=new_user,
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# API 6: PUT /api/v1/users/{userId} - Update User Profile
# ============================================================================

@router.put("/{userId}", response_model=APIResponse, status_code=HTTPStatus.OK)
async def update_user(
    userId: int = Query(..., ge=1, le=1000000000, description="Numeric User ID"),
    user_update: UserUpdate = None,
    db = Depends(get_db)
):
    """
    Update user profile with field-level validation:

    Updateable Fields:
    - firstName, lastName: str
    - currentRole: str (must reference User_Role_Master)
    - emailId: str (RFC 5322 format, unique)
    - mobileNumber: str (10 digits, 1000000000-9999999999)
    - organisation: str
    - address: str
    - status: str (Active/Inactive/Suspended)

    Immutable Fields (CANNOT be modified):
    - userId: Prevents modification
    - createdDate: Auto-managed
    - updatedDate: Auto-updated to current timestamp
    """
    try:
        # Check if user exists
        existing = await UserService.get_user_by_id(db, userId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User with ID {userId} not found"
            )

        # Prevent userId modification
        if user_update.userId is not None and user_update.userId != userId:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Cannot modify immutable field 'userId'"
            )

        # Validate email if provided
        if user_update.emailId:
            import re
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            if not re.match(email_pattern, user_update.emailId):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Email validation failed: '{user_update.emailId}'"
                )

            # Check email uniqueness (if different from current)
            if user_update.emailId != existing.emailId:
                dup = await UserService.get_user_by_email(db, user_update.emailId)
                if dup:
                    raise HTTPException(
                        status_code=HTTPStatus.CONFLICT,
                        detail=f"Email '{user_update.emailId}' already in use"
                    )

        # Validate mobile if provided
        if user_update.mobileNumber:
            if len(user_update.mobileNumber) != 10 or not user_update.mobileNumber.isdigit():
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Mobile number must be exactly 10 digits"
                )

            mobile_int = int(user_update.mobileNumber)
            if mobile_int < 1000000000 or mobile_int > 9999999999:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Mobile number must be in range 1000000000-9999999999"
                )

            # Check mobile uniqueness (if different from current)
            if user_update.mobileNumber != existing.mobileNumber:
                dup = await UserService.get_user_by_mobile(db, user_update.mobileNumber)
                if dup:
                    raise HTTPException(
                        status_code=HTTPStatus.CONFLICT,
                        detail=f"Mobile number '{user_update.mobileNumber}' already in use"
                    )

        # Validate status if provided
        if user_update.status:
            valid_statuses = ["Active", "Inactive", "Suspended"]
            if user_update.status not in valid_statuses:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Status must be one of: {', '.join(valid_statuses)}"
                )

        # Update user
        updated_user = await UserService.update_user(db, userId, user_update)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"User profile updated successfully. updatedDate auto-set to current timestamp.",
            data=updated_user,
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```

---

### 7.3 `app/routes/v1/__init__.py`
```python
# This file is intentionally left empty for package initialization
```

---

## Step 8: Update Main Application

Update `app/main.py` to include routers:

```python
"""
Medostel API Backend - Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.routes.v1 import roles, users  # API 1-2 (Roles), API 5-6 (Users)
from app.config import settings
from app.database import close_db

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events"""
    # Startup
    logger.info("Medostel API Starting...")
    yield
    # Shutdown
    logger.info("Medostel API Shutting down...")
    close_db()

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description="Healthcare AI Assistant - RESTful API",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Medostel API is running",
        "version": settings.API_VERSION
    }

@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "status": "ready",
        "message": "Medostel API is ready to serve traffic"
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Medostel Healthcare API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "endpoints": {
            "roles": "/api/v1/roles",
            "locations": "/api/v1/locations",
            "users": "/api/v1/users",
            "auth": "/api/v1/auth",
            "registrations": "/api/v1/requests",
            "reports": "/api/v1/reports"
        }
    }

# Include routers (uncomment as you create them)
app.include_router(roles.router, prefix="/api/v1", tags=["Roles"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
# app.include_router(locations.router, prefix="/api/v1", tags=["Locations"])
# app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
# app.include_router(registrations.router, prefix="/api/v1", tags=["Registrations"])
# app.include_router(reports.router, prefix="/api/v1", tags=["Reports"])

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return {
        "status": "error",
        "code": exc.status_code,
        "message": exc.detail,
        "path": str(request.url)
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "status": "error",
        "code": 500,
        "message": "Internal server error",
        "path": str(request.url)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

---

## Step 9: Run Development Server

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API Documentation
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

---

## Step 10: Create Docker Setup

### 10.1 Update `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -m httpx http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 10.2 Create `docker-compose.yml`
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel
      - SECRET_KEY=your-secret-key
      - DEBUG=False
    volumes:
      - .:/app
    depends_on:
      - postgres
    networks:
      - medostel-network

  postgres:
    image: postgres:18-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: medostel
      POSTGRES_USER: medostel_api_user
      POSTGRES_PASSWORD: Iag2bMi@0@6aD
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - medostel-network

networks:
  medostel-network:
    driver: bridge

volumes:
  postgres_data:
```

---

## Step 11: Test APIs

### 11.1 Basic API Test
```bash
# Health check
curl http://localhost:8000/health

# Create a role
curl -X POST http://localhost:8000/api/v1/roles \
  -H "Content-Type: application/json" \
  -d '{
    "roleId": "TST01",
    "roleName": "Test Role",
    "status": "Active",
    "comments": "Test role"
  }'

# Get all roles
curl http://localhost:8000/api/v1/roles/all
```

---

## Step 12: Deployment to Cloud Run

```bash
# Build and push to Google Container Registry
docker build -t gcr.io/gen-lang-client-0064186167/medostel-api:latest .
docker push gcr.io/gen-lang-client-0064186167/medostel-api:latest

# Deploy to Cloud Run
gcloud run deploy medostel-api \
  --image gcr.io/gen-lang-client-0064186167/medostel-api:latest \
  --platform managed \
  --region asia-south1 \
  --project gen-lang-client-0064186167 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel
```

---

## Implementation Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Directory structure created
- [ ] Config files implemented
- [ ] Database connection implemented
- [ ] Schemas created (all 6 files)
- [ ] Services created (start with user_role_service)
- [ ] Routes created (start with roles.py)
- [ ] Main application updated with routers
- [ ] Development server tested
- [ ] API endpoints verified on /docs
- [ ] Docker setup tested
- [ ] Cloud Run deployment successful

---

**Last Updated**: 2026-03-01 (Added User_Master implementation - Schema v2.0)
**Status**: APIs 1-2 & 5-6 Complete - Ready for Implementation
**Implementation Coverage**:
- ✅ Section 5.2: user_role.py schemas (User_Role_Master)
- ✅ Section 5.3: user.py schemas (User_Master - Enhanced Schema v2.0)
- ✅ Section 6.1: user_role_service.py (User_Role_Master service)
- ✅ Section 6.2: user_service.py (User_Master service - Schema v2.0)
- ✅ Section 7.1: roles.py routes (API 1 & 2)
- ✅ Section 7.2: users.py routes (API 5 & 6 - Schema v2.0)
- ✅ Step 8: main.py with both routers imported and registered
**Total APIs to Implement**: 12 (6 tables × 2 APIs each)
