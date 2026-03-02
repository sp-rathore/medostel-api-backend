# Medostel API Backend - Complete Structure Guide

## Repository Structure Overview

```
medostel-api-backend/
│
├── 📄 README.md                          # Project overview
├── 📄 PROJECT_STRUCTURE.md               # Detailed structure documentation
├── 📄 APISETUP.md                           # Step-by-step setup guide
├── 📄 API_STRUCTURE_GUIDE.md             # This file - visual guide
├── 📄 requirements.txt                   # Python dependencies
├── 📄 Dockerfile                         # Docker container config
├── 📄 docker-compose.yml                 # Docker compose for local dev
├── 📄 Makefile                           # Development commands
├── 📄 .gitignore                         # Git ignore rules
├── 📄 .env.example                       # Environment variables template
├── 📄 .env                               # Environment variables (local)
│
├── 📁 app/                               # Main application package
│   ├── 📄 __init__.py
│   ├── 📄 main.py                        # FastAPI application entry point
│   ├── 📄 config.py                      # Configuration management
│   ├── 📄 constants.py                   # Error codes, status, roles
│   │
│   ├── 📁 database/                      # Database layer
│   │   ├── 📄 __init__.py
│   │   ├── 📄 connection.py              # Connection pooling
│   │   └── 📄 models.py                  # SQLAlchemy ORM models
│   │
│   ├── 📁 middleware/                    # Request/Response middleware
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth.py                    # Authentication middleware
│   │   ├── 📄 error_handler.py           # Error handling middleware
│   │   └── 📄 logging.py                 # Logging middleware
│   │
│   ├── 📁 security/                      # Security utilities
│   │   ├── 📄 __init__.py
│   │   ├── 📄 jwt.py                     # JWT token management
│   │   ├── 📄 password.py                # Password hashing/verification
│   │   └── 📄 rbac.py                    # Role-based access control
│   │
│   ├── 📁 schemas/                       # Pydantic request/response models
│   │   ├── 📄 __init__.py
│   │   ├── 📄 common.py                  # Common response models
│   │   ├── 📄 user_role.py               # User_Role_Master schemas
│   │   ├── 📄 location.py                # State_City_PinCode_Master schemas
│   │   ├── 📄 user.py                    # User_Master schemas
│   │   ├── 📄 user_login.py              # User_Login schemas
│   │   ├── 📄 registration.py            # New_User_Request schemas
│   │   └── 📄 report.py                  # Report_History schemas
│   │
│   ├── 📁 routes/                        # API route handlers
│   │   ├── 📄 __init__.py
│   │   └── 📁 v1/                        # API v1 routes
│   │       ├── 📄 __init__.py
│   │       ├── 📄 roles.py               # ← API 1 & 2: User_Role_Master
│   │       ├── 📄 locations.py           # ← API 3 & 4: State_City_PinCode
│   │       ├── 📄 users.py               # ← API 5 & 6: User_Master
│   │       ├── 📄 auth.py                # ← API 7 & 8: User_Login
│   │       ├── 📄 registrations.py       # ← API 9 & 10: New_User_Request
│   │       └── 📄 reports.py             # ← API 11 & 12: Report_History
│   │
│   ├── 📁 services/                      # Business logic layer
│   │   ├── 📄 __init__.py
│   │   ├── 📄 user_role_service.py       # User_Role_Master business logic
│   │   ├── 📄 location_service.py        # State_City_PinCode business logic
│   │   ├── 📄 user_service.py            # User_Master business logic
│   │   ├── 📄 auth_service.py            # User_Login business logic
│   │   ├── 📄 registration_service.py    # New_User_Request business logic
│   │   └── 📄 report_service.py          # Report_History business logic
│   │
│   ├── 📁 utils/                         # Utility functions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 helpers.py                 # General helpers
│   │   ├── 📄 validators.py              # Input validators
│   │   ├── 📄 formatters.py              # Response formatters
│   │   └── 📄 cache.py                   # Caching utilities
│   │
│   └── 📁 exceptions/                    # Custom exceptions
│       ├── 📄 __init__.py
│       └── 📄 custom_exceptions.py       # Custom exception classes
│
├── 📁 tests/                             # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py                    # Pytest configuration & fixtures
│   ├── 📄 test_main.py                   # Main app tests
│   │
│   ├── 📁 unit/                          # Unit tests
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_roles.py              # Tests for APIs 1 & 2
│   │   ├── 📄 test_locations.py          # Tests for APIs 3 & 4
│   │   ├── 📄 test_users.py              # Tests for APIs 5 & 6
│   │   ├── 📄 test_auth.py               # Tests for APIs 7 & 8
│   │   ├── 📄 test_registrations.py      # Tests for APIs 9 & 10
│   │   └── 📄 test_reports.py            # Tests for APIs 11 & 12
│   │
│   └── 📁 integration/                   # Integration tests
│       ├── 📄 __init__.py
│       ├── 📄 test_api_integration.py    # Full API flow tests
│       └── 📄 test_db_integration.py     # Database integration tests
│
└── 📁 .git/                              # Git repository
```

