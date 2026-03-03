"""
User_Login Schema Validation Tests
Date: March 3, 2026
Purpose: Comprehensive Pydantic schema validation testing
"""

import pytest
from pydantic import ValidationError
from src.schemas.user_login import (
    UserLoginBase,
    UserLoginCreate,
    UserLoginUpdate,
    UserLoginResponse,
    UserLoginAuthenticateRequest,
    UserLoginPasswordUpdate,
    UserLoginStatusUpdate,
)


class TestUserLoginBaseSchema:
    """Test UserLoginBase schema validation"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_valid_email_and_mobile(self, user_login_fixtures):
        """Test valid email and mobile number"""
        schema = UserLoginBase(
            email_id=user_login_fixtures["valid_email"],
            mobile_number=user_login_fixtures["valid_mobile"]
        )
        assert schema.email_id == user_login_fixtures["valid_email"]
        assert schema.mobile_number == user_login_fixtures["valid_mobile"]

    @pytest.mark.schema
    @pytest.mark.validation
    def test_email_lowercase_conversion(self):
        """Test email is converted to lowercase"""
        schema = UserLoginBase(
            email_id="USER@EXAMPLE.COM",
            mobile_number="9876543210"
        )
        assert schema.email_id == "user@example.com"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_invalid_email_format(self, user_login_fixtures):
        """Test invalid email formats are rejected"""
        for invalid_email in user_login_fixtures["invalid_emails"][:3]:
            with pytest.raises(ValidationError) as exc_info:
                UserLoginBase(
                    email_id=invalid_email,
                    mobile_number="9876543210"
                )
            assert "Invalid email format" in str(exc_info.value)

    @pytest.mark.schema
    @pytest.mark.validation
    def test_invalid_mobile_format(self, user_login_fixtures):
        """Test invalid mobile formats are rejected"""
        invalid_cases = ["123", "12345678901", "abc1234567"]
        for invalid_mobile in invalid_cases:
            with pytest.raises(ValidationError) as exc_info:
                UserLoginBase(
                    email_id="user@example.com",
                    mobile_number=invalid_mobile
                )
            assert "Mobile number must be" in str(exc_info.value) or "digits" in str(exc_info.value)

    @pytest.mark.schema
    @pytest.mark.validation
    def test_mobile_number_range_validation(self):
        """Test mobile number range validation"""
        # Test min value
        schema = UserLoginBase(
            email_id="user@example.com",
            mobile_number="1000000000"
        )
        assert schema.mobile_number == "1000000000"

        # Test max value
        schema = UserLoginBase(
            email_id="user@example.com",
            mobile_number="9999999999"
        )
        assert schema.mobile_number == "9999999999"

        # Test below range
        with pytest.raises(ValidationError):
            UserLoginBase(
                email_id="user@example.com",
                mobile_number="0999999999"  # Below 1000000000
            )

        # Test above range
        with pytest.raises(ValidationError):
            UserLoginBase(
                email_id="user@example.com",
                mobile_number="10000000000"  # Above 9999999999
            )

    @pytest.mark.schema
    @pytest.mark.validation
    def test_multiple_valid_emails(self, user_login_fixtures):
        """Test multiple valid email formats"""
        for valid_email in user_login_fixtures["valid_emails"]:
            schema = UserLoginBase(
                email_id=valid_email,
                mobile_number="9876543210"
            )
            assert schema.email_id == valid_email.lower()


class TestUserLoginCreateSchema:
    """Test UserLoginCreate schema"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_create_with_password(self, user_login_fixtures):
        """Test create with explicit password"""
        schema = UserLoginCreate(
            email_id=user_login_fixtures["valid_email"],
            mobile_number=user_login_fixtures["valid_mobile"],
            password=user_login_fixtures["valid_password"]
        )
        assert schema.password == user_login_fixtures["valid_password"]

    @pytest.mark.schema
    @pytest.mark.validation
    def test_create_without_password(self, user_login_fixtures):
        """Test create without password (uses default)"""
        schema = UserLoginCreate(
            email_id=user_login_fixtures["valid_email"],
            mobile_number=user_login_fixtures["valid_mobile"],
            password=None
        )
        assert schema.password is None

    @pytest.mark.schema
    @pytest.mark.validation
    def test_password_min_length_validation(self):
        """Test password minimum length validation"""
        # Valid: 8 characters
        schema = UserLoginCreate(
            email_id="user@example.com",
            mobile_number="9876543210",
            password="12345678"
        )
        assert schema.password == "12345678"

        # Invalid: 7 characters
        with pytest.raises(ValidationError):
            UserLoginCreate(
                email_id="user@example.com",
                mobile_number="9876543210",
                password="1234567"
            )

    @pytest.mark.schema
    @pytest.mark.validation
    def test_password_max_length_validation(self):
        """Test password maximum length"""
        # Valid: 255 characters
        password_255 = "a" * 255
        schema = UserLoginCreate(
            email_id="user@example.com",
            mobile_number="9876543210",
            password=password_255
        )
        assert schema.password == password_255

        # Invalid: 256 characters
        with pytest.raises(ValidationError):
            UserLoginCreate(
                email_id="user@example.com",
                mobile_number="9876543210",
                password="a" * 256
            )


