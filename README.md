# Medostel Healthcare API Backend

A comprehensive FastAPI-based healthcare backend system with PostgreSQL database integration, implementing 12 RESTful APIs across 6 database tables.

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

### 🏗️ API Development Documentation
All API specifications, architecture, and development guides are located in the **`API Development/`** folder:

| Document | Purpose |
|----------|---------|
| **[API Development Agent.md](./API%20Development/API%20Development%20agent.md)** | Master API specifications & design |
| **[PROJECT_STRUCTURE.md](./API%20Development/PROJECT_STRUCTURE.md)** | Project directory structure & modules |
| **[API_STRUCTURE_GUIDE.md](./API%20Development/API_STRUCTURE_GUIDE.md)** | Visual architecture & endpoint mapping |
| **[SETUP.md](./API%20Development/SETUP.md)** | Step-by-step implementation guide |
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

### Implemented APIs (12 Total)

#### ✅ API 1 & 2: User Roles (User_Role_Master)
- **API 1**: GET `/api/v1/roles/all` - Retrieve roles with flexible filtering
  - 3 request scenarios: by ID, by status, fetch all
  - Case-insensitive role ID handling
- **API 2**: POST/PUT `/api/v1/roles` - Role management
  - POST: Create roles with auto-timestamp population
  - PUT: Status-only updates with protected fields
  - ❌ DELETE: Removed (not supported)

#### ⏳ APIs 3-12: Other Tables
- API 3 & 4: Locations (State_City_PinCode_Master)
- API 5 & 6: Users (User_Master)
- API 7 & 8: Authentication (User_Login)
- API 9 & 10: Registration (New_User_Request)
- API 11 & 12: Reports (Report_History)

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
│   ├── SETUP.md
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
- **Tables**: 6 (User_Role_Master, State_City_PinCode_Master, User_Master, User_Login, New_User_Request, Report_History)
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
3. Follow **[SETUP.md](./API%20Development/SETUP.md)** for code implementation

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
4. **SETUP.md**
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

| Metric | Count |
|--------|-------|
| **Total APIs** | 12 |
| **Database Tables** | 6 |
| **System Roles** | 8 |
| **Test Cases** | 100+ |
| **Documentation Files** | 7 |
| **Code Modules** | 18+ |

---

## 🔗 Important Links

- **Repository**: https://github.com/sp-rathore/medostel-api-backend
- **Database**: medostel-ai-assistant-pgdev-instance (Google Cloud SQL)
- **API Documentation**: See [API Development Agent.md](./API%20Development/API%20Development%20agent.md)
- **Testing Guide**: See [API Unit Testing Agent.md](./API%20Development/Unit%20Testing/API%20Unit%20Testing%20Agent.md)

---

## 📅 Last Updated

- **Date**: March 1, 2026
- **Updated By**: Claude Code
- **Status**: Design Complete & Enhanced - Ready for Implementation
- **API Enhancement**: User_Role_Master (API 1 & 2) ✅ Enhanced
- **Remaining APIs**: APIs 3-12 ⏳ In Development

---

## 📧 Contact & Support

For questions or issues related to:
- **API Development**: Refer to [API Development Agent.md](./API%20Development/API%20Development%20agent.md)
- **Database**: Refer to [DBA.md](./DevOps%20Development/DBA/DBA.md)
- **Testing**: Refer to [API Unit Testing Agent.md](./API%20Development/Unit%20Testing/API%20Unit%20Testing%20Agent.md)
- **Deployment**: Refer to [DEPLOYMENT_GUIDE.md](./DevOps%20Development/DBA/DEPLOYMENT_GUIDE.md)

---

**🚀 Start with the [API Development folder](./API%20Development/) for complete documentation!**