---

## 12 APIs Implementation Map

### Summary Table
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         12 APIs IMPLEMENTATION MAP                       │
├───┬────────────────────────┬──────────────────┬────────────────────────┤
│ # │ Table                  │ Route File       │ API Endpoints          │
├───┼────────────────────────┼──────────────────┼────────────────────────┤
│ 1 │ User_Role_Master       │ routes/v1/roles. │ GET  /api/v1/roles/all │
│ 2 │ User_Role_Master       │ routes/v1/roles. │ POST /api/v1/roles     │
│   │                        │                  │ PUT  /api/v1/roles/{id}│
│   │                        │                  │ DEL  /api/v1/roles/{id}│
├───┼────────────────────────┼──────────────────┼────────────────────────┤
│ 3 │ State_City_PinCode     │ routes/v1/       │ GET  /api/v1/           │
│   │ _Master                │ locations.py     │      locations/all      │
│   │ (Updated Mar 2, 2026)  │                  │ GET  /api/v1/locations/ │
│ 4 │                        │                  │      pincodes (NEW)     │
│   │                        │                  │ POST /api/v1/locations │
│   │                        │                  │ PUT  /api/v1/           │
│   │                        │                  │      locations/{pin}    │
│   │                        │                  │      (was {id})         │
├───┼────────────────────────┼──────────────────┼────────────────────────┤
│ 5 │ User_Master            │ routes/v1/users. │ GET  /api/v1/users/all │
│ 6 │                        │                  │ POST /api/v1/users     │
│   │                        │                  │ PUT  /api/v1/           │
│   │                        │                  │      users/{userId}    │
│   │                        │                  │ DEL  /api/v1/           │
│   │                        │                  │      users/{userId}    │
├───┼────────────────────────┼──────────────────┼────────────────────────┤
│ 7 │ User_Login             │ routes/v1/auth.  │ GET  /api/v1/auth/users│
│ 8 │                        │                  │ POST /api/v1/auth/      │
│   │                        │                  │      credentials       │
│   │                        │                  │ PUT  /api/v1/auth/      │
│   │                        │                  │      credentials/{id}  │
│   │                        │                  │ DEL  /api/v1/auth/      │
│   │                        │                  │      credentials/{id}  │
├───┼────────────────────────┼──────────────────┼────────────────────────┤
│ 9 │ New_User_Request       │ routes/v1/       │ GET  /api/v1/requests/ │
│10 │                        │ registrations.py │      all               │
│   │                        │                  │ POST /api/v1/requests  │
│   │                        │                  │ PUT  /api/v1/requests/ │
│   │                        │                  │      {requestId}       │
│   │                        │                  │ DEL  /api/v1/requests/ │
│   │                        │                  │      {requestId}       │
├───┼────────────────────────┼──────────────────┼────────────────────────┤
│11 │ Report_History         │ routes/v1/       │ GET  /api/v1/reports/  │
│12 │                        │ reports.py       │      all               │
│   │                        │                  │ POST /api/v1/reports   │
│   │                        │                  │ PUT  /api/v1/reports/  │
│   │                        │                  │      {reportId}        │
│   │                        │                  │ DEL  /api/v1/reports/  │
│   │                        │                  │      {reportId}        │
└───┴────────────────────────┴──────────────────┴────────────────────────┘
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT REQUEST                            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FastAPI Application (main.py)                    │
├─────────────────────────────────────────────────────────────────────┤
│ ▪ CORS Middleware                                                   │
│ ▪ Authentication Middleware                                         │
│ ▪ Logging Middleware                                                │
│ ▪ Error Handling                                                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                   ┌───────────┼───────────┐
                   │           │           │
                   ▼           ▼           ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │  Roles       │  │  Locations   │  │  Users       │
        │  routes.py   │  │  locations   │  │  users.py    │
        └──────┬───────┘  └──────┬───────┘  │              │
               │                 │          └──────┬───────┘
               │                 │                 │
        ┌──────▼─────────────────▼─────────────────▼──────┐
        │                                                 │
        │    Security/Authentication Layer                │
        │  (JWT, RBAC, Password Hashing)                 │
        │                                                 │
        └──────────────────────┬──────────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────────┐
        │                                                 │
        │         Services Layer (Business Logic)         │
        │                                                 │
        │  ▪ user_role_service.py                        │
        │  ▪ location_service.py                         │
        │  ▪ user_service.py                             │
        │  ▪ auth_service.py                             │
        │  ▪ registration_service.py                     │
        │  ▪ report_service.py                           │
        │                                                 │
        └──────────────────────┬──────────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────────┐
        │                                                 │
        │     Validation Layer (Pydantic Schemas)        │
        │                                                 │
        │  ▪ user_role.py                                │
        │  ▪ location.py                                 │
        │  ▪ user.py                                     │
        │  ▪ user_login.py                               │
        │  ▪ registration.py                             │
        │  ▪ report.py                                   │
        │                                                 │
        └──────────────────────┬──────────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────────┐
        │                                                 │
        │    Database Connection (connection.py)         │
        │                                                 │
        │  ▪ Connection Pooling                          │
        │  ▪ Session Management                          │
        │  ▪ Transaction Handling                        │
        │                                                 │
        └──────────────────────┬──────────────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────────┐
        │                                                  │
        │   PostgreSQL Database (medostel)                │
        │   35.244.27.232:5432                            │
        │                                                  │
        │   ▪ user_role_master                            │
        │   ▪ state_city_pincode_master                   │
        │   ▪ user_master                                 │
        │   ▪ user_login                                  │
        │   ▪ new_user_request                            │
        │   ▪ report_history                              │
        │                                                  │
        └──────────────────────┬───────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  JSON Response   │
                    │                  │
                    │  {                │
                    │   "status": "ok" │
                    │   "data": {...}  │
                    │  }                │
                    └──────────────────┘
