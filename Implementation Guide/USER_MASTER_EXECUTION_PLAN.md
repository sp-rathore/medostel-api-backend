# MEDOSTEL USER_MASTER TABLE - EXECUTION PLAN

**Status:** APPROVED
**Date Approved:** 2026-03-03
**Document Version:** 1.0

---

## PROJECT OVERVIEW

Migrate and enhance the `user_master` table schema, implement comprehensive CRUD APIs with validation, and update all dependent documentation and code files.

**Prompt Reference:** `/prompt/prompt.md` (2026-03-03)

---

## PHASE 1: DATABASE SCHEMA MIGRATION

### 1.1 Pre-Migration Analysis

**Task:** Analyze current schema vs. new schema requirements

**Deliverables:**
- Document all column changes (data type changes, new columns, removed columns)
- Identify potential data compatibility issues
- Plan data migration strategy for affected columns

**Estimated Duration:** 2-4 hours
**Dependencies:** None
**Owner:** DBA Agent

**Key Changes:**
- `currentrole` (integer) → `currentRole` (VARCHAR(50))
- `mobilenumber` (varchar) → `mobileNumber` (NUMERIC(10))
- Add new columns: `districtId`, `commentLog`
- Add composite unique constraint on (emailId, mobileNumber)
- Add email and mobile validation checks

---

### 1.2 Data Backup & Migration Script Creation

**Task:** Create comprehensive SQL migration scripts

**Deliverables:**
- Backup script for current user_master table
- DROP TABLE script with validation checks
- CREATE TABLE script with all constraints, indexes, and validations
- Data migration script to transfer existing data (if applicable)
- Rollback script for emergency recovery

**Key Requirements:**
- Email validation regex: `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$`
- Mobile number: 10-digit numeric validation (1000000000-9999999999)
- Column: `commentLog VARCHAR(255)` for tracking recent changes
- Composite unique constraint on (emailId, mobileNumber)
- Foreign keys:
  - `currentRole` → `user_role_master(roleId)`
  - `stateId` → `state_city_pincode_master(stateId)`
  - `districtId` → `state_city_pincode_master(districtId)`
  - `cityId` → `state_city_pincode_master(cityId)`
  - `pinCode` → `state_city_pincode_master(pinCode)`
- Add indexes as per DB Dev Agent.md specifications

**Estimated Duration:** 4-6 hours
**Dependencies:** 1.1
**Owner:** DBA Agent
**File Output:** `src/SQL files/create_tables.sql`

**New Table Structure:**
```sql
CREATE TABLE IF NOT EXISTS user_master (
    userId VARCHAR(100) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    currentRole VARCHAR(50) NOT NULL,
    emailId VARCHAR(255) NOT NULL UNIQUE CHECK (emailId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    mobileNumber NUMERIC(10) NOT NULL UNIQUE CHECK (mobileNumber >= 1000000000 AND mobileNumber <= 9999999999),
    organisation VARCHAR(255),
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    stateId INTEGER,
    stateName VARCHAR(100),
    districtId INTEGER,
    cityId INTEGER,
    cityName VARCHAR(100),
    pinCode INTEGER,
    commentLog VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Active',
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (emailId, mobileNumber),
    FOREIGN KEY (currentRole) REFERENCES user_role_master(roleId),
    FOREIGN KEY (stateId) REFERENCES state_city_pincode_master(stateId),
    FOREIGN KEY (districtId) REFERENCES state_city_pincode_master(districtId),
    FOREIGN KEY (cityId) REFERENCES state_city_pincode_master(cityId),
    FOREIGN KEY (pinCode) REFERENCES state_city_pincode_master(pinCode)
);
```

---

### 1.3 Schema Validation & Testing

**Task:** Validate new schema in dev/test environment

**Deliverables:**
- Test data setup
- Constraint validation tests
- Performance testing for indexes
- Rollback procedure verification

**Estimated Duration:** 2-3 hours
**Dependencies:** 1.2
**Owner:** DBA Agent

---

## PHASE 2: API DEVELOPMENT

### 2.1 Schema & Model Definition

**Task:** Create Python Pydantic schemas for user_master

**Deliverables:**
- `UserMasterBase` - Base model with common fields
- `UserMasterCreate` - POST request schema with validation rules
- `UserMasterUpdate` - PUT request schema with optional fields
- `UserMasterResponse` - Response model with all fields
- Field-level validators for email, mobile number, status

**Validation Rules:**
- Email: Valid email format
- Mobile Number: 10 digits (1000000000-9999999999)
- Status: 'active', 'pending', 'deceased', 'inactive'
- Current Role: Must exist in user_role_master
- Composite: emailId + mobileNumber must be unique

