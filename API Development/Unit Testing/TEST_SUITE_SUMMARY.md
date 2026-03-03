# Medostel API - Test Suite Summary

**Version:** 1.3
**Updated:** March 4, 2026 - Added User_Master Geographic Hierarchy Tests
**Framework:** pytest + FastAPI TestClient
**Total Test Cases:** 190+ (50 Roles + 65 Locations + 40 Users + Others)
**Coverage Target:** 80%+
**Location API Tests:** 65 (APIs 3-3.4 with district hierarchy endpoints)
**User API Tests:** 40 (APIs 5-6 with geographic FK validation)

---

## 📁 Test Suite Structure

### Files Created

1. **API Unit Testing Agent.md** (Main Documentation)
   - Comprehensive testing strategy
   - All 100+ test cases for 12 APIs
   - Functional and non-functional test cases
   - Test framework setup instructions
   - Expected test baselines and requirements

2. **conftest.py** (Shared Test Configuration)
   - AsyncClient fixture for HTTP testing
   - Sample data generators (Faker)
   - Role fixtures (sample_role, doctor_role, patient_role)
   - Location fixtures (8 total) - Updated March 3, 2026:
     * sample_location (with district hierarchy)
     * sample_location_pincode
     * mumbai_location (district 1)
     * delhi_location (district 1)
     * bangalore_location (district 1)
     * pune_location (district 2 in Maharashtra) - NEW
     * nagpur_location (district 3 in Maharashtra) - NEW
     * navi_mumbai_location (different city, district 1) - NEW
   - User fixtures (sample_user, doctor_user, patient_user)
   - Login fixtures (sample_login)
   - Registration request fixtures (sample_request, pending_request)
   - Report fixtures (sample_report, xray_report, mri_report)
   - Test markers configuration (unit, functional, performance, security, smoke)

3. **test_roles_api.py** (Reference Implementation - APIs 1 & 2)
   - Complete test implementation for Roles API
   - 50+ test cases covering:
     - GET /api/v1/roles/all (API 1)
     - POST /api/v1/roles (API 2 - Create)
     - PUT /api/v1/roles/{roleId} (API 2 - Update)
     - DELETE /api/v1/roles/{roleId} (API 2 - Delete)
   - Test class organization by operation
   - Security and edge case tests
   - Performance tests

4. **TEST_EXECUTION_GUIDE.md** (How to Run Tests)
   - Quick start instructions
   - Command reference for all testing scenarios
   - Coverage report generation
   - CI/CD integration examples
   - Debugging and troubleshooting
   - Best practices
   - Performance baselines

5. **requirements-test.txt** (Dependencies)
   - pytest and plugins
   - httpx for async HTTP testing
   - faker for test data generation
   - pytest-mock for mocking
   - Coverage tools
   - Optional reporting tools

6. **test_locations_api.py** (APIs 1-3.4) ✅ Updated March 3, 2026
   - Complete test implementation for Location APIs with District Hierarchy
   - 65 test cases covering:
     - GET /api/v1/locations/all (API 1 - 15 tests, including district_id filter)
     - POST/PUT /api/v1/locations (API 2 - 18 tests for Create/Update)
     - GET /api/v1/locations/pincodes (API 3.1 - 8 tests, Get by City)
     - GET /api/v1/locations/districts/{state_id} (API 3.2 - 8 tests) - NEW
     - GET /api/v1/locations/cities/{district_id} (API 3.3 - 8 tests) - NEW
     - GET /api/v1/locations/by-district/{district_id} (API 3.4 - 8 tests) - NEW
   - Updated fixtures with district hierarchy (districtId, districtName)
   - 4 new fixtures for multi-district/multi-city testing