```

---

## File Organization by Functionality

### Core Application Files
```
app/
├── __init__.py          # Package initialization
├── main.py              # FastAPI app setup & router registration
├── config.py            # Settings & configuration
└── constants.py         # Error codes, roles, status values
```

### Request/Response Handling
```
app/schemas/
├── common.py            # APIResponse, ErrorResponse (for all APIs)
├── user_role.py         # Schemas for APIs 1 & 2
├── location.py          # Schemas for APIs 3 & 4
├── user.py              # Schemas for APIs 5 & 6
├── user_login.py        # Schemas for APIs 7 & 8
├── registration.py      # Schemas for APIs 9 & 10
└── report.py            # Schemas for APIs 11 & 12
```

### Database Access
```
app/database/
├── connection.py        # Connection pool, get_db dependency
└── models.py            # SQLAlchemy ORM models (future)
```

### API Implementation
```
app/routes/v1/
├── roles.py             # APIs 1 & 2 - GET, POST, PUT, DELETE
├── locations.py         # APIs 3 & 4 - GET, POST, PUT, DELETE
├── users.py             # APIs 5 & 6 - GET, POST, PUT, DELETE
├── auth.py              # APIs 7 & 8 - GET, POST, PUT, DELETE
├── registrations.py     # APIs 9 & 10 - GET, POST, PUT, DELETE
└── reports.py           # APIs 11 & 12 - GET, POST, PUT, DELETE
```

### Business Logic
```
app/services/
├── user_role_service.py     # Business logic for APIs 1 & 2
├── location_service.py      # Business logic for APIs 3 & 4
├── user_service.py          # Business logic for APIs 5 & 6
├── auth_service.py          # Business logic for APIs 7 & 8
├── registration_service.py  # Business logic for APIs 9 & 10
└── report_service.py        # Business logic for APIs 11 & 12
```

### Cross-cutting Concerns
```
app/security/
├── jwt.py               # Token creation & verification
├── password.py          # Password hashing
└── rbac.py              # Role-based access control

app/middleware/
├── auth.py              # Auth middleware
├── error_handler.py     # Error handling
└── logging.py           # Request/response logging

