# API Unit Testing - Execution Guide

**Version:** 1.0
**Last Updated:** March 1, 2026
**Framework:** pytest + FastAPI TestClient

---

## 📋 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install pytest pytest-asyncio pytest-cov httpx faker pytest-mock

# Navigate to test directory
cd medostel-api-backend
```

### Run Tests Immediately

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html
```

---

## Directory Structure

```
medostel-api-backend/
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── test_roles_api.py        # APIs 1 & 2 tests (reference implementation)
│   ├── test_locations_api.py    # APIs 3 & 4 tests
│   ├── test_users_api.py        # APIs 5 & 6 tests
│   ├── test_auth_api.py         # APIs 7 & 8 tests
│   ├── test_registrations_api.py # APIs 9 & 10 tests
│   └── test_reports_api.py      # APIs 11 & 12 tests
├── pytest.ini
└── requirements-test.txt
```

---

## Test Fixtures Available

### Commonly Used Fixtures

```python
# Basic async client
async def test_example(client):
    response = await client.get("/api/v1/roles/all")

# Role fixtures
async def test_with_role(sample_role, sample_role_id, doctor_role):
    pass

# Location fixtures
async def test_with_location(sample_location, sample_location_id, mumbai_location):
    pass

# User fixtures
async def test_with_user(sample_user, sample_user_id, doctor_user, patient_user):
    pass

# Login fixtures
async def test_with_login(sample_login):
    pass

# Registration request fixtures
async def test_with_request(sample_request, sample_request_id, pending_request):
    pass

# Report fixtures
async def test_with_report(sample_report, sample_report_id, xray_report, mri_report):
    pass
```

---

## Running Specific Test Categories

### Run All Unit Tests

```bash
pytest tests/ -m unit
```

### Run All Functional Tests

```bash
pytest tests/ -m functional
```

### Run All Performance Tests

```bash
pytest tests/ -m performance
```

### Run All Security Tests

```bash
pytest tests/ -m security
```

### Run All Integration Tests

```bash
pytest tests/ -m integration
```

### Run Smoke Tests Only

```bash
pytest tests/ -m smoke
```

---

## Running Specific API Tests

### Test Roles API (APIs 1 & 2)

```bash
pytest tests/test_roles_api.py -v
```

### Test Specific Test Class

```bash
# Test only GET all roles
pytest tests/test_roles_api.py::TestAPIOne_GetAllRoles -v

# Test only create role
pytest tests/test_roles_api.py::TestAPITwo_CreateRole -v

# Test only update role
pytest tests/test_roles_api.py::TestAPITwo_UpdateRole -v

# Test only delete role
pytest tests/test_roles_api.py::TestAPITwo_DeleteRole -v
```

### Test Specific Test Case

```bash
# Test single test case
pytest tests/test_roles_api.py::TestAPIOne_GetAllRoles::test_get_all_roles_success -v

# Test with keyword expression
pytest tests/test_roles_api.py -k "success" -v
```

---

## Coverage Reports

### Generate HTML Coverage Report

```bash
pytest tests/ --cov=app --cov-report=html

# View report
open htmlcov/index.html
```

### Generate Terminal Coverage Report

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Generate XML Coverage Report (for CI/CD)

```bash
pytest tests/ --cov=app --cov-report=xml
```

### View Coverage by Module

```bash
pytest tests/ --cov=app --cov-report=term:skip-covered
```

### Coverage for Specific Module

```bash
pytest tests/ --cov=app.routes --cov-report=html
```

---

## Test Output Formats

### Verbose Output

```bash
pytest tests/ -v
```

**Output:**
```
tests/test_roles_api.py::TestAPIOne_GetAllRoles::test_get_all_roles_success PASSED
tests/test_roles_api.py::TestAPIOne_GetAllRoles::test_get_all_roles_response_structure PASSED
```

### Short Output

```bash
pytest tests/
```

**Output:**
```
tests/test_roles_api.py ............................. [ 30%]
tests/test_auth_api.py ............................... [ 60%]
tests/test_reports_api.py ............................ [100%]
```

### Show Captured Output

```bash
pytest tests/ -s
```

### Show Print Statements

```bash
pytest tests/ -v -s
```

---

## Test Filtering and Selection

### Run Tests by Name Pattern

```bash
# Run tests containing "create" in name
pytest tests/ -k "create"

# Run tests containing "success"
pytest tests/ -k "success"

# Run tests NOT containing "slow"
pytest tests/ -k "not slow"

# Complex expressions
pytest tests/ -k "test_create and not performance"
```

### Run Tests by File

```bash
# Single file
pytest tests/test_roles_api.py

# Multiple files
pytest tests/test_roles_api.py tests/test_users_api.py

# All tests in directory
pytest tests/unit/
```

### Run Specific Number of Tests

```bash
# Run first 10 tests and stop
pytest tests/ --maxfail=10
```

### Stop on First Failure

```bash
pytest tests/ -x
```

### Stop After N Failures

```bash
pytest tests/ --maxfail=3
```

---

## Performance Testing

### Run Performance Tests Only

```bash
pytest tests/ -m performance
```

### Measure Test Execution Time

```bash
pytest tests/ --durations=10
```

Shows 10 slowest tests.

### Run Tests in Parallel (if installed)

```bash
pip install pytest-xdist
pytest tests/ -n auto
```

---

## Debugging Tests

### Show Full Traceback

```bash
pytest tests/ -v --tb=long
```