class TestUserLoginUpdateSchema:
    """Test UserLoginUpdate schema"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_update_password_only(self):
        """Test updating password only"""
        schema = UserLoginUpdate(
            password="NewPassword123",
            is_active=None
        )
        assert schema.password == "NewPassword123"
        assert schema.is_active is None

    @pytest.mark.schema
    @pytest.mark.validation
    def test_update_status_only(self):
        """Test updating status only"""
        schema = UserLoginUpdate(
            password=None,
            is_active="Y"
        )
        assert schema.password is None
        assert schema.is_active == "Y"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_update_both_fields(self):
        """Test updating both password and status"""
        schema = UserLoginUpdate(
            password="NewPassword123",
            is_active="N"
        )
        assert schema.password == "NewPassword123"
        assert schema.is_active == "N"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_status_case_insensitive(self):
        """Test is_active is converted to uppercase"""
        schema = UserLoginUpdate(is_active="y")
        assert schema.is_active == "Y"

        schema = UserLoginUpdate(is_active="n")
        assert schema.is_active == "N"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_invalid_status_value(self):
        """Test invalid status values are rejected"""
        invalid_statuses = ["X", "YES", "NO", "True", "False"]
        for invalid_status in invalid_statuses:
            with pytest.raises(ValidationError):
                UserLoginUpdate(is_active=invalid_status)

    @pytest.mark.schema
    @pytest.mark.validation
    def test_password_validation_in_update(self):
        """Test password validation in update schema"""
        # Valid
        schema = UserLoginUpdate(password="ValidPassword123")
        assert schema.password == "ValidPassword123"

        # Invalid: too short
        with pytest.raises(ValidationError):
            UserLoginUpdate(password="short")


class TestUserLoginAuthenticateRequestSchema:
    """Test UserLoginAuthenticateRequest schema"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_authenticate_by_email(self):
        """Test authenticate request with email"""
        schema = UserLoginAuthenticateRequest(
            email_id="user@example.com",
            mobile_number=None
        )
        assert schema.email_id == "user@example.com"
        assert schema.mobile_number is None

    @pytest.mark.schema
    @pytest.mark.validation
    def test_authenticate_by_mobile(self):
        """Test authenticate request with mobile"""
        schema = UserLoginAuthenticateRequest(
            email_id=None,
            mobile_number="9876543210"
        )
        assert schema.email_id is None
        assert schema.mobile_number == "9876543210"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_invalid_email_format_in_authenticate(self):
        """Test invalid email in authenticate request"""
        with pytest.raises(ValidationError):
            UserLoginAuthenticateRequest(
                email_id="invalid_email",
                mobile_number=None
            )

    @pytest.mark.schema
    @pytest.mark.validation
    def test_invalid_mobile_format_in_authenticate(self):
        """Test invalid mobile in authenticate request"""
        with pytest.raises(ValidationError):
            UserLoginAuthenticateRequest(
                email_id=None,
                mobile_number="123"
            )