app/utils/
├── helpers.py           # General utilities
├── validators.py        # Input validation
├── formatters.py        # Response formatting
└── cache.py             # Caching logic
```

---

## Development Phases

### Phase 1: Foundation (Week 1)
```
✓ Create directory structure
✓ Setup configuration (config.py, constants.py)
✓ Setup database connection (connection.py)
✓ Create common schemas (schemas/common.py)
✓ Update main.py with basic structure
```

### Phase 2: APIs 1-2 (Week 2)
```
✓ Create user_role schemas
✓ Create user_role_service.py
✓ Create routes/v1/roles.py (APIs 1 & 2)
✓ Write unit tests
✓ Test on /docs endpoint
```

### Phase 3: APIs 3-4 (Week 2)
```
✓ Create location schemas
✓ Create location_service.py
✓ Create routes/v1/locations.py (APIs 3 & 4)
✓ Write unit tests
```

### Phase 4: APIs 5-6 (Week 3)
```
✓ Create user schemas
✓ Create user_service.py
✓ Create routes/v1/users.py (APIs 5 & 6)
✓ Implement authentication checks
✓ Write integration tests
```

### Phase 5: APIs 7-8 (Week 3)
```
✓ Create user_login schemas
✓ Create auth_service.py
✓ Create routes/v1/auth.py (APIs 7 & 8)
✓ Implement JWT security
✓ Test authentication flow
```

### Phase 6: APIs 9-10 (Week 4)
```
✓ Create registration schemas
✓ Create registration_service.py
✓ Create routes/v1/registrations.py (APIs 9 & 10)
✓ Implement approval workflow
✓ Test registration flow
```

### Phase 7: APIs 11-12 (Week 4)
```
✓ Create report schemas
✓ Create report_service.py
✓ Create routes/v1/reports.py (APIs 11 & 12)
✓ Implement file handling
✓ Test report flow
```

### Phase 8: Testing & Deployment (Week 5)
```
✓ Full integration testing
✓ Load testing
✓ Security audit
✓ Docker build & test
✓ Cloud Run deployment
✓ Production monitoring
```

---

## Key Implementation Points

### 1. Each Route File Contains
```python
@router.get("/all")           # SELECT API - Read all records
async def get_all(...):
    """Retrieve all records"""

@router.post("")              # CRUD API - Create
async def create(...):
    """Create new record"""

@router.put("/{id}")          # CRUD API - Update
async def update(...):
    """Update record"""

@router.delete("/{id}")       # CRUD API - Delete
async def delete(...):
    """Delete record"""
```

### 2. Each Service Contains
```python
class <TableName>Service:
    @staticmethod
    async def get_all_<records>(...):
        """Retrieve all"""

    @staticmethod
    async def create_<record>(...):
        """Create"""

    @staticmethod
    async def update_<record>(...):
        """Update"""

    @staticmethod
    async def delete_<record>(...):
        """Delete"""
```

### 3. Response Format (Consistent)
```json
{
  "status": "success|error",
  "code": 200,
  "message": "Description",
  "data": {...},
  "timestamp": "ISO-8601"
}
```

---

## Testing Strategy

```
tests/
├── unit/
│   ├── test_roles.py              # Test APIs 1 & 2
│   ├── test_locations.py          # Test APIs 3 & 4
│   ├── test_users.py              # Test APIs 5 & 6
│   ├── test_auth.py               # Test APIs 7 & 8
│   ├── test_registrations.py      # Test APIs 9 & 10
│   └── test_reports.py            # Test APIs 11 & 12
│
└── integration/
    ├── test_api_integration.py    # Full API chains
    └── test_db_integration.py     # Database integration
```

---

## Deployment Architecture

```
Local Development
        │
        ▼
Docker Container Build
        │
        ▼
Push to GCR (Google Container Registry)
        │
        ▼
Deploy to Cloud Run
        │
        ├─► GKE Cluster (medostel-api-cluster)
        │
        └─► PostgreSQL Instance
                (35.244.27.232:5432)
```

---

## Quick Command Reference

```bash
# Setup
source venv/bin/activate
pip install -r requirements.txt

# Development
python -m uvicorn app.main:app --reload

# Testing
pytest                              # All tests
pytest tests/unit/test_roles.py    # Specific test
pytest --cov=app                   # With coverage

# Docker
docker build -t medostel-api .
docker-compose up

# Deployment
gcloud run deploy medostel-api \
  --image gcr.io/project/medostel-api:latest \
  --region asia-south1
```

---

## Database Connection Info

```
Host:       35.244.27.232
Port:       5432
Database:   medostel
User:       medostel_api_user
Password:   Iag2bMi@0@6aD
Instance:   medostel-ai-assistant-pgdev-instance

Tables:
1. user_role_master
2. state_city_pincode_master
3. user_master
4. user_login
5. new_user_request
6. report_history
```

---

**Last Updated**: 2026-02-28
**Status**: Structure & Guide Complete - Ready for Implementation
**Total APIs**: 12 (6 tables × 2 APIs each)
**Framework**: FastAPI + PostgreSQL + Python 3.11+
**Deployment**: Google Cloud Run on GKE
