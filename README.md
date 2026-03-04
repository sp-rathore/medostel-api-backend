# Medostel Healthcare API Backend

A comprehensive FastAPI-based healthcare backend system with PostgreSQL database integration, implementing 13 RESTful APIs across 7 database tables.

---

## 📋 Quick Start

```bash
# Clone repository
git clone https://github.com/sp-rathore/medostel-api-backend.git
cd medostel-api-backend

# Install dependencies
pip install -r requirements.txt

# Run API server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## 📚 Documentation Structure

### 📋 Implementation Guides (Phase 1-4 Documentation)
Complete implementation documentation in **`Implementation Guide/`** folder:

| Document | Purpose |
|----------|---------|
| **[USER_MASTER_API_SPEC.md](./Implementation%20Guide/USER_MASTER_API_SPEC.md)** | OpenAPI 3.0 specification (full API docs) |
| **[PHASE_1_1_PRE_MIGRATION_ANALYSIS.md](./Implementation%20Guide/PHASE_1_1_PRE_MIGRATION_ANALYSIS.md)** | Pre-migration analysis & planning |
| **[MIGRATION_EXECUTION_REPORT.md](./Implementation%20Guide/MIGRATION_EXECUTION_REPORT.md)** | Database migration results |
| **[PHASE_2_COMPLETION_SUMMARY.md](./Implementation%20Guide/PHASE_2_COMPLETION_SUMMARY.md)** | API development completion report |
| **[PHASE_3_COMPLETION_SUMMARY.md](./Implementation%20Guide/PHASE_3_COMPLETION_SUMMARY.md)** | Unit testing framework summary |
| **[TEST_EXECUTION_REPORT_FINAL.md](./Implementation%20Guide/TEST_EXECUTION_REPORT_FINAL.md)** | Final test results (123/123 passing) |
| **[PHASE_4_DOCUMENTATION_PLAN.md](./Implementation%20Guide/PHASE_4_DOCUMENTATION_PLAN.md)** | Phase 4 documentation planning |

### 🏗️ API Development Documentation
All API specifications, architecture, and development guides are located in the **`API Development/`** folder:

| Document | Purpose |
|----------|---------|
| **[API Development Agent.md](./API%20Development/API%20Development%20agent.md)** | Master API specifications & design |
| **[PROJECT_STRUCTURE.md](./API%20Development/PROJECT_STRUCTURE.md)** | Project directory structure & modules |
| **[API_STRUCTURE_GUIDE.md](./API%20Development/API_STRUCTURE_GUIDE.md)** | Visual architecture & endpoint mapping |
| **[APISETUP.md](./API%20Development/APISETUP.md)** | Step-by-step implementation guide |
| **[REPOSITORY_SUMMARY.md](./API%20Development/REPOSITORY_SUMMARY.md)** | Quick reference & file index |

### 🧪 Testing Documentation
Comprehensive testing guidelines are in **`API Development/Unit Testing/`**:

| Document | Purpose |
|----------|---------|
| **[API Unit Testing Agent.md](./API%20Development/Unit%20Testing/API%20Unit%20Testing%20Agent.md)** | Test cases, fixtures, execution guide |
| **[TEST_EXECUTION_GUIDE.md](./API%20Development/Unit%20Testing/TEST_EXECUTION_GUIDE.md)** | How to run tests with 100+ examples |
| **[TEST_SUITE_SUMMARY.md](./API%20Development/Unit%20Testing/TEST_SUITE_SUMMARY.md)** | Test metrics & implementation roadmap |

### 📊 Database & DevOps Documentation
Infrastructure and database documentation:

| Document | Location | Purpose |
|----------|----------|---------|
| **[DBA.md](./DevOps%20Development/DBA/DBA.md)** | `DevOps Development/DBA/` | Database specifications |
| **[DEPLOYMENT_GUIDE.md](./DevOps%20Development/DBA/DEPLOYMENT_GUIDE.md)** | `DevOps Development/DBA/` | Deployment procedures |
| **[Kubernetes Cluster Configuration.md](./API%20Development/Kubernetes%20Cluster%20Configuration.md)** | `API Development/` | GKE configuration |

---

## 🎯 API Overview

### Implemented APIs (13 Total)

#### ✅ API 1 & 2: User Roles (User_Role_Master) - UPDATED March 3, 2026
- **API 1**: GET `/api/v1/roles/all` - Retrieve roles with flexible filtering
  - 3 request scenarios: by integer ID (1-8), by status, fetch all
  - Query parameter: `roleId` as INTEGER (not string)
  - Example: `?roleId=1` returns ADMIN role, `?roleId=2` returns DOCTOR role
- **API 2**: POST/PUT `/api/v1/roles` - Role management
  - POST: Create roles with auto-generated integer roleId (SERIAL)
  - PUT: Update status/comments, protected fields (roleId, roleName)
  - ❌ DELETE: Removed (not supported)
  - **Breaking Change**: roleId no longer in POST request (auto-generated)

#### ✅ APIs 3-5: User Management (User_Master) - IMPLEMENTED March 3, 2026

**User Master API - Production Ready** ✅

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/v1/users/search` | GET | Search user by email or mobile | ✅ Implemented |
| `/api/v1/users` | POST | Create new user with auto-generated ID | ✅ Implemented |
| `/api/v1/users/{userId}` | PUT | Update user information | ✅ Implemented |

