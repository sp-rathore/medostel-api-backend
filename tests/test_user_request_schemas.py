"""
Unit tests for user_request schemas
Phase 3: Unit Testing - Schema Validation
Date: 2026-03-03

Test coverage:
- Email validation (RFC 5322)
- Mobile number validation (10 digits)
- Status enum validation
- Role validation
- Schema creation and response models
"""

import pytest
from pydantic import ValidationError
from src.schemas.user_request import (
    UserRequestBase, UserRequestCreate, UserRequestUpdate,
    UserRequestResponse, UserRequestSearchResponse, UserRequestListResponse,
    UserRequestCreateResponse, UserRequestUpdateResponse
)


class TestUserRequestCreateSchema:
    """Tests for UserRequestCreate schema"""

    def test_create_valid_request_minimal(self):
        """Test creating request with minimal required fields"""
        data = {
            "userId": "john@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "currentRole": "DOCTOR"
        }
        request = UserRequestCreate(**data)
        assert request.userId == "john@example.com"
        assert request.firstName == "John"
        assert request.status == "pending"  # Default

    def test_create_valid_request_full(self):
        """Test creating request with all fields"""
        data = {
            "userId": "john.doe@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "organization": "Hospital XYZ",
            "currentRole": "DOCTOR",
            "city_name": "Mumbai",
            "district_name": "Mumbai",
            "pincode": "400001",
            "state_name": "Maharashtra",
            "status": "pending"
        }
        request = UserRequestCreate(**data)
        assert request.userId == "john.doe@example.com"
        assert request.organization == "Hospital XYZ"
        assert request.status == "pending"

    def test_email_valid_formats(self, valid_emails):
        """Test valid email formats"""
        for email in valid_emails:
            data = {
                "userId": email,
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": 9876543210,
                "currentRole": "ADMIN"
            }
            request = UserRequestCreate(**data)
            assert request.userId == email.lower()

    def test_email_invalid_formats(self, invalid_emails):
        """Test invalid email formats"""
        for email in invalid_emails:
            data = {
                "userId": email,
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": 9876543210,
                "currentRole": "ADMIN"
            }
            with pytest.raises(ValidationError):
                UserRequestCreate(**data)

    def test_email_case_insensitivity(self):
        """Test that emails are normalized to lowercase"""
        data = {
            "userId": "John.Doe@Example.COM",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "currentRole": "DOCTOR"
        }
        request = UserRequestCreate(**data)
        assert request.userId == "john.doe@example.com"

    def test_mobile_valid_values(self, valid_mobile_numbers):
        """Test valid mobile numbers"""
        for mobile in valid_mobile_numbers:
            data = {
                "userId": "test@example.com",
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": mobile,
                "currentRole": "ADMIN"
            }
            request = UserRequestCreate(**data)
            assert request.mobileNumber == mobile

    def test_mobile_invalid_values(self, invalid_mobile_numbers):
        """Test invalid mobile numbers"""
        for mobile in invalid_mobile_numbers:
            data = {
                "userId": "test@example.com",
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": mobile,
                "currentRole": "ADMIN"
            }
            with pytest.raises(ValidationError):
                UserRequestCreate(**data)

    def test_mobile_boundary_values(self):
        """Test mobile number boundary values"""
        # Min valid
        data = {
            "userId": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "mobileNumber": 1000000000,
            "currentRole": "ADMIN"
        }
        request = UserRequestCreate(**data)
        assert request.mobileNumber == 1000000000

        # Max valid
        data["mobileNumber"] = 9999999999
        request = UserRequestCreate(**data)
        assert request.mobileNumber == 9999999999

    def test_role_valid_values(self, valid_roles):
        """Test valid role values"""
        for role in valid_roles:
            data = {
                "userId": "test@example.com",
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": 9876543210,
                "currentRole": role
            }
            request = UserRequestCreate(**data)
            assert request.currentRole == role

    def test_role_case_insensitivity(self):
        """Test that roles are normalized to uppercase"""
        data = {
            "userId": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "mobileNumber": 9876543210,
            "currentRole": "doctor"
        }
        request = UserRequestCreate(**data)
        assert request.currentRole == "DOCTOR"

    def test_role_invalid_values(self, invalid_roles):
        """Test invalid role values"""
        for role in invalid_roles:
            data = {
                "userId": "test@example.com",
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": 9876543210,
                "currentRole": role
            }
            with pytest.raises(ValidationError):
                UserRequestCreate(**data)

    def test_status_valid_values(self):
        """Test valid status values"""
        for status in ["pending", "active", "rejected"]:
            data = {
                "userId": "test@example.com",
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": 9876543210,
                "currentRole": "ADMIN",
                "status": status
            }
            request = UserRequestCreate(**data)
            assert request.status == status

    def test_status_case_insensitivity(self):
        """Test that status is normalized to lowercase"""
        data = {
            "userId": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "mobileNumber": 9876543210,
            "currentRole": "ADMIN",
            "status": "PENDING"
        }
        request = UserRequestCreate(**data)
        assert request.status == "pending"

    def test_status_invalid_values(self):
        """Test invalid status values"""
        for status in ["inactive", "archived", "approved", "unknown"]:
            data = {
                "userId": "test@example.com",
                "firstName": "Test",
                "lastName": "User",
                "mobileNumber": 9876543210,
                "currentRole": "ADMIN",
                "status": status
            }
            with pytest.raises(ValidationError):
                UserRequestCreate(**data)

    def test_first_name_required(self):
        """Test that firstName is required"""
        data = {
            "userId": "test@example.com",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "currentRole": "ADMIN"
        }
        with pytest.raises(ValidationError):
            UserRequestCreate(**data)

    def test_last_name_required(self):
        """Test that lastName is required"""
        data = {
            "userId": "test@example.com",
            "firstName": "John",
            "mobileNumber": 9876543210,
            "currentRole": "ADMIN"
        }
        with pytest.raises(ValidationError):
            UserRequestCreate(**data)

    def test_optional_fields(self):
        """Test that optional fields can be omitted"""
        data = {
            "userId": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "mobileNumber": 9876543210,
            "currentRole": "ADMIN"
            # organization, city_name, etc. omitted
        }
        request = UserRequestCreate(**data)
        assert request.organization is None
        assert request.city_name is None


