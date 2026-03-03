# User_Login API Implementation - Comprehensive Execution Plan

**Date Created:** 2026-03-03
**Status:** PENDING REVIEW & APPROVAL
**Priority:** HIGH
**Complexity:** MEDIUM
**Estimated Effort:** 4-5 Implementation Phases

---

## Executive Summary

This document outlines a complete implementation plan for the **User_Login API** module, including database schema redesign, REST API endpoints, Pydantic validators, comprehensive testing, and documentation updates. The implementation addresses critical requirements from `prompt/prompt.md` including password hashing, email-based user identification, mobile number validation, and status synchronization with the User_Master table.

---

## Current State Analysis

### Existing Schema (src/SQL files/create_Tables.sql - Lines 105-125)
```sql
CREATE TABLE IF NOT EXISTS user_login (
    userId BIGINT PRIMARY KEY,              -- ❌ ISSUE: Should be VARCHAR (email-based)
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,         -- ⚠️ Password hashing not implemented
    roleId INTEGER NOT NULL,                -- ✓ FK to user_role_master
    isActive BOOLEAN DEFAULT TRUE,          -- ❌ ISSUE: Should sync with user_master.status
    lastLoginTime TIMESTAMP,                -- ⚠️ Schema name mismatch (lastLoginTime vs last_login)
    loginAttempts INTEGER DEFAULT 0,        -- ❌ NOT IN REQUIREMENTS
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Issues Identified
1. **Primary Key Mismatch**: Currently BIGINT, should be email (VARCHAR)
2. **No Password Hashing**: Password stored as plain text
3. **Status Sync Missing**: is_Active not synchronized with user_master.status
4. **Mobile Number Missing**: Not stored in user_login table
5. **API Implementation Gap**: No GET/POST/PUT endpoints for user_login
6. **Schema Naming Inconsistency**: lastLoginTime vs last_login_date
7. **Default Password Logic Missing**: No support for default 'Medostel@AI2026'

---

## Implementation Roadmap

### PHASE 1: Database Schema Migration
**Duration:** 1-2 hours
**Output:** Updated SQL schemas and migration scripts

#### 1.1 Schema Redesign
- **File**: `src/SQL files/create_Tables.sql` (Lines 105-125)
- **Changes**:
  - Change `userId` from BIGINT PK to `email_id` VARCHAR(255) PK
  - Add `mobile_number` NUMERIC(10) column with NOT NULL and CHECK constraint
  - Rename `lastLoginTime` → `last_login` for consistency
  - Rename `isActive` → `is_active` for consistency
  - Rename `loginAttempts` → `login_attempts` (to be removed per requirements)
  - Remove `loginAttempts` column (not in requirements)
  - Add CHECK constraint for `is_active` values ('Y', 'N')
  - Update FK: `userId` REFERENCES `user_master(emailId)` instead of numeric reference
  - Add CONSTRAINT: `mobile_number` must match `user_master(mobileNumber)` for same email

#### 1.2 Migration Script
- **File**: Create `src/SQL files/05_migrate_user_login_schema.sql`
- **Content**:
  ```sql
  -- Step 1: Create temporary table with new schema
  CREATE TABLE user_login_new (
      email_id VARCHAR(255) PRIMARY KEY,
      password VARCHAR(255) NOT NULL,
      mobile_number NUMERIC(10) NOT NULL,
      is_active CHAR(1) NOT NULL DEFAULT 'Y' CHECK (is_active IN ('Y', 'N')),
      role_id INTEGER NOT NULL,
      last_login TIMESTAMP,
      created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (email_id) REFERENCES user_master(emailId),
      FOREIGN KEY (role_id) REFERENCES user_role_master(roleId) ON UPDATE CASCADE ON DELETE RESTRICT
  );

  -- Step 2: Migrate data (if any exists)
  -- Step 3: Drop old table and rename new
  -- Step 4: Recreate indexes
  ```

#### 1.3 Indexes
```sql
CREATE UNIQUE INDEX pk_user_login ON user_login(email_id);
CREATE INDEX idx_user_login_mobile ON user_login(mobile_number);
CREATE INDEX idx_user_login_is_active ON user_login(is_active);
CREATE INDEX idx_user_login_role_id ON user_login(role_id);
CREATE INDEX idx_user_login_last_login ON user_login(last_login);
CREATE INDEX idx_user_login_updated_date ON user_login(updated_date);
```

#### 1.4 Validation Scripts
- **File**: Create `src/SQL files/06_validate_user_login_migration.sql`
- Verify schema, constraints, FKs, data integrity

---

### PHASE 2: API Schema & Models
**Duration:** 2-3 hours
**Output:** Pydantic validators and schemas

#### 2.1 Update Schema File
- **File**: `src/schemas/user_login.py` (REWRITE)
- **Changes**:

```python
# Core Models
class UserLoginBase(BaseModel):
    email_id: str = Field(..., description="Email ID (PK, from user_master)")
    mobile_number: str = Field(..., regex="^[0-9]{10}$", description="10-digit mobile")
    role_id: Optional[int] = Field(None, ge=1, le=8, description="FK to user_role_master")