**Estimated Duration:** 2-3 hours
**Dependencies:** None (can start in parallel)
**Owner:** API Dev Agent
**File Output:** `src/schemas/user_master.py` (new file)

---

### 2.2 Database Utilities & Helpers

**Task:** Create database access layer functions

**Deliverables:**
- User ID auto-increment logic (max(userId) + 1)
- Query functions:
  - `get_user_by_email(email)`
  - `get_user_by_mobile(mobile)`
  - `get_user_by_id(user_id)`
- Check functions:
  - `email_exists(email)`
  - `mobile_exists(mobile)`
  - `email_mobile_combination_exists(email, mobile)`
- Insert/Update helper functions with timestamp management

**Estimated Duration:** 2-3 hours
**Dependencies:** 2.1
**Owner:** API Dev Agent

---

### 2.3 API Endpoints Development

#### 2.3.1 SELECT/GET Endpoints

**Endpoint:** `GET /api/v1/users/search`

**Query Parameters:**
- `emailId` (optional) - User email ID
- `mobileNumber` (optional) - User mobile number
- At least one parameter required

**Response (200 Success):**
```json
{
  "data": {
    "userId": "string",
    "firstName": "string",
    "lastName": "string",
    "currentRole": "string",
    "emailId": "string",
    "mobileNumber": "string",
    "organisation": "string",
    "address1": "string",
    "address2": "string",
    "stateId": "integer",
    "stateName": "string",
    "districtId": "integer",
    "cityId": "integer",
    "cityName": "string",
    "pinCode": "integer",
    "commentLog": "string",
    "status": "string",
    "createdDate": "timestamp",
    "updatedDate": "timestamp"
  },
  "existsFlag": true
}
```

**Response (404 Not Found):**
```json
{
  "existsFlag": false,
  "message": "User not found"
}
```

**Response (400 Bad Request):**
```json
{
  "message": "At least one of emailId or mobileNumber must be provided"
}
```

**Estimated Duration:** 2 hours
**Owner:** API Dev Agent

---

#### 2.3.2 POST Endpoint (Create User)

**Endpoint:** `POST /api/v1/users`

**Request Body:**
```json
{
  "firstName": "string",
  "lastName": "string",
  "currentRole": "string",
  "emailId": "string",
  "mobileNumber": "string",
  "organisation": "string (optional)",
  "address1": "string (optional)",
  "address2": "string (optional)",
  "stateId": "integer (optional)",
  "stateName": "string (optional)",
  "districtId": "integer (optional)",
  "cityId": "integer (optional)",
  "cityName": "string (optional)",
  "pinCode": "integer (optional)",
  "status": "string (optional, default: 'Active')"
}
```

**Auto-Generated Fields:**
- `userId` - max(userId) + 1
- `createdDate` - CURRENT_TIMESTAMP
- `updatedDate` - CURRENT_TIMESTAMP
- `commentLog` - Empty on creation

