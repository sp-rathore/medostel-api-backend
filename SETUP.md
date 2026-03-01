# Medostel API Backend - Setup & Implementation Guide

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

### 5.2 `app/schemas/user_role.py`
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UserRoleBase(BaseModel):
    roleId: str = Field(..., max_length=10)
    roleName: str = Field(..., max_length=50)
    status: str = Field(default="Active")
    comments: Optional[str] = Field(None, max_length=250)

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleUpdate(BaseModel):
    status: Optional[str] = None
    comments: Optional[str] = None

class UserRoleResponse(UserRoleBase):
    createdDate: date
    updatedDate: date

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

### 6.1 `app/services/user_role_service.py`
```python
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class UserRoleService:
    """Service for User_Role_Master operations"""

    @staticmethod
    async def get_all_roles(db, status: Optional[str] = None, limit: int = 100, offset: int = 0):
        """Retrieve all user roles with optional filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_role_master"
            params = []

            if status:
                query += " WHERE status = %s"
                params.append(status)

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
        """Create new user role"""
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO user_role_master
                (roleId, roleName, status, createdDate, updatedDate, comments)
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_DATE, %s)
                RETURNING *
            """
            cursor.execute(query, (
                role_data['roleId'],
                role_data['roleName'],
                role_data.get('status', 'Active'),
                role_data.get('comments')
            ))
            db.commit()
            return cursor.fetchone()
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_role(db, role_id: str, role_data: dict):
        """Update existing user role"""
        cursor = db.cursor()
        try:
            query = "UPDATE user_role_master SET "
            updates = []
            params = []

            if 'status' in role_data:
                updates.append("status = %s")
                params.append(role_data['status'])

            if 'comments' in role_data:
                updates.append("comments = %s")
                params.append(role_data['comments'])

            if not updates:
                return await UserRoleService.get_role_by_id(db, role_id)

            query += ", ".join(updates) + ", updatedDate = CURRENT_DATE"
            query += " WHERE roleId = %s RETURNING *"
            params.append(role_id)

            cursor.execute(query, params)
            db.commit()
            return cursor.fetchone()
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_role(db, role_id: str):
        """Delete user role"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM user_role_master WHERE roleId = %s"
            cursor.execute(query, (role_id,))
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_role_by_id(db, role_id: str):
        """Get role by ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_role_master WHERE roleId = %s"
            cursor.execute(query, (role_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
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

### 7.1 `app/routes/v1/roles.py`
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db
from app.services.user_role_service import UserRoleService
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate, UserRoleResponse
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter(prefix="/roles", tags=["User Roles"])

# API 1: SELECT - Get all user roles
@router.get("/all", response_model=APIResponse)
async def get_all_roles(
    db = Depends(get_db),
    status: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Retrieve all user roles (SELECT API)"""
    try:
        roles = await UserRoleService.get_all_roles(db, status, limit, offset)
        return APIResponse(
            status="success",
            code=200,
            message="User roles retrieved successfully",
            data={"roles": roles},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API 2: CRUD - Create role
@router.post("", response_model=APIResponse)
async def create_role(role: UserRoleCreate, db = Depends(get_db)):
    """Create new user role (CRUD API)"""
    try:
        new_role = await UserRoleService.create_role(db, role.dict())
        return APIResponse(
            status="success",
            code=201,
            message="Role created successfully",
            data={"role": new_role},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API 2: CRUD - Update role
@router.put("/{roleId}", response_model=APIResponse)
async def update_role(roleId: str, role: UserRoleUpdate, db = Depends(get_db)):
    """Update user role (CRUD API)"""
    try:
        updated_role = await UserRoleService.update_role(db, roleId, role.dict(exclude_unset=True))
        if not updated_role:
            raise HTTPException(status_code=404, detail="Role not found")
        return APIResponse(
            status="success",
            code=200,
            message="Role updated successfully",
            data={"role": updated_role},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API 2: CRUD - Delete role
@router.delete("/{roleId}", response_model=APIResponse)
async def delete_role(roleId: str, db = Depends(get_db)):
    """Delete user role (CRUD API)"""
    try:
        success = await UserRoleService.delete_role(db, roleId)
        if not success:
            raise HTTPException(status_code=404, detail="Role not found")
        return APIResponse(
            status="success",
            code=204,
            message="Role deleted successfully",
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
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