class TestUserLoginPasswordUpdateSchema:
    """Test UserLoginPasswordUpdate schema"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_valid_password_update(self):
        """Test valid password update"""
        schema = UserLoginPasswordUpdate(
            email_id="user@example.com",
            new_password="NewSecurePassword123"
        )
        assert schema.email_id == "user@example.com"
        assert schema.new_password == "NewSecurePassword123"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_password_update_validation(self):
        """Test password validation in update"""
        # Valid: 8 chars
        schema = UserLoginPasswordUpdate(
            email_id="user@example.com",
            new_password="12345678"
        )
        assert len(schema.new_password) == 8

        # Invalid: 7 chars
        with pytest.raises(ValidationError):
            UserLoginPasswordUpdate(
                email_id="user@example.com",
                new_password="1234567"
            )

    @pytest.mark.schema
    @pytest.mark.validation
    def test_email_validation_in_password_update(self):
        """Test email validation in password update"""
        with pytest.raises(ValidationError):
            UserLoginPasswordUpdate(
                email_id="invalid_email",
                new_password="ValidPassword123"
            )


class TestUserLoginStatusUpdateSchema:
    """Test UserLoginStatusUpdate schema"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_valid_status_update_y(self):
        """Test valid status update to Y"""
        schema = UserLoginStatusUpdate(
            email_id="user@example.com",
            is_active="Y"
        )
        assert schema.is_active == "Y"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_valid_status_update_n(self):
        """Test valid status update to N"""
        schema = UserLoginStatusUpdate(
            email_id="user@example.com",
            is_active="N"
        )
        assert schema.is_active == "N"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_status_lowercase_conversion(self):
        """Test status is converted to uppercase"""
        schema = UserLoginStatusUpdate(
            email_id="user@example.com",
            is_active="y"
        )
        assert schema.is_active == "Y"

    @pytest.mark.schema
    @pytest.mark.validation
    def test_invalid_status_in_update(self):
        """Test invalid status values"""
        invalid_statuses = ["X", "YES", "NO", "0", "1", ""]
        for invalid_status in invalid_statuses:
            with pytest.raises(ValidationError):
                UserLoginStatusUpdate(
                    email_id="user@example.com",
                    is_active=invalid_status
                )

    @pytest.mark.schema
    @pytest.mark.validation
    def test_email_validation_in_status_update(self):
        """Test email validation in status update"""
        with pytest.raises(ValidationError):
            UserLoginStatusUpdate(
                email_id="invalid@",
                is_active="Y"
            )


class TestUserLoginResponseSchema:
    """Test UserLoginResponse schema"""

    @pytest.mark.schema
    @pytest.mark.validation
    def test_response_schema_creation(self, sample_login_record):
        """Test response schema creation"""
        schema = UserLoginResponse(
            email_id=sample_login_record["email_id"],
            mobile_number=str(sample_login_record["mobile_number"]),
            is_active=sample_login_record["is_active"],
            last_login=None,
            created_date=sample_login_record["created_date"],
            updated_date=sample_login_record["updated_date"]
        )
        assert schema.email_id == sample_login_record["email_id"]
        assert schema.is_active == "Y"


class TestSchemaIntegration:
    """Integration tests for multiple schemas"""

    @pytest.mark.schema
    @pytest.mark.integration
    def test_create_then_update_flow(self):
        """Test create and update flow"""
        # Create
        create_schema = UserLoginCreate(
            email_id="user@example.com",
            mobile_number="9876543210",
            password="InitialPassword123"
        )
        assert create_schema.email_id == "user@example.com"

        # Update password
        update_schema = UserLoginUpdate(
            password="UpdatedPassword456",
            is_active=None
        )
        assert update_schema.password == "UpdatedPassword456"

        # Update status
        update_schema = UserLoginUpdate(
            password=None,
            is_active="N"
        )
        assert update_schema.is_active == "N"

    @pytest.mark.schema
    @pytest.mark.integration
    def test_authenticate_then_update_flow(self):
        """Test authenticate and update flow"""
        # Authenticate
        auth_schema = UserLoginAuthenticateRequest(
            email_id="user@example.com",
            mobile_number=None
        )
        assert auth_schema.email_id == "user@example.com"

        # Update password after auth
        password_update = UserLoginPasswordUpdate(
            email_id=auth_schema.email_id,
            new_password="NewPassword123"
        )
        assert password_update.email_id == auth_schema.email_id

    @pytest.mark.schema
    @pytest.mark.validation
    def test_all_email_validations(self, user_login_fixtures):
        """Test all valid emails pass validation"""
        for valid_email in user_login_fixtures["valid_emails"]:
            schema = UserLoginCreate(
                email_id=valid_email,
                mobile_number="9876543210"
            )
            assert "@" in schema.email_id
            assert "." in schema.email_id