**Validations:**
- Email format validation (regex pattern)
- Mobile number format (10 digits)
- Unique email check
- Unique mobile number check
- Unique email + mobile combination check
- Current role must exist in user_role_master
- Status must be valid ('active', 'pending', 'deceased', 'inactive')

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "data": {
    "userId": "string",
    "firstName": "string",
    "lastName": "string",
    "currentRole": "string",
    "emailId": "string",
    "mobileNumber": "string",
    "createdDate": "timestamp",
    "updatedDate": "timestamp",
    "status": "string"
  }
}
```

**Response (400 Bad Request - Validation Error):**
```json
{
  "message": "Validation error",
  "errors": {
    "emailId": ["Invalid email format"],
    "mobileNumber": ["Mobile number must be 10 digits"]
  }
}
```

**Response (409 Conflict - Duplicate):**
```json
{
  "message": "Email or mobile number already exists"
}
```

**Estimated Duration:** 3 hours
**Owner:** API Dev Agent

---

#### 2.3.3 PUT Endpoint (Update User)

**Endpoint:** `PUT /api/v1/users/{userId}`

**Request Body:**
```json
{
  "firstName": "string (optional)",
  "lastName": "string (optional)",
  "currentRole": "string (optional)",
  "emailId": "string (optional)",
  "mobileNumber": "string (optional)",
  "organisation": "string (optional)",
  "address1": "string (optional)",
  "address2": "string (optional)",
  "stateId": "integer (optional)",
  "stateName": "string (optional)",
  "districtId": "integer (optional)",
  "cityId": "integer (optional)",
  "cityName": "string (optional)",
  "pinCode": "integer (optional)",
  "status": "string (optional)",
  "commentLog": "string (required for audit trail)"
}
```

**Update Rules:**
- Immutable fields: `userId`, `createdDate`
- Auto-update: `updatedDate` - CURRENT_TIMESTAMP
- At least one field must be provided for update
- `commentLog` is required and describes the change
- Request can update one value or all values

**Updateable Fields:**
- Status (valid: 'active', 'pending', 'deceased', 'inactive')
- firstName, lastName, organisation
- city, state, pinCode (via cityId, stateId, pinCode)
- address1, address2
- mobileNumber, emailId

**Validations:**
- Same validation rules as POST for affected fields
- Ensure new email + mobile combination is unique (if both updated)
- Verify role exists if currentRole is being updated
- createdDate must not be changed

**Response (200 Success):**
```json
{
  "message": "User updated successfully",
  "data": {
    "userId": "string",
    "firstName": "string",
    "lastName": "string",
    "updatedDate": "timestamp",
    "commentLog": "string"
  }
}
```

**Response (400 Bad Request - Validation Error):**
```json
{
  "message": "Validation error",
  "errors": {
    "status": ["Invalid status value"]
  }
}
```

**Response (404 Not Found):**
```json
{
  "message": "User not found"
}
```

**Response (409 Conflict - Duplicate):**
```json
{
  "message": "Email or mobile number already in use"
}
```

**Estimated Duration:** 3 hours
**Owner:** API Dev Agent

---

#### 2.3.4 Summary of All Endpoints

| Endpoint | Method | Purpose | Input | Output |
|----------|--------|---------|-------|--------|
| `/api/v1/users/search` | GET | Fetch by email/mobile | emailId OR mobileNumber | User details + existsFlag |
| `/api/v1/users` | POST | Create new user | User data (except userId) | Created user with userId |
| `/api/v1/users/{userId}` | PUT | Update user | Field(s) to update + commentLog | Updated user |

**Estimated Duration:** 8 hours total
**Dependencies:** 2.2
**Owner:** API Dev Agent
**File Output:** `src/routes/v1/users.py` (new file)

---

## PHASE 3: UNIT TESTING

### 3.1 Unit Tests - Models & Validators

**Task:** Test Pydantic models and validators

**Deliverables:**
- Test valid and invalid email formats
- Test valid and invalid mobile numbers
- Test status field validation
- Test required/optional field constraints

**Test Cases:**
- Valid email: "user@example.com"
- Invalid emails: "invalid-email", "user@", "@example.com"
- Valid mobile: 9876543210
- Invalid mobiles: 123, 12345678901, "abcdefghij"
- Valid statuses: 'active', 'pending', 'deceased', 'inactive'
- Invalid status: 'unknown'

**Estimated Duration:** 2 hours
**Dependencies:** 2.1
**Owner:** API Unit Testing Agent

---

### 3.2 Unit Tests - Database Layer

**Task:** Test database access functions

**Deliverables:**
- Test user ID auto-increment logic
- Test existence checks (email, mobile, combination)
- Test CRUD operations with various scenarios
- Test timestamp management

**Test Scenarios:**
- Auto-increment logic generates correct userId
- Email existence check works correctly
- Mobile existence check works correctly
- Composite uniqueness check enforces constraint
- Timestamps (createdDate, updatedDate) are set correctly
- Update operations preserve createdDate, change updatedDate

**Estimated Duration:** 3 hours
**Dependencies:** 2.2
**Owner:** API Unit Testing Agent

---

### 3.3 Unit Tests - API Endpoints

**Task:** Test all API endpoints

**Deliverables:**
- Test GET endpoint with valid/invalid inputs
- Test POST endpoint with various scenarios
- Test PUT endpoint with various update scenarios
- Test error handling and response codes
- Test validation messages

**Test Scenarios:**

**GET Endpoint:**
- Search by valid email - returns user
- Search by valid mobile - returns user
- Search by invalid email - returns 404
- Search by invalid mobile - returns 404
- Search with no parameters - returns 400
- Search with both parameters - returns user

**POST Endpoint:**
- Create with all required fields - returns 201
- Create with duplicate email - returns 409
- Create with duplicate mobile - returns 409
- Create with duplicate email+mobile combination - returns 409
- Create with invalid email format - returns 400
- Create with invalid mobile format - returns 400
- Create with non-existent role - returns 400
- Auto-increment userId works correctly

**PUT Endpoint:**
- Update single field - returns 200
- Update multiple fields - returns 200
- Update status with valid value - returns 200
- Update status with invalid value - returns 400
- Update email to existing email - returns 409
- Update without commentLog - returns 400
- Update non-existent user - returns 404
- createdDate remains unchanged
- updatedDate is updated to current timestamp

**Estimated Duration:** 4 hours
**Dependencies:** 2.3
**Owner:** API Unit Testing Agent
**File Output:** `tests/test_users.py` (new file)

**Target Coverage:** >90% code coverage

---

## PHASE 4: DOCUMENTATION & CODE REGENERATION

### 4.1 Database Documentation

**Task:** Update DevOps documentation

**Deliverables:**
- Update `DevOps/DBA/DatabaseSpecs.md` with new user_master schema
- Update `DevOps/DBA/DEPLOYMENT_GUIDE.md` with migration steps
- Document index specifications
- Document rollback procedures

**Content to Include:**
- New table structure with all columns and constraints
- Index specifications (names, fields, types)
- Foreign key relationships and cascade rules
- Validation constraints and check conditions
- Migration steps and deployment procedure
- Rollback procedure with step-by-step instructions
- Pre-migration checklist
- Post-migration validation steps

**Estimated Duration:** 2 hours
**Dependencies:** 1.2
**Owner:** DBA Agent
**Files to Update:**
- `DevOps/DBA/DatabaseSpecs.md`
- `DevOps/DBA/DEPLOYMENT_GUIDE.md`

---

### 4.2 Agent Documentation Updates

**Task:** Update all agent specifications

**Deliverables:**

**Agents/DB Dev Agent.md:**
- New table schema with all columns, types, and constraints
- Complete index specifications (names, column combinations, types)
- Backup and restore procedures
- Validation and testing procedures
- Performance tuning guidelines

**Agents/API Dev Agent.md:**
- API endpoint specifications (all 3 endpoints)
- Request/response formats and examples
- Validation rules and error handling
- Auto-increment logic for userId
- Timestamp management rules
- Status field valid values

**Agents/API Unit Testing Agent.md:**
- Complete test scenarios for models, database layer, and endpoints
- Test data fixtures
- Expected outcomes for each scenario
- Coverage targets

**Agents/DBA Agent.md:**
- Migration procedures
- Pre-migration validation
- Data backup strategy
- Rollback procedures
- Performance validation

**Estimated Duration:** 3 hours
**Dependencies:** 1.2, 2.3, 3.3
**Owner:** Technical Lead/Architect
**Files to Update:**
- `Agents/DB Dev Agent.md`
- `Agents/API Dev Agent.md`
- `Agents/API Unit Testing Agent.md`
- `Agents/DBA Agent.md`

---

### 4.3 Overall Plan Document

**Task:** Create comprehensive plan document

**Deliverables:**
- Update `Plan/API Development Plan.md` with:
  - Project overview
  - Phase-wise breakdown with timelines
  - Dependencies and critical path
  - Risk assessment and mitigation strategies
  - Rollback procedures and success criteria
  - Integration with user_role_master table
  - References to state_city_pincode_master relationships

**Estimated Duration:** 2 hours
**Dependencies:** All phases
**Owner:** Technical Lead
**File Output:** `Plan/API Development Plan.md`

---

### 4.4 Project Documentation

**Task:** Update project README and specs

**Deliverables:**
- Update `README.md` with:
  - user_master table overview
  - New API endpoints
  - Setup and deployment instructions
- Update documentation for:
  - `src/schemas/user_master.py` reference in existing schema docs
  - API documentation (Swagger/OpenAPI spec)
  - Database ERD (if applicable)

**Estimated Duration:** 2 hours
**Dependencies:** 2.1, 2.3
**Owner:** Technical Writer
**Files to Update:**
- `README.md`
- API documentation

---

## TIMELINE SUMMARY

| Phase | Tasks | Duration | Dependencies | Status |
|-------|-------|----------|--------------|--------|
| 1 - Database Schema Migration | 1.1, 1.2, 1.3 | 8-13 hrs | None | Pending |
| 2 - API Development | 2.1, 2.2, 2.3 | 13-16 hrs | Phase 1 | Pending |
| 3 - Unit Testing | 3.1, 3.2, 3.3 | 9 hrs | Phase 2 | Pending |
| 4 - Documentation | 4.1, 4.2, 4.3, 4.4 | 9 hrs | All | Pending |
| **TOTAL** | **16 tasks** | **39-47 hrs** | - | **Pending** |

---

## DEPENDENCIES & CRITICAL PATH

```
Phase 1 (Database)
├── 1.1 Pre-Migration Analysis
│   └── 1.2 Data Backup & Migration Script
│       └── 1.3 Schema Validation & Testing
│           │
└───────────┼──→ Phase 2 (API Development)
            │   ├── 2.1 Schema & Model Definition
            │   ├── 2.2 Database Utilities & Helpers
            │   └── 2.3 API Endpoints Development
            │       │
            │       └──→ Phase 3 (Unit Testing)
            │           ├── 3.1 Unit Tests - Models
            │           ├── 3.2 Unit Tests - Database Layer
            │           └── 3.3 Unit Tests - API Endpoints
            │               │
            └───────────────┼──→ Phase 4 (Documentation)
                            ├── 4.1 Database Documentation
                            ├── 4.2 Agent Documentation
                            ├── 4.3 Overall Plan Document
                            └── 4.4 Project Documentation
