"""
Shared test fixtures and configuration for Medostel API tests
"""

import pytest
import asyncio
from httpx import AsyncClient
from typing import AsyncGenerator
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../repositories/medostel-api-backend')))

from app.main import app
from faker import Faker

fake = Faker()


@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ===== Roles Fixtures =====
@pytest.fixture
async def sample_role(client):
    """Create and return a sample role"""
    role_data = {
        "roleId": f"ROLE_{fake.word().upper()[:10]}",
        "roleName": fake.job()[:50],
        "status": "Active",
        "comments": fake.text()[:200]
    }
    response = await client.post("/api/v1/roles", json=role_data)
    if response.status_code == 201:
        return role_data
    return None


@pytest.fixture
async def sample_role_id(sample_role):
    """Return sample role ID"""
    return sample_role["roleId"] if sample_role else None


@pytest.fixture
async def doctor_role(client):
    """Get or create Doctor role"""
    role_data = {
        "roleId": "ROLE_DOCTOR",
        "roleName": "Doctor",
        "status": "Active",
        "comments": "Doctor role"
    }
    # Try to get existing
    response = await client.get(f"/api/v1/roles/all?status=Active")
    if response.status_code == 200:
        roles = response.json()["data"]["roles"]
        for role in roles:
            if role.get("roleId") == "ROLE_DOCTOR":
                return role_data

    # Create new
    response = await client.post("/api/v1/roles", json=role_data)
    if response.status_code in [201, 409]:  # Created or already exists
        return role_data
    return None


@pytest.fixture
async def patient_role(client):
    """Get or create Patient role"""
    role_data = {
        "roleId": "ROLE_PATIENT",
        "roleName": "Patient",
        "status": "Active",
        "comments": "Patient role"
    }
    response = await client.post("/api/v1/roles", json=role_data)
    if response.status_code in [201, 409]:
        return role_data
    return None


