"""
Unit tests for user_master Pydantic schemas and field validators
Phase 3.1: Models & Validators Tests
Date: 2026-03-03

Test Coverage:
- UserCreate model validation
- UserUpdate model validation
- Email format validation
- Mobile number format validation
- Status values validation
- Role name validation
- Response model creation
"""

import pytest
from pydantic import ValidationError

from src.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserBase,
    UserSearchResponse, UserCreateResponse, UserUpdateResponse
)


# ============================================================================
# TESTS: EMAIL VALIDATION
# ============================================================================

class TestEmailValidation:
    """Test email format validation"""

    @pytest.mark.unit
    @pytest.mark.validation
    def test_valid_email_formats(self, valid_emails):
        """Test that valid email formats are accepted"""
        for email in valid_emails:
            user = UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                emailId=email,
                mobileNumber=9876543210,
                status="active"
            )
            assert user.emailId == email.lower()  # Email should be lowercased

    @pytest.mark.unit
    @pytest.mark.validation
    def test_invalid_email_formats(self, invalid_emails):
        """Test that invalid email formats are rejected"""
        for email in invalid_emails:
            with pytest.raises(ValidationError) as exc_info:
                UserCreate(
                    firstName="John",
                    lastName="Doe",
                    currentRole="ADMIN",
                    emailId=email,
                    mobileNumber=9876543210,
                    status="active"
                )
            assert "Invalid email format" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.validation
    def test_email_case_normalization(self):
        """Test that email is normalized to lowercase"""
        user = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="JOHN@EXAMPLE.COM",
            mobileNumber=9876543210,
            status="active"
        )
        assert user.emailId == "john@example.com"

    @pytest.mark.unit
    @pytest.mark.validation
    def test_email_required_in_create(self):
        """Test that email is required in UserCreate"""
        with pytest.raises(ValidationError):
            UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                mobileNumber=9876543210,
                status="active"
            )

    @pytest.mark.unit
    @pytest.mark.validation
    def test_email_optional_in_update(self):
        """Test that email is optional in UserUpdate"""
        user = UserUpdate(
            firstName="John",
            commentLog="Updated first name"
        )
        assert user.emailId is None
        assert user.firstName == "John"


# ============================================================================
# TESTS: MOBILE NUMBER VALIDATION
# ============================================================================

class TestMobileNumberValidation:
    """Test mobile number format validation"""

    @pytest.mark.unit
    @pytest.mark.validation
    def test_valid_mobile_numbers(self, valid_mobile_numbers):
        """Test that valid mobile numbers are accepted"""
        for mobile in valid_mobile_numbers:
            user = UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=mobile,
                status="active"
            )
            assert user.mobileNumber == mobile

    @pytest.mark.unit
    @pytest.mark.validation
    def test_invalid_mobile_numbers(self, invalid_mobile_numbers):
        """Test that invalid mobile numbers are rejected"""
        for mobile in invalid_mobile_numbers:
            with pytest.raises(ValidationError) as exc_info:
                UserCreate(
                    firstName="John",
                    lastName="Doe",
                    currentRole="ADMIN",
                    emailId="john@example.com",
                    mobileNumber=mobile,
                    status="active"
                )
            # Check for Pydantic v2 constraint validation messages (greater/less than or equal)
            error_str = str(exc_info.value).lower()
            assert "greater than or equal" in error_str or "less than or equal" in error_str or "10 digits" in error_str

    @pytest.mark.unit
    @pytest.mark.validation
    def test_mobile_boundary_values(self):
        """Test mobile number boundary values"""
        # Minimum valid value
        user_min = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="john@example.com",
            mobileNumber=1000000000,
            status="active"
        )
        assert user_min.mobileNumber == 1000000000

        # Maximum valid value
        user_max = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="john@example.com",
            mobileNumber=9999999999,
            status="active"
        )
        assert user_max.mobileNumber == 9999999999

    @pytest.mark.unit
    @pytest.mark.validation
    def test_mobile_below_minimum(self):
        """Test mobile number below minimum"""
        with pytest.raises(ValidationError):
            UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=999999999,  # Below 1000000000
                status="active"
            )

    @pytest.mark.unit
    @pytest.mark.validation
    def test_mobile_above_maximum(self):
        """Test mobile number above maximum"""
        with pytest.raises(ValidationError):
            UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=10000000000,  # Above 9999999999
                status="active"
            )


# ============================================================================
# TESTS: STATUS VALIDATION
# ============================================================================