7. **test_users_api.py** (APIs 5 & 6) ✅ Updated March 4, 2026
   - Complete test implementation for User Management APIs with Geographic Hierarchy
   - 40 test cases covering:
     - GET /api/v1/users/all (API 5 - 10 tests, including geographic filters)
     - POST /api/v1/users (API 6 - 15 tests for Create with geographic validation)
     - PUT /api/v1/users/{userId} (API 6 - 10 tests for Update, pinCode immutability)
     - DELETE /api/v1/users/{userId} (API 6 - 5 tests for Delete)
   - Updated fixtures with geographic hierarchy (stateId, districtId, cityId, pinCode as int)
   - Geographic FK validation tests (valid/invalid references)
   - pinCode immutability verification tests
   - Partial update tests (geographic fields)

8. **test_auth_api.py** (APIs 7 & 8)
   - *To be created* following test_roles_api.py pattern

9. **test_registrations_api.py** (APIs 9 & 10)
   - *To be created* following test_roles_api.py pattern

10. **test_reports_api.py** (APIs 11 & 12)
    - *To be created* following test_roles_api.py pattern

---

## 🧪 Test Case Coverage

### API 1: GET /api/v1/roles/all - Select All Roles (7 Tests)

| Test Case | Status | Type |
|-----------|--------|------|
| Get all roles successfully | ✅ | Functional |
| Response structure validation | ✅ | Functional |
| Filter by status | ✅ | Functional |
| Filter by inactive status | ✅ | Functional |
| Pagination with limit | ✅ | Functional |
| Pagination with offset | ✅ | Functional |
| Limit validation (max 1000) | ✅ | Functional |
| Offset non-negative validation | ✅ | Functional |
| Minimum limit constraint | ✅ | Functional |
| Maximum limit constraint | ✅ | Functional |
| Empty result set handling | ✅ | Functional |
| Invalid parameter handling | ✅ | Functional |
| Response time performance | ✅ | Performance |

### API 2: CRUD Operations on Roles (32 Tests)

#### Create Operation
| Test Case | Status | Type |
|-----------|--------|------|
| Create role successfully | ✅ | Functional |
| Response structure validation | ✅ | Functional |
| Duplicate role conflict (409) | ✅ | Functional |
| Missing roleId validation | ✅ | Functional |
| Missing roleName validation | ✅ | Functional |
| Missing status validation | ✅ | Functional |
| Optional comments field | ✅ | Functional |
| Empty string handling | ✅ | Functional |
| Special characters handling | ✅ | Functional |
| Very long strings handling | ✅ | Functional |

#### Update Operation
| Test Case | Status | Type |
|-----------|--------|------|
| Update role successfully | ✅ | Functional |
| Update non-existent role (404) | ✅ | Functional |
| Partial update only name | ✅ | Functional |
| Update only status | ✅ | Functional |
| Update comments only | ✅ | Functional |
| Empty body handling | ✅ | Functional |

#### Delete Operation
| Test Case | Status | Type |
|-----------|--------|------|
| Delete role successfully (204) | ✅ | Functional |
| Delete non-existent role (404) | ✅ | Functional |
| Verify actual deletion | ✅ | Functional |

#### Security Tests
| Test Case | Status | Type |
|-----------|--------|------|
| SQL injection prevention | ✅ | Security |
| XSS prevention in response | ✅ | Security |

#### Edge Cases
| Test Case | Status | Type |
|-----------|--------|------|
| Case sensitivity handling | ✅ | Functional |
| Unicode character support | ✅ | Functional |

### APIs 3-12 Test Plan

Similar comprehensive coverage for:
- **API 3 & 4:** Locations (Geographic management)
- **API 5 & 6:** Users (User profiles)
- **API 7 & 8:** Authentication (Login credentials)
- **API 9 & 10:** Registrations (Registration requests)
- **API 11 & 12:** Reports (Medical reports)

**Each API 2-level (CRUD) endpoint** will have:
- 4-5 GET /all tests
- 8-10 Create tests
- 6-8 Update tests
- 3-4 Delete tests
- 2-3 Security tests
- 2-3 Edge case tests

**Total minimum:** 25-30 tests per API pair