# ===== Location Fixtures =====
# Note: Updated March 3, 2026 - District hierarchy support added
@pytest.fixture
async def sample_location(client):
    """Create and return a sample location with numeric types and district hierarchy"""
    location_data = {
        "stateId": fake.random_int(min=1, max=36),  # India has 36 states/UTs
        "stateName": fake.state()[:50],
        "districtId": fake.random_int(min=1, max=20),  # 1-20 per state
        "districtName": f"{fake.city()} District"[:100],
        "cityId": fake.random_int(min=1, max=1000),
        "cityName": fake.city()[:50],
        "pinCode": fake.random_int(min=100000, max=999999),  # 5-6 digits
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code == 201:
        return response.json()["data"]["location"]
    return None


@pytest.fixture
async def sample_location_pincode(sample_location):
    """Return sample location's pinCode (primary key)"""
    return sample_location["pinCode"] if sample_location else None


@pytest.fixture
async def pune_location(client):
    """Get or create Pune location (different district in Maharashtra)"""
    location_data = {
        "stateId": 27,  # Maharashtra
        "stateName": "Maharashtra",
        "districtId": 2,  # Pune District
        "districtName": "Pune",
        "cityId": 103,  # Pune
        "cityName": "Pune",
        "pinCode": 411001,
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            return response.json()["data"]["location"]
    return location_data


@pytest.fixture
async def nagpur_location(client):
    """Get or create Nagpur location (another district in Maharashtra)"""
    location_data = {
        "stateId": 27,  # Maharashtra
        "stateName": "Maharashtra",
        "districtId": 3,  # Nagpur District
        "districtName": "Nagpur",
        "cityId": 104,  # Nagpur
        "cityName": "Nagpur",
        "pinCode": 440001,
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            return response.json()["data"]["location"]
    return location_data


@pytest.fixture
async def navi_mumbai_location(client):
    """Get or create Navi Mumbai location (another city in Mumbai district)"""
    location_data = {
        "stateId": 27,  # Maharashtra
        "stateName": "Maharashtra",
        "districtId": 1,  # Mumbai District
        "districtName": "Mumbai",
        "cityId": 105,  # Navi Mumbai
        "cityName": "Navi Mumbai",
        "pinCode": 400703,
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            return response.json()["data"]["location"]
    return location_data


@pytest.fixture
async def mumbai_location(client):
    """Get or create Mumbai location with numeric types and district hierarchy"""
    location_data = {
        "stateId": 27,  # Maharashtra
        "stateName": "Maharashtra",
        "districtId": 1,  # Mumbai District
        "districtName": "Mumbai",
        "cityId": 102,  # Mumbai
        "cityName": "Mumbai",
        "pinCode": 400001,
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            return response.json()["data"]["location"]
    return location_data


@pytest.fixture
async def delhi_location(client):
    """Get or create Delhi location with numeric types and district hierarchy"""
    location_data = {
        "stateId": 7,  # Delhi
        "stateName": "Delhi",
        "districtId": 1,  # Central Delhi District
        "districtName": "Central Delhi",
        "cityId": 45,  # New Delhi
        "cityName": "New Delhi",
        "pinCode": 110001,
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            return response.json()["data"]["location"]
    return location_data


@pytest.fixture
async def bangalore_location(client):
    """Get or create Bangalore location with numeric types and district hierarchy"""
    location_data = {
        "stateId": 8,  # Karnataka
        "stateName": "Karnataka",
        "districtId": 1,  # Bangalore Urban District
        "districtName": "Bangalore Urban",
        "cityId": 85,  # Bangalore
        "cityName": "Bangalore",
        "pinCode": 560001,
        "countryName": "India",
        "status": "Active"
    }
    response = await client.post("/api/v1/locations", json=location_data)
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            return response.json()["data"]["location"]
    return location_data


# ===== User Fixtures =====
@pytest.fixture
async def sample_user(client):
    """Create and return a sample user"""
    user_data = {
        "userId": f"user_{fake.numerify('####')}@example.com",
        "firstName": fake.first_name()[:50],
        "lastName": fake.last_name()[:50],
        "currentRole": "Doctor",
        "emailId": fake.email()[:100],
        "mobileNumber": fake.numerify("##########"),
        "organisation": fake.company()[:100],
        "address": fake.address()[:200],
        "status": "Active"
    }
    response = await client.post("/api/v1/users", json=user_data)
    if response.status_code == 201:
        return user_data
    return None


@pytest.fixture
async def sample_user_id(sample_user):
    """Return sample user ID"""
    return sample_user["userId"] if sample_user else None


@pytest.fixture
async def doctor_user(client):
    """Create a doctor user"""
    user_data = {
        "userId": f"doctor_{fake.numerify('####')}@example.com",
        "firstName": "Dr.",
        "lastName": fake.last_name()[:50],
        "currentRole": "Doctor",
        "emailId": fake.email()[:100],
        "mobileNumber": fake.numerify("##########"),
        "organisation": "Medical Center",
        "address": "Medical Center Building",
        "status": "Active"
    }
    response = await client.post("/api/v1/users", json=user_data)
    if response.status_code == 201:
        return user_data
    return None


@pytest.fixture
async def patient_user(client):
    """Create a patient user"""
    user_data = {
        "userId": f"patient_{fake.numerify('####')}@example.com",
        "firstName": fake.first_name()[:50],
        "lastName": fake.last_name()[:50],
        "currentRole": "Patient",
        "emailId": fake.email()[:100],
        "mobileNumber": fake.numerify("##########"),
        "organisation": "Self",
        "address": fake.address()[:200],
        "status": "Active"
    }
    response = await client.post("/api/v1/users", json=user_data)
    if response.status_code == 201:
        return user_data
    return None


# ===== Login Fixtures =====
@pytest.fixture
async def sample_login(client, sample_user):
    """Create and return sample login credentials"""
    if not sample_user:
        return None

    login_data = {
        "userId": sample_user["userId"],
        "username": fake.user_name()[:50],
        "password": "TestPassword123!",
        "roleId": "ROLE_DOCTOR",
        "isActive": True
    }
    response = await client.post("/api/v1/auth/credentials", json=login_data)
    if response.status_code == 201:
        return login_data
    return None


# ===== Registration Request Fixtures =====
@pytest.fixture
async def sample_request(client):
    """Create and return a sample registration request"""
    request_data = {
        "requestId": f"REQ_{fake.numerify('####')}",
        "userName": fake.user_name()[:50],
        "firstName": fake.first_name()[:50],
        "lastName": fake.last_name()[:50],
        "currentRole": "Doctor",
        "emailId": fake.email()[:100],
        "mobileNumber": fake.numerify("##########"),
        "address": fake.address()[:200],
        "requestStatus": "Pending"
    }
    response = await client.post("/api/v1/requests", json=request_data)
    if response.status_code == 201:
        return request_data
    return None


@pytest.fixture
async def sample_request_id(sample_request):
    """Return sample request ID"""
    return sample_request["requestId"] if sample_request else None


@pytest.fixture
async def pending_request(client):
    """Create a pending registration request"""
    request_data = {
        "requestId": f"REQ_PENDING_{fake.numerify('####')}",
        "userName": fake.user_name()[:50],
        "firstName": fake.first_name()[:50],
        "lastName": fake.last_name()[:50],
        "currentRole": "Doctor",
        "emailId": fake.email()[:100],
        "mobileNumber": fake.numerify("##########"),
        "address": fake.address()[:200],
        "requestStatus": "Pending"
    }
    response = await client.post("/api/v1/requests", json=request_data)
    if response.status_code == 201:
        return request_data
    return None


# ===== Report Fixtures =====
@pytest.fixture
async def sample_report(client):
    """Create and return a sample report"""
    report_data = {
        "id": f"RPT_{fake.numerify('####')}",
        "userId": f"patient_{fake.numerify('####')}@example.com",
        "fileName": f"{fake.word()}.pdf",
        "fileType": "PDF",
        "reportType": "XRay",
        "status": "Pending",
        "diagnosis": fake.text()[:200],
        "jsonData": {
            "findings": [fake.sentence()[:100]],
            "severity": "Low"
        }
    }
    response = await client.post("/api/v1/reports", json=report_data)
    if response.status_code == 201:
        return report_data
    return None


@pytest.fixture
async def sample_report_id(sample_report):
    """Return sample report ID"""
    return sample_report["id"] if sample_report else None


@pytest.fixture
async def xray_report(client):
    """Create an XRay report"""
    report_data = {
        "id": f"RPT_XRAY_{fake.numerify('####')}",
        "userId": f"patient_{fake.numerify('####')}@example.com",
        "fileName": "chest_xray.pdf",
        "fileType": "PDF",
        "reportType": "XRay",
        "status": "Pending",
        "diagnosis": "Chest XRay - No abnormalities detected",
        "jsonData": {
            "findings": ["No consolidation", "No effusion"],
            "severity": "Low"
        }
    }
    response = await client.post("/api/v1/reports", json=report_data)
    if response.status_code == 201:
        return report_data
    return None


@pytest.fixture
async def mri_report(client):
    """Create an MRI report"""
    report_data = {
        "id": f"RPT_MRI_{fake.numerify('####')}",
        "userId": f"patient_{fake.numerify('####')}@example.com",
        "fileName": "brain_mri.pdf",
        "fileType": "PDF",
        "reportType": "MRI",
        "status": "Pending",
        "diagnosis": "Brain MRI - Normal",
        "jsonData": {
            "findings": ["No tumor", "No lesions"],
            "severity": "Low"
        }
    }
    response = await client.post("/api/v1/reports", json=report_data)
    if response.status_code == 201:
        return report_data
    return None


# ===== Cleanup Fixtures =====
@pytest.fixture(autouse=True)
async def cleanup(client):
    """Cleanup after each test"""
    yield
    # Cleanup code here if needed
    # For now, tests create separate records that won't interfere


# ===== Marker Configuration =====
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "functional: mark test as a functional test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test"
    )