class TestStatusValidation:
    """Test status field validation"""

    @pytest.mark.unit
    @pytest.mark.validation
    def test_valid_statuses(self, valid_statuses):
        """Test that valid statuses are accepted"""
        for status in valid_statuses:
            user = UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=9876543210,
                status=status
            )
            assert user.status == status.lower()

    @pytest.mark.unit
    @pytest.mark.validation
    def test_invalid_statuses(self, invalid_statuses):
        """Test that invalid statuses are rejected"""
        for status in invalid_statuses:
            with pytest.raises(ValidationError) as exc_info:
                UserCreate(
                    firstName="John",
                    lastName="Doe",
                    currentRole="ADMIN",
                    emailId="john@example.com",
                    mobileNumber=9876543210,
                    status=status
                )
            assert "Status must be one of" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.validation
    def test_status_case_insensitive(self):
        """Test that status is case-insensitive but stored as lowercase"""
        for case_variant in ["ACTIVE", "Active", "aCtIvE"]:
            user = UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=9876543210,
                status=case_variant
            )
            assert user.status == "active"

    @pytest.mark.unit
    @pytest.mark.validation
    def test_status_default_value(self):
        """Test that status defaults to 'active'"""
        user = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="john@example.com",
            mobileNumber=9876543210
        )
        assert user.status == "active"


# ============================================================================
# TESTS: ROLE VALIDATION
# ============================================================================

class TestRoleValidation:
    """Test currentRole field validation"""

    @pytest.mark.unit
    @pytest.mark.validation
    def test_valid_roles(self, valid_roles):
        """Test that valid roles are accepted"""
        for role in valid_roles:
            user = UserCreate(
                firstName="John",
                lastName="Doe",
                currentRole=role,
                emailId="john@example.com",
                mobileNumber=9876543210,
                status="active"
            )
            assert user.currentRole == role.upper()

    @pytest.mark.unit
    @pytest.mark.validation
    def test_invalid_roles(self, invalid_roles):
        """Test that invalid roles are rejected"""
        for role in invalid_roles:
            with pytest.raises(ValidationError) as exc_info:
                UserCreate(
                    firstName="John",
                    lastName="Doe",
                    currentRole=role,
                    emailId="john@example.com",
                    mobileNumber=9876543210,
                    status="active"
                )
            assert "Invalid role" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.validation
    def test_role_case_normalization(self):
        """Test that role is normalized to uppercase"""
        user = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="admin",
            emailId="john@example.com",
            mobileNumber=9876543210,
            status="active"
        )
        assert user.currentRole == "ADMIN"

    @pytest.mark.unit
    @pytest.mark.validation
    def test_role_required_in_create(self):
        """Test that role is required in UserCreate"""
        with pytest.raises(ValidationError):
            UserCreate(
                firstName="John",
                lastName="Doe",
                emailId="john@example.com",
                mobileNumber=9876543210,
                status="active"
            )


# ============================================================================
# TESTS: NAME VALIDATION
# ============================================================================

class TestNameValidation:
    """Test firstName and lastName validation"""

    @pytest.mark.unit
    @pytest.mark.validation
    def test_valid_names(self):
        """Test that valid names are accepted"""
        user = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="john@example.com",
            mobileNumber=9876543210,
            status="active"
        )
        assert user.firstName == "John"
        assert user.lastName == "Doe"

    @pytest.mark.unit
    @pytest.mark.validation
    def test_name_max_length(self):
        """Test that names are limited to 50 characters"""
        with pytest.raises(ValidationError):
            UserCreate(
                firstName="A" * 51,  # 51 characters
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=9876543210,
                status="active"
            )

    @pytest.mark.unit
    @pytest.mark.validation
    def test_name_required(self):
        """Test that firstName and lastName are required"""
        with pytest.raises(ValidationError):
            UserCreate(
                lastName="Doe",
                currentRole="ADMIN",
                emailId="john@example.com",
                mobileNumber=9876543210,
                status="active"
            )


# ============================================================================
# TESTS: USER_CREATE MODEL
# ============================================================================