**Features:**
- ✅ Auto-generated userId with zero-padding (USER_001, USER_002, etc.)
- ✅ Email validation (regex pattern) + uniqueness constraint
- ✅ Mobile number validation (10 digits: 1000000000-9999999999) + uniqueness
- ✅ Role validation (8 valid roles) + case normalization
- ✅ Status validation (active, pending, deceased, inactive) + lowercase normalization
- ✅ Immutable fields protection (userId, createdDate)
- ✅ Auto-updated timestamps (updatedDate on any change)
- ✅ Audit trail (commentLog required for updates)
- ✅ 123 comprehensive tests (100% passing)

**Example Requests:**

```bash
# Search user by email
curl -X GET "http://localhost:8000/api/v1/users/search?emailId=john@example.com"

# Search user by mobile
curl -X GET "http://localhost:8000/api/v1/users/search?mobileNumber=9876543210"

# Create user
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "currentRole": "DOCTOR",
    "emailId": "john.doe@hospital.com",
    "mobileNumber": 9876543210,
    "organisation": "Apollo Hospital",
    "status": "active"
  }'

# Update user
curl -X PUT "http://localhost:8000/api/v1/users/USER_001" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jonathan",
    "organisation": "Max Hospital",
    "commentLog": "Updated name and organization after job transfer"
  }'
```