```

**Critical Path:** 1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 2.3 → 3.1, 3.2, 3.3 → 4.1, 4.2, 4.3, 4.4

---

## DELIVERABLES CHECKLIST

### Database Files
- [ ] `src/SQL files/create_tables.sql` - Migration script
- [ ] `DevOps/DBA/DatabaseSpecs.md` - Updated
- [ ] `DevOps/DBA/DEPLOYMENT_GUIDE.md` - Updated

### API Code Files
- [ ] `src/schemas/user_master.py` - New schema file
- [ ] `src/routes/v1/users.py` - New routes file
- [ ] `tests/test_users.py` - New test file

### Documentation Files
- [ ] `Agents/DB Dev Agent.md` - Updated
- [ ] `Agents/API Dev Agent.md` - Updated
- [ ] `Agents/API Unit Testing Agent.md` - Updated
- [ ] `Agents/DBA Agent.md` - Updated
- [ ] `Plan/API Development Plan.md` - Created/Updated
- [ ] `README.md` - Updated

---

## RISK ASSESSMENT & MITIGATION

| Risk | Severity | Probability | Impact | Mitigation Strategy |
|------|----------|-------------|--------|----------------------|
| Data loss during migration | Critical | Low | Lost user records | Full backup before migration, rollback procedure tested, dry-run on staging |
| Breaking existing APIs | High | Medium | Service downtime | Version new endpoints (v1), maintain backward compatibility during transition |
| Schema constraint conflicts | High | Medium | Migration failure | Pre-migration validation script to identify conflicts |
| Missing dependencies | Medium | Medium | Incomplete setup | Verify foreign key tables (user_role_master, state_city_pincode_master) exist |
| Performance degradation | Medium | Low | Slow queries | Index optimization, query performance testing, load testing |
| Role/Permission issues | Medium | Low | Unauthorized access | Verify medostel_admin_user and medostel_api_user roles have proper permissions |
| Foreign key violations | High | High | Data integrity issues | Validate existing data before migration, handle orphaned records |

**Mitigation Actions:**
- Create detailed pre-flight checklist
- Perform dry-run migration on staging environment
- Maintain comprehensive backup strategy
- Document all rollback procedures
- Have designated DBA on-call during deployment
- Plan deployment during maintenance window

---

## SUCCESS CRITERIA

- ✅ All database migration scripts execute successfully without errors
- ✅ All unit tests pass with >90% code coverage
- ✅ All API endpoints respond with correct HTTP status codes
- ✅ All validation rules correctly enforce constraints
- ✅ Composite unique constraint (emailId, mobileNumber) enforced
- ✅ All documentation updated and accurate
- ✅ Rollback procedure tested and verified to restore original state
- ✅ Zero data loss during migration
- ✅ Performance benchmarks meet targets (query response time < 100ms)
- ✅ All foreign key relationships maintained
- ✅ User ID auto-increment logic works correctly
- ✅ Timestamp management (createdDate immutable, updatedDate auto-updated)
- ✅ No breaking changes to existing APIs during transition
- ✅ All team members trained on new schema and APIs

---

## APPROVAL RECORD

| Field | Value |
|-------|-------|
| Plan Created | 2026-03-03 |
| Plan Approved | 2026-03-03 |
| Approved By | User |
| Status | APPROVED FOR EXECUTION |
| Location | Implementation Guide folder |

---

## REFERENCES

- Original Prompt: `/prompt/prompt.md`
- Current User Master Schema: [From database query - 2026-03-03]
- Related Files:
  - `Agents/DB Dev Agent.md`
  - `Agents/API Dev Agent.md`
  - `Agents/API Unit Testing Agent.md`
  - `Agents/DBA Agent.md`
  - `Plan/API Development Plan.md` (to be created)

---

**Document Prepared By:** Claude Code
**Preparation Date:** 2026-03-03
**Last Updated:** 2026-03-03
**Status:** ✅ APPROVED