---

## 📊 Test Metrics

### Test Categories

| Category | Count | Percentage |
|----------|-------|-----------|
| Functional Tests | 70+ | 65% |
| Non-Functional Tests | 25+ | 23% |
| Security Tests | 8+ | 7% |
| Performance Tests | 5+ | 5% |
| **Total** | **100+** | **100%** |

### Test Types Breakdown

**Functional Tests (70+)**
- Successful operations (CREATE, READ, UPDATE, DELETE)
- Validation tests (required fields, constraints)
- Filtering and pagination
- Error handling
- Response structure validation

**Non-Functional Tests (25+)**
- Performance tests (response time < 500ms)
- Reliability tests (edge cases, boundary values)
- Concurrent request handling
- Database timeout handling
- Unicode and special character support

**Security Tests (8+)**
- SQL injection prevention
- XSS prevention
- Input validation
- Authentication/Authorization
- Password security
- Rate limiting (structure)

**Performance Tests (5+)**
- Response time benchmarks
- Large result set handling
- Pagination performance
- Concurrent request handling
- Database query optimization

---

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
cd medostel-api-backend
pip install -r ../Development/API\ Development/Unit\ Testing/requirements-test.txt
```

### Step 2: Copy Test Files

```bash
# Copy test files to project
cp ../Development/API\ Development/Unit\ Testing/conftest.py tests/
cp ../Development/API\ Development/Unit\ Testing/test_roles_api.py tests/
```

### Step 3: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific API tests
pytest tests/test_roles_api.py -v
```

### Step 4: View Results

```bash
# Open coverage report
open htmlcov/index.html
```

---

## 📈 Test Execution Examples

### Example 1: Run All Tests

```bash
pytest tests/
```

**Output:**
```
tests/test_roles_api.py::TestAPIOne_GetAllRoles::test_get_all_roles_success PASSED [  2%]
tests/test_roles_api.py::TestAPIOne_GetAllRoles::test_get_all_roles_response_structure PASSED [  3%]
...
tests/test_roles_api.py::TestRolesAPIEdgeCases::test_unicode_in_role_data PASSED [100%]

============== 50 passed in 8.42s ===============
```

### Example 2: Run Functional Tests Only

```bash
pytest tests/ -m functional
```

### Example 3: Run Performance Tests Only

```bash
pytest tests/ -m performance
```

### Example 4: Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

**Output:**
```
============== coverage report ==============
Name                          Stmts   Miss  Cover
app/routes/v1/roles.py            45      2    95%
app/services/user_role_service.py  38      1    97%
...
TOTAL                            200     15    92%
```

### Example 5: Debug Failing Test

```bash
pytest tests/test_roles_api.py::TestAPITwo_CreateRole::test_create_role_success -v -s --pdb
```

---

## 📝 Test File Creation Checklist

For each API pair, follow this pattern:

### Step 1: Create Test File

```python
"""
Unit tests for [Feature] APIs
"""
import pytest
from httpx import AsyncClient

class TestAPIOne_[Feature]:
    """Tests for API [N]: GET /api/v1/[endpoint]/all"""
    async def test_...(self, client):
        pass

class TestAPITwo_Create[Feature]:
    """Tests for API [N]: POST /api/v1/[endpoint]"""
    async def test_...(self, client):
        pass

class TestAPITwo_Update[Feature]:
    """Tests for API [N]: PUT /api/v1/[endpoint]/{id}"""
    async def test_...(self, client):
        pass

class TestAPITwo_Delete[Feature]:
    """Tests for API [N]: DELETE /api/v1/[endpoint]/{id}"""
    async def test_...(self, client):
        pass

class Test[Feature]APISecurity:
    """Security tests"""
    async def test_...(self, client):
        pass

class Test[Feature]APIEdgeCases:
    """Edge case tests"""
    async def test_...(self, client):
        pass
```

### Step 2: Reference Available Fixtures