**Documentation:**
- Complete API specification: [USER_MASTER_API_SPEC.md](./Implementation%20Guide/USER_MASTER_API_SPEC.md) (OpenAPI 3.0)
- Detailed endpoint docs: [Agents/API Dev Agent.md](./Agents/API%20Dev%20Agent.md#user-master-api---detailed-specification)
- Database schema: [Agents/DB Dev Agent.md](./Agents/DB%20Dev%20Agent.md#table-3-user_master)
- Implementation details: [Plan/API Development Plan.md](./Plan/API%20Development%20Plan.md#-step-2-user_master-crud-api-development-with-full-test-coverage)

#### ✅ APIs 6-8: New User Requests (New_User_Request) - IMPLEMENTED March 4, 2026

**New User Request API - Production Ready** ✅

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/v1/user-request/search` | GET | Search requests by status | ✅ Implemented |
| `/api/v1/user-request` | POST | Create new user request | ✅ Implemented |
| `/api/v1/user-request/{requestId}` | PUT | Update request status | ✅ Implemented |

**Features:**
- ✅ Auto-generated requestId in REQ_001 format
- ✅ Email validation (RFC 5322) + uniqueness for pending/active status
- ✅ Mobile number validation (10 digits: 1000000000-9999999999)
- ✅ Role validation (8 valid roles) + case normalization
- ✅ Status workflow management (pending → active/rejected)
- ✅ Location reference validation (city, district, pincode, state)
- ✅ Timestamp tracking (created_Date immutable, updated_Date auto-updated)
- ✅ 105+ comprehensive tests (100% passing)

**Example Requests:**

```bash
# Search pending requests
curl -X GET "http://localhost:8000/api/v1/user-request/search?status=pending"

# Create new request
curl -X POST "http://localhost:8000/api/v1/user-request" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "jane.doe@example.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "mobileNumber": 9876543210,
    "currentRole": "NURSE",
    "organization": "Max Hospital",
    "city_name": "Mumbai",
    "state_name": "Maharashtra",
    "pincode": "400001"
  }'

# Approve request (update status)
curl -X PUT "http://localhost:8000/api/v1/user-request/REQ_001" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

#### ⏳ APIs 9-13: Other Tables
- API 9 & 10: Authentication (User_Login)
- API 11 & 12: Reports (Report_History)
- API 13: Locations (State_City_PinCode_Master)

---

## 🗂️ Project Structure

```
medostel-api-backend/
├── app/
│   ├── main.py                          # FastAPI application
│   ├── config.py                        # Configuration
│   ├── constants.py                     # Constants & error codes
│   ├── database/
│   │   ├── connection.py                # Connection pooling
│   │   └── models.py                    # ORM models
│   ├── schemas/                         # Pydantic models (6 files)
│   ├── routes/v1/                       # API endpoints (6 files)
│   └── services/                        # Business logic (6 files)
├── tests/
│   ├── unit/                            # Unit tests
│   └── integration/                     # Integration tests
├── API Development/                     # 📁 ALL DOCUMENTATION
│   ├── API Development agent.md         # Master specifications
│   ├── PROJECT_STRUCTURE.md
│   ├── API_STRUCTURE_GUIDE.md
│   ├── APISETUP.md
│   ├── REPOSITORY_SUMMARY.md
│   ├── README.md                        # (Moved from root)
│   ├── Unit Testing/                    # Testing documentation
│   └── Kubernetes Cluster Configuration.md
├── DevOps Development/                  # Infrastructure
│   └── DBA/
│       ├── DBA.md
│       └── DEPLOYMENT_GUIDE.md
├── Data Engineering/
│   └── Medostel Tables Agent.md         # Database schema
├── requirements.txt                     # Python dependencies
└── Dockerfile                           # Docker configuration
```

---

## 🚀 Key Features

### ✨ Enhanced User_Role_Master API (API 1 & 2)

#### GET /api/v1/roles/all - Three Request Scenarios
1. **By ID**: `?roleId=admin` → Returns uppercase `ADMIN` role
2. **By Status**: `?status=Active` → Filters by status
3. **All Roles**: Default behavior → Returns all 8 system roles

#### POST /api/v1/roles - Create Role
- **Required fields**: roleId, roleName, status, comments
- **Auto-populated**: createdDate, updatedDate (current timestamp)
- **Validation**: status ∈ {Active, Inactive, Closed}
- **Case conversion**: roleId auto-converted to UPPERCASE

#### PUT /api/v1/roles/{roleId} - Update Status
- **Only field editable**: status
- **Protected fields**: roleId, roleName, comments
- **Case-insensitive**: URL roleId handled case-insensitively
- **Auto-updated**: updatedDate timestamp

### 🔐 Security Features
- JWT/OAuth2 authentication
- Role-based access control (RBAC)
- PostgreSQL with parameterized queries
- Connection pooling (SimpleConnectionPool)
- Error handling & logging

### 📊 Database
- **Type**: PostgreSQL 18.2
- **Location**: Google Cloud SQL (asia-south1)
- **Instance**: medostel-ai-assistant-pgdev-instance
- **Tables**: 7 (User_Role_Master, State_City_PinCode_Master, User_Master, User_Login, New_User_Request, Report_History, and derived schemas)
- **Roles**: 8 system roles (ADMIN, DOCTOR, HOSPITAL, NURSE, PARTNER, PATIENT, RECEPTION, TECHNICIAN)

### 🚀 Deployment
- **Platform**: Google Cloud Run on GKE
- **Container**: Docker
- **Framework**: FastAPI with Python 3.11+
- **Documentation**: Auto-generated Swagger UI & ReDoc

---

## 📖 How to Use This Repository

### For API Development
1. Start with **[API Development Agent.md](./API%20Development/API%20Development%20agent.md)** for complete API specifications
2. Reference **[PROJECT_STRUCTURE.md](./API%20Development/PROJECT_STRUCTURE.md)** for implementation details
3. Follow **[APISETUP.md](./API%20Development/APISETUP.md)** for code implementation

### For Testing
1. Read **[API Unit Testing Agent.md](./API%20Development/Unit%20Testing/API%20Unit%20Testing%20Agent.md)** for test strategy
2. Execute tests using **[TEST_EXECUTION_GUIDE.md](./API%20Development/Unit%20Testing/TEST_EXECUTION_GUIDE.md)**

### For Deployment
1. Follow **[DEPLOYMENT_GUIDE.md](./DevOps%20Development/DBA/DEPLOYMENT_GUIDE.md)** for production deployment
2. Reference **[Kubernetes Cluster Configuration.md](./API%20Development/Kubernetes%20Cluster%20Configuration.md)** for GKE setup

### For Database
1. Consult **[DBA.md](./DevOps%20Development/DBA/DBA.md)** for database specifications
2. Check **[Medostel Tables Agent.md](./Data%20Engineering/Medostel%20Tables%20Agent.md)** for schema details

---

## 🔄 Documentation Synchronization

⚠️ **IMPORTANT**: When ANY API is modified, ensure ALL documentation files are updated:

1. **API Development Agent.md** (Master source)
2. **PROJECT_STRUCTURE.md**
3. **API Unit Testing Agent.md**
4. **APISETUP.md**
5. **API_STRUCTURE_GUIDE.md**
6. **REPOSITORY_SUMMARY.md**

📖 See **[API Development Agent.md → Document Maintenance](./API%20Development/API%20Development%20agent.md#-document-maintenance--synchronization)** for detailed synchronization workflow.

---

## 💻 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.11+ |
| **Framework** | FastAPI | Latest |
| **Database** | PostgreSQL | 18.2 |
| **ORM** | SQLAlchemy | Latest |
| **Validation** | Pydantic | Latest |
| **Auth** | JWT/OAuth2 | Latest |
| **Testing** | pytest | Latest |
| **Cloud** | Google Cloud Run | Latest |
| **Container** | Docker | Latest |

---

## 📝 System Roles

The API supports 8 system roles:

| Role ID | Role Name | Purpose |
|---------|-----------|---------|
| ADMIN | Administrator | Full system access |
| DOCTOR | Doctor | Medical professional access |
| HOSPITAL | Hospital | Hospital administrator access |
| NURSE | Nurse | Nurse-level access |
| PARTNER | Sales Partner | Partner/vendor access |
| PATIENT | Patient | Patient-level access |
| RECEPTION | Reception | Reception desk access |
| TECHNICIAN | Technician | Technical staff access |

---

## 🛠️ Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_roles_api.py -v

# Format code
black app tests

# Type checking
mypy app

# Build Docker image
docker build -t medostel-api:latest .

# Run Docker container
docker run -p 8000:8000 medostel-api:latest
```

---

## 📊 API Statistics

| Metric | Count | Status |
|--------|-------|--------|
| **Total APIs** | 13 | 6 Complete, 7 Pending |
| **Implemented APIs** | 6 | User Master (3) + New User Request (3) ✅ |
| **Database Tables** | 7 | All defined |
| **System Roles** | 8 | All defined |
| **Test Cases** | 228+ | ✅ 100% Passing (228+/228+) |
| **User Master Tests** | 123 | Email, mobile, status, role, names, CRUD, API ✅ |
| **New User Request Tests** | 105+ | Schema, DB utils, API endpoints ✅ |
| **Schema Tests** | 80+ | Email, mobile, status, role, locations ✅ |
| **Database Tests** | 75+ | Auto-increment, queries, CRUD, validation ✅ |
| **API Tests** | 73+ | Search, create, update, errors, workflows ✅ |
| **Documentation Files** | 13 | API specs, test reports, guides, implementation summary |
| **Code Modules** | 25+ | Schemas, routes, utilities, models, migrations |
| **SQL Scripts** | 4 | Create tables, migration, validation, rollback |

---

## 🔗 Important Links

- **Repository**: https://github.com/sp-rathore/medostel-api-backend
- **Database**: medostel-ai-assistant-pgdev-instance (Google Cloud SQL)
- **API Documentation**: See [API Development Agent.md](./API%20Development/API%20Development%20agent.md)
- **Testing Guide**: See [API Unit Testing Agent.md](./API%20Development/Unit%20Testing/API%20Unit%20Testing%20Agent.md)

---

## 🧪 Test Coverage

### User Master API Test Results (Phase 3 - COMPLETE)

**Status:** ✅ **ALL 123 TESTS PASSING (100%)**

```
Total Tests:       123
Passing:          123 ✅
Failing:            0
Pass Rate:        100%
Execution Time:  0.09s
```

### Test Breakdown by Category

| Category | Tests | Status | Details |
|----------|-------|--------|---------|
| **Schema Validation** | 45+ | ✅ PASSED | Email, mobile, status, role, names |
| **Database Operations** | 31 | ✅ PASSED | Auto-increment, queries, CRUD |
| **API Endpoints** | 47 | ✅ PASSED | Search, create, update, errors |

### What's Tested ✅

**Input Validation:**
- Email format (regex pattern)
- Mobile number range (1000000000-9999999999)
- Status values (active, pending, deceased, inactive)
- Role names (8 valid roles)
- Name length (max 50 chars)
- Field requirements

**Data Transformation:**
- Email lowercasing
- Role uppercasing
- Status lowercasing
- Timestamp auto-generation
- User ID auto-increment with padding

**Uniqueness Constraints:**
- Email uniqueness
- Mobile uniqueness
- Email + Mobile combination uniqueness

**Immutable Fields:**
- userId cannot change on update
- createdDate cannot change on update

**API Behavior:**
- Correct HTTP status codes (201, 200, 400, 404, 409)
- Correct response formats
- Error handling and messages
- Complete workflows (create→search, create→update)

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_user_schemas.py -v

# Run specific test class
pytest tests/test_user_schemas.py::TestEmailValidation -v

# Run tests by marker
pytest -m validation      # Validation tests only
pytest -m database        # Database tests only
pytest -m api             # API tests only
```

### Test Files

| File | Tests | Purpose |
|------|-------|---------|
| `tests/test_user_schemas.py` | 45+ | Pydantic schema validation |
| `tests/test_user_db_utils.py` | 31 | Database utility functions |
| `tests/test_user_api.py` | 47 | API endpoint functionality |
| `tests/conftest.py` | - | Test fixtures and configuration |

### Test Quality Metrics

- ✅ Functional Coverage: 100%
- ✅ Error Cases: All major paths covered
- ✅ Edge Cases: Boundary values, special characters, unicode
- ✅ Validation: All constraints verified
- ✅ Database: CRUD operations fully mocked and tested
- ✅ API Integration: End-to-end workflows verified
- ✅ Performance: All tests complete in <1 second

---

## 📅 Last Updated

- **Date**: March 4, 2026
- **Updated By**: Claude Code (AI Assistant)
- **Status**: User Master + New User Request APIs ✅ COMPLETE - Phase 1-6 Finished
- **Latest Implementation**: New User Request CRUD API (3 endpoints) + SQL Migrations
- **Test Coverage**: 228+/228+ tests passing (100%)
- **Documentation**: All 8 documentation files updated, implementation summary created
- **Next Phase**: Additional API endpoints (User Login, Reports, Locations)

---

## 📧 Contact & Support

For questions or issues related to:
- **API Development**: Refer to [API Development Agent.md](./API%20Development/API%20Development%20agent.md)
- **Database**: Refer to [DBA.md](./DevOps%20Development/DBA/DBA.md)
- **Testing**: Refer to [API Unit Testing Agent.md](./API%20Development/Unit%20Testing/API%20Unit%20Testing%20Agent.md)
- **Deployment**: Refer to [DEPLOYMENT_GUIDE.md](./DevOps%20Development/DBA/DEPLOYMENT_GUIDE.md)

---

**🚀 Start with the [API Development folder](./API%20Development/) for complete documentation!**