### Show Local Variables on Failure

```bash
pytest tests/ -l
```

### Start Debugger on Failure

```bash
pytest tests/ --pdb
```

### Start Debugger on First Failure

```bash
pytest tests/ -x --pdb
```

### Print Statements in Tests

```bash
pytest tests/ -s
```

### Show pytest Version

```bash
pytest --version
```

---

## Test Organization

### Group Tests by Feature

```bash
# Run all role tests
pytest tests/test_roles_api.py

# Run all user tests
pytest tests/test_users_api.py

# Run all auth tests
pytest tests/test_auth_api.py
```

### Test Class Organization

Tests are organized by operation type:
- `TestAPIOne_GetAllRoles` - GET operations
- `TestAPITwo_CreateRole` - POST operations
- `TestAPITwo_UpdateRole` - PUT operations
- `TestAPITwo_DeleteRole` - DELETE operations
- `TestRolesAPISecurity` - Security tests
- `TestRolesAPIEdgeCases` - Edge cases

### Running Tests by Class

```bash
pytest tests/test_roles_api.py::TestAPITwo_CreateRole -v
```

---

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/tests.yml`:

```yaml
name: API Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-test.txt

    - name: Run tests
      run: |
        pytest tests/ -v --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

### Run Full Test Suite Before Commit

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
pytest tests/ -q
if [ $? -ne 0 ]; then
  echo "Tests failed! Commit aborted."
  exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

---

## Test Reports

### Generate Allure Report

```bash
# Install allure
pip install allure-pytest

# Run with allure
pytest tests/ --allure-dir=allure-results

# View report
allure serve allure-results
```

### Generate JUnit XML Report

```bash
pytest tests/ --junit-xml=test-results.xml
```

### Generate HTML Report

```bash
# Install plugin
pip install pytest-html

# Run with HTML report
pytest tests/ --html=report.html --self-contained-html
```

---

## Common Issues & Solutions

### Issue: Async Event Loop Error

**Error:** `RuntimeError: asyncio.run() cannot be called from a running event loop`

**Solution:** Add to `conftest.py`:
```python
@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

### Issue: Database Connection Failed

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
- Verify PostgreSQL is running
- Check database credentials in test environment
- Ensure test database exists

### Issue: Import Error in Tests

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Add to `conftest.py`:
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../repositories/medostel-api-backend'
)))
```

### Issue: Fixture Not Found

**Error:** `fixture 'sample_role' not found`

**Solution:**
- Ensure `conftest.py` is in the same directory as tests
- Check fixture name spelling
- Verify fixture is imported/available

---

## Best Practices

### 1. Test Organization

```python
class TestAPIOne_GetAllRoles:
    """Descriptive class docstring"""

    async def test_descriptive_test_name(self):
        """Descriptive test docstring explaining what is tested"""
        # Arrange - setup test data
        # Act - perform the test
        # Assert - verify results
```

### 2. Async/Await Pattern

```python
# Always use async def for async tests
async def test_async_operation(client):
    response = await client.get("/api/v1/roles/all")
    assert response.status_code == 200
```

### 3. Fixture Usage

```python
# Use fixtures for common setup
async def test_with_fixtures(client, sample_role, sample_role_id):
    # sample_role and sample_role_id are automatically created
    assert sample_role is not None
```

### 4. Parameterized Tests

```python
@pytest.mark.parametrize("status,expected_code", [
    ("Active", 200),
    ("Inactive", 200),
    ("Invalid", 200)  # Should still return 200 with empty results
])
async def test_filter_by_status(client, status, expected_code):
    response = await client.get(f"/api/v1/roles/all?status={status}")
    assert response.status_code == expected_code
```

### 5. Skip Tests Conditionally

```python
async def test_requires_sample_role(sample_role_id):
    if not sample_role_id:
        pytest.skip("Could not create sample role")
    # Test continues...
```

---

## Performance Baseline

Expected response times (on local development machine):

| Endpoint | Operation | Avg Time | Max Time |
|----------|-----------|----------|----------|
| GET /all | Retrieve 100 records | 50ms | 200ms |
| POST | Create single record | 30ms | 100ms |
| PUT | Update single record | 25ms | 80ms |
| DELETE | Delete single record | 20ms | 70ms |

---

## Maintenance

### Regular Test Updates

- Update tests when API specifications change
- Add tests for new API endpoints immediately
- Remove tests for deprecated endpoints
- Review and update fixtures monthly

### Coverage Monitoring

- Run coverage reports before each release
- Maintain minimum 80% code coverage
- Investigate coverage gaps
- Document any intentional gaps

### Test Documentation

- Keep test class docstrings updated
- Document any special test setup requirements
- Include performance baselines in test comments
- Note any environment-specific requirements

---

## Quick Reference Commands

```bash
# Most common commands
pytest tests/                                    # Run all tests
pytest tests/ -v                                 # Verbose output
pytest tests/ --cov=app --cov-report=html      # Coverage report
pytest tests/ -m functional                      # Functional tests only
pytest tests/ -k "test_create"                   # Tests with "create"
pytest tests/test_roles_api.py -v               # Specific file
pytest tests/ -x                                 # Stop on first failure
pytest tests/ --durations=10                     # Show slowest tests
pytest tests/ --pdb                              # Start debugger on failure
```

---

**Document Version:** 1.0
**Last Updated:** March 1, 2026
**Next Review:** April 1, 2026