class UserLoginCreate(UserLoginBase):
    password: Optional[str] = Field(None, min_length=8, description="Min 8 chars, default: Medostel@AI2026")

    @validator('password')
    def validate_password(cls, v):
        if v and len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserLoginSelect(BaseModel):
    email_id: str
    mobile_number: str

class UserLoginUpdate(BaseModel):
    # Option 1: Password change
    password: Optional[str] = Field(None, min_length=8)

    # Option 2: Status change
    is_active: Optional[str] = Field(None, regex="^[YN]$")

    # Option 3: Last login update (auto on successful SELECT)
    update_last_login: bool = Field(False)

class UserLoginResponse(UserLoginBase):
    is_active: str  # 'Y' or 'N'
    last_login: Optional[datetime] = None
    created_date: datetime
    updated_date: datetime

class UserLoginPasswordResponse(BaseModel):
    email_id: str
    password: str  # UNHASHED for API response only
    is_active: str
    role_id: Optional[int] = None
```

#### 2.2 Password Hashing Utility
- **File**: Create `src/utils/password_utils.py`
- **Functions**:
  - `hash_password(plain_password: str) -> str`
  - `verify_password(plain_password: str, hashed_password: str) -> bool`
- **Library**: Use `bcrypt` or `passlib`

#### 2.3 Validation Rules
| Field | Rule | Example |
|-------|------|---------|
| email_id | Must exist in user_master | test@example.com |
| mobile_number | 10 digits, must match user_master for same email | 9876543210 |
| password | Min 8 chars OR use default 'Medostel@AI2026' | MyPass123 |
| is_active | 'Y' or 'N', sync with user_master.status | Y |
| role_id | Integer 1-8, FK to user_role_master | 1 |

---

### PHASE 3: API Endpoints
**Duration:** 2-3 hours
**Output:** FastAPI routes with full CRUD support

#### 3.1 Database Utility Layer
- **File**: Create `src/db/user_login_utils.py`
- **Functions**:
  ```python
  def get_user_login_by_email(email_id: str) -> Optional[dict]
  def get_user_login_by_mobile(mobile_number: str) -> Optional[dict]
  def validate_email_in_user_master(email_id: str) -> bool
  def validate_mobile_matches_email(email_id: str, mobile_number: str) -> bool
  def create_user_login(email_id: str, mobile_number: str, password: Optional[str], role_id: Optional[int]) -> dict
  def update_password(email_id: str, new_password: str) -> dict
  def update_is_active(email_id: str, is_active: str) -> dict
  def update_last_login(email_id: str) -> dict
  def get_default_password() -> str  # Returns 'Medostel@AI2026'
  ```

#### 3.2 API Endpoints
- **File**: Create/Update `src/routes/v1/user_login.py`

**Endpoint 1: GET /api/v1/user-login/authenticate**
- **Purpose**: Authenticate user and fetch login details
- **Input**: email_id OR mobile_number
- **Processing**:
  1. Validate input (email or mobile format)
  2. Query user_login table
  3. Unhash password for response
  4. Return password and is_active flag
  5. Trigger update_last_login automatically
- **Response**:
  ```json
  {
    "data": {
      "email_id": "user@example.com",
      "password": "plain_password_unhashed",
      "is_active": "Y",
      "role_id": 2,
      "last_login": "2026-03-03T10:30:00Z"
    },
    "message": "Authentication details retrieved"
  }
  ```
- **Status Codes**: 200, 404, 400

**Endpoint 2: POST /api/v1/user-login/create**
- **Purpose**: Create new user login record
- **Input**:
  ```json
  {
    "email_id": "user@example.com",
    "mobile_number": "9876543210",
    "password": "optional_password",
    "role_id": 2
  }
  ```
- **Processing**:
  1. Validate email exists in user_master
  2. Validate mobile matches user_master for same email
  3. Validate is_active status in user_master is 'active'
  4. If password empty, use default 'Medostel@AI2026'
  5. Hash password
  6. Set is_active to 'Y' if user_master.status='active', else 'N'
  7. Set created_date, updated_date to CURRENT_TIMESTAMP
  8. Insert record
- **Response**:
  ```json
  {
    "message": "User login created successfully",
    "data": {
      "email_id": "user@example.com",
      "mobile_number": "9876543210",
      "is_active": "Y",
      "role_id": 2,
      "created_date": "2026-03-03T10:30:00Z"
    }
  }
  ```
- **Status Codes**: 201, 400, 409, 422

**Endpoint 3: PUT /api/v1/user-login/password**
- **Purpose**: Update password
- **Input**:
  ```json
  {
    "email_id": "user@example.com",
    "new_password": "NewPassword123"
  }
  ```
- **Processing**:
  1. Validate email exists in user_login
  2. Hash new password
  3. Update password column
  4. Set updated_date to CURRENT_TIMESTAMP
  5. Keep created_date unchanged
  6. Do NOT update last_login
- **Response**:
  ```json
  {
    "message": "Password updated successfully",
    "data": {
      "email_id": "user@example.com",
      "updated_date": "2026-03-03T10:35:00Z"
    }
  }
  ```
- **Status Codes**: 200, 400, 404

**Endpoint 4: PUT /api/v1/user-login/status**
- **Purpose**: Update is_active flag
- **Input**:
  ```json
  {
    "email_id": "user@example.com",
    "is_active": "Y"
  }
  ```
- **Processing**:
  1. Validate email exists
  2. Validate is_active is 'Y' or 'N'
  3. Update is_active and updated_date
  4. Keep all other columns unchanged
- **Response**:
  ```json
  {
    "message": "User status updated successfully",
    "data": {
      "email_id": "user@example.com",
      "is_active": "Y",
      "updated_date": "2026-03-03T10:40:00Z"
    }
  }
  ```
- **Status Codes**: 200, 400, 404

#### 3.3 Error Handling
| Error | HTTP Status | Message |
|-------|------------|---------|
| Email not found in user_master | 404 | "Email not registered in user master" |
| Mobile doesn't match email | 422 | "Mobile number doesn't match registered mobile for this email" |
| User status not active | 422 | "User account is not active in user_master" |
| Email already in user_login | 409 | "Login credentials already exist for this email" |
| Invalid email format | 400 | "Invalid email format" |
| Invalid mobile format | 400 | "Mobile number must be 10 digits" |
| Password too short | 400 | "Password must be at least 8 characters" |
| Record not found | 404 | "User login record not found" |

---

### PHASE 4: Unit Testing
**Duration:** 3-4 hours
**Output:** Comprehensive test suite with 50+ tests

#### 4.1 Test File Structure
- **File**: Create `tests/test_user_login_schemas.py` (20 tests)
  - Email validation
  - Mobile number validation
  - Password validation
  - is_active flag validation

- **File**: Create `tests/test_user_login_db_utils.py` (15 tests)
  - Database CRUD operations
  - Validation logic
  - Data integrity checks

- **File**: Create `tests/test_user_login_api.py` (25+ tests)
  - GET /authenticate endpoint
  - POST /create endpoint
  - PUT /password endpoint
  - PUT /status endpoint
  - Error scenarios
  - Edge cases

#### 4.2 Test Coverage Goals
- **Schema Validation**: 100% (email, mobile, password, status)
- **Database Operations**: 100% (create, read, update)
- **API Endpoints**: 100% (happy path + error cases)
- **Edge Cases**: Password hashing, default password, status sync
- **Total Tests**: 60+ with 95%+ passing rate target

#### 4.3 Test Fixtures
```python
# Conftest additions
valid_emails_from_master = ["user1@example.com", "user2@example.com", ...]
valid_mobile_numbers = ["9876543210", "9123456789", ...]
valid_passwords = ["Medostel@AI2026", "SecurePass123", "MyPassword#789"]
invalid_emails = ["notanemail", "user@", "@example.com", ...]
invalid_mobiles = ["123", "12345678901", "abcdefghij", ...]
invalid_passwords = ["short", "1234567", ""]
```

---

### PHASE 5: Documentation Updates
**Duration:** 2-3 hours
**Output:** Updated agent files and specifications

#### 5.1 Files to Update

**5.1.1 Agents/DB Dev Agent.md**
- Add User_Login table section
- Include final schema definition
- Document indexes and constraints
- Migration strategy
- Rollback procedure

**5.1.2 Agents/API Dev Agent.md**
- Add User_Login API section (APIs 7-10)
- Document all 4 endpoints
- Request/response schemas
- Validation rules
- Authentication flow

**5.1.3 Agents/API Unit Testing Agent.md**
- Add User_Login test section
- Test structure overview
- Coverage metrics
- Test execution commands

**5.1.4 Agents/DBA Agent.md**
- Update connection pooling for new table
- Performance considerations
- Backup strategy for user_login
- Security recommendations for password storage

**5.1.5 DevOps/DBA/Databasespecs.md**
- Add user_login table specifications
- Column descriptions
- Index definitions
- FK relationships diagram

**5.1.6 DevOps/DBA/DEPLOYMENT_GUIDE.md**
- Migration deployment steps
- Pre-deployment checks
- Rollback procedures
- Post-deployment verification

**5.1.7 Plan/API Development Plan.md (REWRITE)**
- Add "STEP 3: User_Login API Implementation" section
- Phase breakdown (1-5)
- Completion status
- File change summary
- Test results

**5.1.8 README.md**
- Add User_Login API endpoints table
- Example cURL requests
- Test execution examples
- Update last modified date

#### 5.2 Documentation Template

**User_Login API Section Template:**
```markdown
## User_Login Module

