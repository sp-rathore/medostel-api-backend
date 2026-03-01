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
├── SETUP.md                            # Setup instructions
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

| API # | Table | Module | Route | Service |
|-------|-------|--------|-------|---------|
| 1 | User_Role_Master | roles.py | GET /api/v1/roles/all | user_role_service |
| 2 | User_Role_Master | roles.py | POST/PUT/DELETE /api/v1/roles | user_role_service |
| 3 | State_City_PinCode | locations.py | GET /api/v1/locations/all | location_service |
| 4 | State_City_PinCode | locations.py | POST/PUT/DELETE /api/v1/locations | location_service |
| 5 | User_Master | users.py | GET /api/v1/users/all | user_service |
| 6 | User_Master | users.py | POST/PUT/DELETE /api/v1/users | user_service |
| 7 | User_Login | auth.py | GET /api/v1/auth/users | auth_service |
| 8 | User_Login | auth.py | POST/PUT/DELETE /api/v1/auth/credentials | auth_service |
| 9 | New_User_Request | registrations.py | GET /api/v1/requests/all | registration_service |
| 10 | New_User_Request | registrations.py | POST/PUT/DELETE /api/v1/requests | registration_service |
| 11 | Report_History | reports.py | GET /api/v1/reports/all | report_service |
| 12 | Report_History | reports.py | POST/PUT/DELETE /api/v1/reports | report_service |

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

**Last Updated**: 2026-02-28
**Created By**: Claude Code
**Status**: Structure Defined - Ready for Implementation
**Total APIs**: 12 (6 tables × 2 APIs each)