class TestUserCreateModel:
    """Test UserCreate model creation"""

    @pytest.mark.unit
    def test_complete_user_creation(self, test_user_data):
        """Test creating a user with all fields"""
        user = UserCreate(**test_user_data)
        assert user.firstName == test_user_data["firstName"]
        assert user.lastName == test_user_data["lastName"]
        assert user.currentRole == test_user_data["currentRole"]
        assert user.emailId == test_user_data["emailId"].lower()
        assert user.mobileNumber == test_user_data["mobileNumber"]

    @pytest.mark.unit
    def test_minimal_user_creation(self):
        """Test creating a user with only required fields"""
        user = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="john@example.com",
            mobileNumber=9876543210
        )
        assert user.firstName == "John"
        assert user.status == "active"  # Default
        assert user.organisation is None

    @pytest.mark.unit
    def test_user_create_optional_fields(self):
        """Test that optional fields can be omitted"""
        user = UserCreate(
            firstName="John",
            lastName="Doe",
            currentRole="ADMIN",
            emailId="john@example.com",
            mobileNumber=9876543210,
            organisation=None,
            address1=None
        )
        assert user.organisation is None
        assert user.address1 is None


# ============================================================================
# TESTS: USER_UPDATE MODEL
# ============================================================================

class TestUserUpdateModel:
    """Test UserUpdate model"""

    @pytest.mark.unit
    def test_update_single_field(self):
        """Test updating a single field"""
        user = UserUpdate(
            firstName="Jonathan",
            commentLog="Updated first name"
        )
        assert user.firstName == "Jonathan"
        assert user.lastName is None
        assert user.commentLog == "Updated first name"

    @pytest.mark.unit
    def test_update_multiple_fields(self, test_user_update_data):
        """Test updating multiple fields"""
        user = UserUpdate(**test_user_update_data)
        assert user.firstName == "Jonathan"
        assert user.organisation == "New Hospital"
        assert user.status == "pending"
        assert user.commentLog == test_user_update_data["commentLog"]

    @pytest.mark.unit
    def test_update_requires_at_least_one_field(self):
        """Test that at least one field is required in update"""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(commentLog="No other field provided")
        assert "At least one field must be provided" in str(exc_info.value)

    @pytest.mark.unit
    def test_update_comment_log_required(self):
        """Test that commentLog is required in UserUpdate"""
        with pytest.raises(ValidationError):
            UserUpdate(firstName="Jonathan")

    @pytest.mark.unit
    def test_update_all_fields_optional_except_comment_log(self):
        """Test that all fields are optional except commentLog"""
        # Should fail because no other field provided (only commentLog)
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(commentLog="Updated user")
        assert "At least one field must be provided" in str(exc_info.value)


# ============================================================================
# TESTS: USER_RESPONSE MODEL
# ============================================================================

class TestUserResponseModel:
    """Test UserResponse model"""

    @pytest.mark.unit
    def test_user_response_creation(self, test_user_data):
        """Test creating a UserResponse with all fields"""
        from datetime import datetime
        test_user_data['userId'] = 'USER_001'
        test_user_data['createdDate'] = datetime.now()
        test_user_data['updatedDate'] = datetime.now()

        response = UserResponse(**test_user_data)
        assert response.userId == 'USER_001'
        assert response.firstName == test_user_data['firstName']
        assert response.createdDate is not None


# ============================================================================
# TESTS: SEARCH RESPONSE MODEL
# ============================================================================

class TestSearchResponseModel:
    """Test UserSearchResponse model"""

    @pytest.mark.unit
    def test_search_response_found(self, test_user_data):
        """Test search response when user is found"""
        from datetime import datetime
        test_user_data['userId'] = 'USER_001'
        test_user_data['createdDate'] = datetime.now()
        test_user_data['updatedDate'] = datetime.now()

        response_data = UserResponse(**test_user_data)
        response = UserSearchResponse(
            data=response_data,
            existsFlag=True
        )
        assert response.data is not None
        assert response.existsFlag is True

    @pytest.mark.unit
    def test_search_response_not_found(self):
        """Test search response when user is not found"""
        response = UserSearchResponse(
            data=None,
            existsFlag=False
        )
        assert response.data is None
        assert response.existsFlag is False


# ============================================================================
# INTEGRATION TESTS: FULL WORKFLOW
# ============================================================================

class TestFullWorkflow:
    """Test complete user workflows"""

    @pytest.mark.integration
    def test_create_then_update_workflow(self, test_user_data, test_user_update_data):
        """Test creating a user then updating it"""
        # Create user
        user = UserCreate(**test_user_data)
        assert user.firstName == "John"

        # Update user
        update = UserUpdate(**test_user_update_data)
        assert update.firstName == "Jonathan"
        assert update.commentLog is not None
