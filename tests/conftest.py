"""
Pytest configuration and fixtures for user_master tests
Phase 3: Unit Testing
Date: 2026-03-03
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Database setup for testing
# Use SQLite in-memory database for fast tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Session:
    """
    Create a test database session for each test function

    This fixture:
    - Creates tables before each test
    - Provides a clean database session
    - Rolls back transactions after each test
    """
    # Create all tables
    # Note: Uncomment when you have the models defined
    # Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.rollback()
    session.close()


@pytest.fixture(scope="session")
def test_user_data():
    """Sample user data for testing"""
    return {
        "firstName": "John",
        "lastName": "Doe",
        "currentRole": "ADMIN",
        "emailId": "john.doe@example.com",
        "mobileNumber": 9876543210,
        "organisation": "Hospital XYZ",
        "address1": "123 Medical Street",
        "address2": "Suite 101",
        "stateId": "MH",
        "stateName": "Maharashtra",
        "districtId": "DIST_01",
        "cityId": "CITY_01",
        "cityName": "Mumbai",
        "pinCode": "400001",
        "status": "active"
    }


@pytest.fixture(scope="session")
def test_user_update_data():
    """Sample update data for testing"""
    return {
        "firstName": "Jonathan",
        "organisation": "New Hospital",
        "status": "pending",
        "commentLog": "Updated name and status after promotion"
    }


@pytest.fixture(scope="session")
def invalid_emails():
    """Invalid email addresses for testing email validation"""
    return [
        "notanemail",
        "@example.com",
        "user@",
        "user @example.com",
        "user@.com",
        "user@example",
        "user@example.c",  # TLD must be 2+ chars
        "plaintext"  # No @ symbol
    ]


@pytest.fixture(scope="session")
def valid_emails():
    """Valid email addresses for testing email validation"""
    return [
        "john@example.com",
        "john.doe@example.com",
        "john+label@example.co.uk",
        "user123@test-domain.com",
        "a@example.com"
    ]


@pytest.fixture(scope="session")
def invalid_mobile_numbers():
    """Invalid mobile numbers for testing mobile validation"""
    return [
        123,                    # Too short (3 digits)
        12345678901,           # Too long (11 digits)
        999999999,             # Below range (9 digits)
        10000000000,           # Above range (11 digits, exceeds max)
        0,                     # Zero
        -9876543210,           # Negative
        999,                   # Very short
    ]


@pytest.fixture(scope="session")
def valid_mobile_numbers():
    """Valid mobile numbers for testing mobile validation"""
    return [
        1000000000,            # Min valid
        9999999999,            # Max valid
        9876543210,            # Standard Indian mobile
        5555555555,            # Mid-range
        1111111111             # All ones
    ]


@pytest.fixture(scope="session")
def valid_statuses():
    """Valid status values"""
    return ["active", "pending", "deceased", "inactive"]


@pytest.fixture(scope="session")
def invalid_statuses():
    """Invalid status values"""
    return ["inactive2", "unknown", "archived", "deleted", "pending2", "active_"]


@pytest.fixture(scope="session")
def valid_roles():
    """Valid role names"""
    return ["ADMIN", "DOCTOR", "HOSPITAL", "NURSE", "PARTNER", "PATIENT", "RECEPTION", "TECHNICIAN"]


@pytest.fixture(scope="session")
def invalid_roles():
    """Invalid role names"""
    return ["CEO", "MANAGER", "STUDENT", "INVALID", "USER", "SUPPORT"]


@pytest.fixture(scope="session")
def user_login_fixtures():
    """User_Login test data fixtures"""
    return {
        "valid_email": "user@example.com",
        "valid_mobile": "9876543210",
        "valid_password": "SecurePassword123",
        "default_password": "Medostel@AI2026",
        "valid_emails": [
            "john@example.com",
            "jane.doe@company.co.uk",
            "user+label@test.com",
            "a@b.co",
            "test123@example.com"
        ],
        "invalid_emails": [
            "notanemail",
            "@example.com",
            "user@",
            "user@.com",
            "user@example",
            "plaintext",
            "user @example.com",
            "user..name@example.com"
        ],
        "valid_mobiles": [
            "1000000000",  # Min
            "9999999999",  # Max
            "9876543210",  # Standard
            "5555555555",  # Mid-range
            "1111111111"   # All ones
        ],
        "invalid_mobiles": [
            "123",          # Too short
            "12345678901",  # Too long
            "999999999",    # 9 digits (below range)
            "10000000000",  # 11 digits (above range)
            "0",            # Zero
            "abcdefghij",   # Non-numeric
            "9876543210 ",  # With space
            ""              # Empty
        ],
        "valid_passwords": [
            "MyPassword123",
            "SecurePass456",
            "Test@Password789",
            "Medostel@AI2026",
            "LongPasswordFor123"
        ],
        "invalid_passwords": [
            "short",        # Too short
            "1234567",      # 7 chars
            "",             # Empty
            "pass",         # Very short
            "abc"           # 3 chars
        ],
        "valid_statuses": ["Y", "N"],
        "invalid_statuses": ["y", "n", "YES", "NO", "True", "False", "", "X"]
    }


@pytest.fixture(scope="session")
def sample_login_record():
    """Sample login record for testing"""
    return {
        "email_id": "user@example.com",
        "password": "$2b$12$abcdefghijklmnopqrstuvwxyz",  # Bcrypt hash
        "mobile_number": 9876543210,
        "is_active": "Y",
        "last_login": None,
        "created_date": "2026-03-03T10:30:00",
        "updated_date": "2026-03-03T10:30:00"
    }


# Pytest markers for organizing tests
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for multiple components"
    )
    config.addinivalue_line(
        "markers", "validation: Tests for input validation"
    )
    config.addinivalue_line(
        "markers", "database: Tests for database operations"
    )
    config.addinivalue_line(
        "markers", "api: Tests for API endpoints"
    )
    config.addinivalue_line(
        "markers", "password: Tests for password utilities"
    )
    config.addinivalue_line(
        "markers", "schema: Tests for Pydantic schemas"
    )