class TestUserRequestUpdateSchema:
    """Tests for UserRequestUpdate schema"""

    def test_update_status_valid(self):
        """Test updating with valid status"""
        data = {"status": "active"}
        update = UserRequestUpdate(**data)
        assert update.status == "active"

    def test_update_status_case_insensitive(self):
        """Test that status is normalized"""
        data = {"status": "REJECTED"}
        update = UserRequestUpdate(**data)
        assert update.status == "rejected"

    def test_update_status_required(self):
        """Test that status is required for update"""
        data = {}
        with pytest.raises(ValidationError):
            UserRequestUpdate(**data)

    def test_update_status_invalid(self):
        """Test invalid status values"""
        for status in ["inactive", "unknown", "closed"]:
            data = {"status": status}
            with pytest.raises(ValidationError):
                UserRequestUpdate(**data)


class TestUserRequestResponseSchema:
    """Tests for UserRequestResponse schema"""

    def test_response_schema_valid(self):
        """Test creating a valid response"""
        from datetime import datetime
        data = {
            "requestId": "REQ_001",
            "userId": "john@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "currentRole": "DOCTOR",
            "status": "pending",
            "created_Date": datetime.now(),
            "updated_Date": datetime.now()
        }
        response = UserRequestResponse(**data)
        assert response.requestId == "REQ_001"
        assert response.userId == "john@example.com"


class TestUserRequestListResponseSchema:
    """Tests for UserRequestListResponse schema"""

    def test_list_response_with_data(self):
        """Test list response with data"""
        from datetime import datetime
        request_data = {
            "requestId": "REQ_001",
            "userId": "john@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "currentRole": "DOCTOR",
            "status": "pending",
            "created_Date": datetime.now(),
            "updated_Date": datetime.now()
        }
        list_response = UserRequestListResponse(
            data=[UserRequestResponse(**request_data)],
            existsFlag=True
        )
        assert len(list_response.data) == 1
        assert list_response.existsFlag is True

    def test_list_response_empty(self):
        """Test list response with no data"""
        list_response = UserRequestListResponse(data=[], existsFlag=False)
        assert len(list_response.data) == 0
        assert list_response.existsFlag is False