### Overview
- 4 REST endpoints (GET, POST, PUT)
- Password hashing with bcrypt
- Email-based primary key
- Mobile number validation
- Status synchronization with user_master

### Schema
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| email_id | VARCHAR(255) | PK, FK to user_master | |
| password | VARCHAR(255) | NOT NULL | Bcrypt hashed |
| mobile_number | NUMERIC(10) | NOT NULL, CHECK | Must match user_master |
| is_active | CHAR(1) | Y/N | Synced with user_master.status |
| role_id | INTEGER | FK to user_role_master | Optional |
| last_login | TIMESTAMP | NULLABLE | Updated on SELECT |
| created_date | TIMESTAMP | NOT NULL | Immutable |
| updated_date | TIMESTAMP | NOT NULL | Updated on password/status change |

### Endpoints
1. GET /api/v1/user-login/authenticate
2. POST /api/v1/user-login/create
3. PUT /api/v1/user-login/password
4. PUT /api/v1/user-login/status

### Test Coverage
- Schema Validation: 20 tests
- Database Utils: 15 tests
- API Endpoints: 25+ tests
- Total: 60+ tests
```

---

## Implementation Sequence

### Recommended Order of Execution

```
PHASE 1: Database Layer
├── 1.1 Update create_Tables.sql schema definition
├── 1.2 Create migration script (05_migrate_user_login_schema.sql)
├── 1.3 Create validation script (06_validate_user_login_migration.sql)
└── 1.4 Create rollback script (07_rollback_user_login_migration.sql)