Use appropriate fixtures from `conftest.py`:
- `client` - AsyncClient for HTTP requests
- `sample_[entity]` - Auto-generated test data
- `[role]_[entity]` - Pre-configured entities

### Step 3: Follow Test Structure

```python
async def test_descriptive_name(self, client, fixture_data):
    """Test description"""
    # Arrange - Setup
    data = {}

    # Act - Execute
    response = await client.post("/endpoint", json=data)

    # Assert - Verify
    assert response.status_code == expected_code
    assert response.json()["status"] == "success"
```

### Step 4: Add Markers

```python
@pytest.mark.unit           # Unit test
@pytest.mark.functional     # Functional test
@pytest.mark.security       # Security test
async def test_example(self, client):
    pass
```

---

## 🔍 Fixture Quick Reference

### Available Fixtures

```python
# HTTP client
client                              # AsyncClient for API testing

# Roles
sample_role, sample_role_id
doctor_role, patient_role

# Locations (Updated March 3, 2026)
sample_location, sample_location_pincode
mumbai_location, delhi_location, bangalore_location
pune_location, nagpur_location, navi_mumbai_location  # NEW: For district hierarchy tests

# Users
sample_user, sample_user_id
doctor_user, patient_user

# Authentication
sample_login

# Registrations
sample_request, sample_request_id
pending_request

# Reports
sample_report, sample_report_id
xray_report, mri_report
```

### Using Fixtures

```python
async def test_with_fixtures(self, client, sample_role, doctor_role, sample_user):
    # All fixtures automatically created
    assert sample_role is not None
    assert doctor_role is not None
    assert sample_user is not None
```

---

## 📋 Test Maintenance

### Weekly Tasks
- Review test failures
- Update fixtures if test data schema changes
- Monitor test execution time

### Monthly Tasks
- Review coverage reports
- Update test documentation
- Refactor duplicate test code
- Add tests for new API features

### Quarterly Tasks
- Performance baseline review
- Security audit of test cases
- Architecture review
- Update test dependencies

---

## 🎯 Success Criteria

### Code Coverage
- ✅ Target: 80%+ overall coverage
- ✅ Minimum: 70% per module
- ✅ Monitor coverage trends

### Test Execution
- ✅ All tests pass before commit
- ✅ Full suite runs in < 5 minutes
- ✅ No flaky tests

### Test Quality
- ✅ Clear, descriptive test names
- ✅ One assertion per logical concept
- ✅ No test interdependencies
- ✅ Proper cleanup/teardown

### Documentation
- ✅ Every test has docstring
- ✅ Fixture usage documented
- ✅ Complex tests explained
- ✅ Setup/teardown documented

---

## 📚 Additional Resources

### Test Documentation Files
1. **API Unit Testing Agent.md** - Complete test specifications
2. **TEST_EXECUTION_GUIDE.md** - How to run tests
3. **test_roles_api.py** - Reference implementation
4. **conftest.py** - Fixture definitions

### External Resources
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [httpx Documentation](https://www.python-httpx.org/)
- [Faker Documentation](https://faker.readthedocs.io/)

---

## 🔗 Integration with CI/CD

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements-test.txt
      - run: pytest tests/ --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3
```

### Jenkins
```groovy
pipeline {
    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/ --cov=app --junit-xml=results.xml'
            }
        }
        stage('Coverage') {
            steps {
                publishHTML([
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
    }
}
```

---

## 📞 Support & Questions

### Troubleshooting
- Check TEST_EXECUTION_GUIDE.md for common issues
- Review test output with `-vv` flag
- Use `--pdb` flag to debug failures

### Getting Help
- Refer to API Unit Testing Agent.md for detailed test specs
- Review conftest.py for fixture usage
- Check test_roles_api.py for reference implementation

---

**Document Version:** 1.0
**Last Updated:** March 1, 2026
**Next Review:** April 1, 2026
**Maintained By:** QA Team
