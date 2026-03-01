# Medostel API Backend - Setup & Implementation Guide

---

## ⭐ Latest Enhancements (March 1, 2026)

### User_Role_Master APIs (API 1 & 2) - Major Improvements

The User_Role_Master implementation has been significantly enhanced to provide flexible role management:

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

### 6.2 `app/services/__init__.py`
```python
from app.services.user_role_service import UserRoleService

__all__ = [
    "UserRoleService",
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

### 7.2 `app/routes/v1/__init__.py`
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
from app.routes.v1 import roles  # Import when ready
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
# app.include_router(locations.router, prefix="/api/v1", tags=["Locations"])
# app.include_router(users.router, prefix="/api/v1", tags=["Users"])
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

**Last Updated**: 2026-02-28
**Status**: Ready for Step-by-Step Implementation
**Total APIs to Implement**: 12 (6 tables × 2 APIs each)