PHASE 2: Code Layer - Schemas & Utils
├── 2.1 Create password_utils.py (bcrypt hashing)
├── 2.2 Rewrite user_login.py schemas
├── 2.3 Create user_login_utils.py (database operations)
└── 2.4 Update src/schemas/__init__.py (add user_login imports)

PHASE 3: Code Layer - API Routes
├── 3.1 Create user_login.py routes with 4 endpoints
├── 3.2 Add error handlers and validators
└── 3.3 Update main.py to include new routes

PHASE 4: Testing
├── 4.1 Create test_user_login_schemas.py
├── 4.2 Create test_user_login_db_utils.py
├── 4.3 Create test_user_login_api.py
├── 4.4 Update conftest.py with fixtures
└── 4.5 Execute all tests (target: 60+ passing)

PHASE 5: Documentation
├── 5.1 Update Agents/DB Dev Agent.md
├── 5.2 Update Agents/API Dev Agent.md
├── 5.3 Update Agents/API Unit Testing Agent.md
├── 5.4 Update Agents/DBA Agent.md
├── 5.5 Update DevOps/DBA/Databasespecs.md
├── 5.6 Update DevOps/DBA/DEPLOYMENT_GUIDE.md
├── 5.7 Rewrite Plan/API Development Plan.md
└── 5.8 Update README.md

PHASE 6: Integration & Deployment
├── 6.1 Code review and quality checks
├── 6.2 Git commit and push
├── 6.3 Migration verification in dev environment
└── 6.4 Final testing and sign-off
```

---

## Key Technical Decisions

### 1. Primary Key Strategy
- **Decision**: Use email_id (VARCHAR) as PK instead of numeric userId
- **Rationale**: Directly references user_master.emailId, eliminates FK join overhead
- **Impact**: Simplifies password verification workflow, reduces query complexity

### 2. Password Hashing
- **Library**: `bcrypt` (via `passlib`)
- **Cost**: 12 rounds (security vs performance balance)
- **Workflow**:
  - Storage: Hash only
  - Retrieval: Unhash for API response (security consideration - review needed)
  - Verification: Compare with bcrypt.verify()

### 3. Default Password
- **Value**: `Medostel@AI2026`
- **Hash on Create**: Auto-hash if not provided
- **User Communication**: Should be communicated separately (outside API)

### 4. is_active Sync
- **Source**: user_master.status (only when 'active' → is_active = 'Y')
- **Trigger**: Manual API call (not automatic sync)
- **Update Capability**: Via PUT /api/v1/user-login/status endpoint

### 5. last_login Auto-Update
- **Trigger**: On successful GET /authenticate call
- **Implementation**: Automatic within GET endpoint logic
- **Explicit Update**: Via update_last_login utility function (optional)

### 6. Mobile Number Storage
- **Type**: NUMERIC(10) in database, STRING in API
- **Validation**: Must match user_master.mobileNumber for same email
- **Immutable**: Once created, not updatable

---

## Risk Assessment & Mitigation

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Password hashing performance | LOW | Use bcrypt with cost=12 balance |
| FK constraint on email | MEDIUM | Add NOT NULL constraint, validate before insert |
| Mobile-Email mismatch | MEDIUM | Validate both exist AND match before create |
| Status out of sync | MEDIUM | Document manual sync requirement, add alerts |
| Default password security | MEDIUM | Require immediate change on first login |
| Data loss during migration | HIGH | Full backup before migration, test on dev first |
| Rollback complexity | MEDIUM | Pre-create rollback script, test rollback procedure |

---

## Success Criteria

✅ **Phase 1**: Schema migration completes without errors
✅ **Phase 2**: All schemas validate correctly, password hashing works
✅ **Phase 3**: 4 endpoints respond with correct status codes
✅ **Phase 4**: 60+ tests passing (95%+ pass rate)
✅ **Phase 5**: All documentation updated and consistent
✅ **Phase 6**: Code merged to main branch, dev environment verified

---

## Timeline Estimate

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Database | 1-2 hours | ⏳ Pending |
| Phase 2: Schemas | 2-3 hours | ⏳ Pending |
| Phase 3: API Routes | 2-3 hours | ⏳ Pending |
| Phase 4: Testing | 3-4 hours | ⏳ Pending |
| Phase 5: Documentation | 2-3 hours | ⏳ Pending |
| Phase 6: Integration | 1-2 hours | ⏳ Pending |
| **TOTAL** | **11-17 hours** | ⏳ Pending |

---

## Next Steps

1. ✅ Review this execution plan
2. ⏳ Approve (or request modifications)
3. ⏳ Begin Phase 1 implementation
4. ⏳ Execute sequential phases with testing
5. ⏳ Final validation and deployment

---

**Document Version**: 1.0
**Last Updated**: 2026-03-03
**Prepared By**: Claude Code
**Status**: AWAITING APPROVAL
