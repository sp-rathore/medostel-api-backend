"""
User_Login Database Utility Tests
Date: March 3, 2026
Purpose: Test database CRUD operations and validation
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.db.user_login_utils import UserLoginManager
from src.utils.password_utils import PasswordManager


class MockCursor:
    """Mock database cursor for testing"""
    def __init__(self):
        self.last_query = None
        self.last_params = None
        self.result = None

    def execute(self, query, params=None):
        self.last_query = query
        self.last_params = params

    def fetchone(self):
        return self.result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockDbConnection:
    """Mock database connection for testing"""
    def __init__(self):
        self.cursor_instance = MockCursor()
        self.committed = False
        self.rolled_back = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


class TestEmailExistsValidation:
    """Test email existence validation"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_email_exists_true(self):
        """Test email exists in user_master"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (1,)

        result = UserLoginManager.email_exists_in_user_master(
            "user@example.com",
            mock_conn
        )
        assert result is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_email_exists_false(self):
        """Test email does not exist in user_master"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (0,)

        result = UserLoginManager.email_exists_in_user_master(
            "nonexistent@example.com",
            mock_conn
        )
        assert result is False

    @pytest.mark.database
    @pytest.mark.unit
    def test_email_exists_exception_handling(self):
        """Test exception handling in email existence check"""
        mock_conn = Mock()
        mock_conn.cursor.side_effect = Exception("Database error")

        result = UserLoginManager.email_exists_in_user_master(
            "user@example.com",
            mock_conn
        )
        assert result is False


class TestMobileMatchesValidation:
    """Test mobile number matching validation"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_mobile_matches_email(self):
        """Test mobile matches email in user_master"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (9876543210,)

        result = UserLoginManager.mobile_matches_email(
            "user@example.com",
            "9876543210",
            mock_conn
        )
        assert result is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_mobile_does_not_match_email(self):
        """Test mobile does not match email in user_master"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (9876543210,)

        result = UserLoginManager.mobile_matches_email(
            "user@example.com",
            "1111111111",
            mock_conn
        )
        assert result is False

    @pytest.mark.database
    @pytest.mark.unit
    def test_mobile_match_email_not_found(self):
        """Test when email not found in user_master"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = None

        result = UserLoginManager.mobile_matches_email(
            "nonexistent@example.com",
            "9876543210",
            mock_conn
        )
        assert result is False


class TestUserStatusValidation:
    """Test user status validation"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_user_status_active(self):
        """Test user status is active"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = ("active",)

        result = UserLoginManager.user_status_is_active(
            "user@example.com",
            mock_conn
        )
        assert result is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_user_status_not_active(self):
        """Test user status is not active"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = ("inactive",)

        result = UserLoginManager.user_status_is_active(
            "user@example.com",
            mock_conn
        )
        assert result is False

    @pytest.mark.database
    @pytest.mark.unit
    def test_user_status_case_insensitive(self):
        """Test user status check is case insensitive"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = ("Active",)

        result = UserLoginManager.user_status_is_active(
            "user@example.com",
            mock_conn
        )
        assert result is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_user_status_email_not_found(self):
        """Test when email not found"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = None

        result = UserLoginManager.user_status_is_active(
            "nonexistent@example.com",
            mock_conn
        )
        assert result is False


class TestLoginExistsValidation:
    """Test login existence validation"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_login_exists_true(self):
        """Test login record exists"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (1,)

        result = UserLoginManager.login_exists_for_email(
            "user@example.com",
            mock_conn
        )
        assert result is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_login_exists_false(self):
        """Test login record does not exist"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (0,)

        result = UserLoginManager.login_exists_for_email(
            "user@example.com",
            mock_conn
        )
        assert result is False


class TestGetUserLogin:
    """Test retrieving user login records"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_get_user_login_by_email_success(self):
        """Test retrieving user login by email"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (
            "user@example.com",
            "$2b$12$hashedpassword",
            9876543210,
            "Y",
            None,
            "2026-03-03 10:30:00",
            "2026-03-03 10:30:00"
        )

        result = UserLoginManager.get_user_login_by_email(
            "user@example.com",
            mock_conn
        )
        assert result is not None
        assert result["email_id"] == "user@example.com"
        assert result["is_active"] == "Y"

    @pytest.mark.database
    @pytest.mark.unit
    def test_get_user_login_by_email_not_found(self):
        """Test when login not found by email"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = None

        result = UserLoginManager.get_user_login_by_email(
            "nonexistent@example.com",
            mock_conn
        )
        assert result is None

    @pytest.mark.database
    @pytest.mark.unit
    def test_get_user_login_by_mobile_success(self):
        """Test retrieving user login by mobile"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = (
            "user@example.com",
            "$2b$12$hashedpassword",
            9876543210,
            "Y",
            None,
            "2026-03-03 10:30:00",
            "2026-03-03 10:30:00"
        )

        result = UserLoginManager.get_user_login_by_mobile(
            "9876543210",
            mock_conn
        )
        assert result is not None
        assert result["mobile_number"] == "9876543210"

    @pytest.mark.database
    @pytest.mark.unit
    def test_get_user_login_by_mobile_not_found(self):
        """Test when login not found by mobile"""
        mock_conn = MockDbConnection()
        mock_conn.cursor_instance.result = None

        result = UserLoginManager.get_user_login_by_mobile(
            "9999999999",
            mock_conn
        )
        assert result is None


class TestCreateUserLogin:
    """Test creating user login records"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_create_user_login_success(self):
        """Test successful login creation"""
        mock_conn = MockDbConnection()

        # Mock the validation checks
        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=True), \
             patch.object(UserLoginManager, 'mobile_matches_email', return_value=True), \
             patch.object(UserLoginManager, 'user_status_is_active', return_value=True), \
             patch.object(UserLoginManager, 'login_exists_for_email', return_value=False):

            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$hashedpassword",
                9876543210,
                "Y",
                None,
                "2026-03-03 10:30:00",
                "2026-03-03 10:30:00"
            )

            success, data, message = UserLoginManager.create_user_login(
                "user@example.com",
                "9876543210",
                "MyPassword123",
                mock_conn
            )

            assert success is True
            assert data["email_id"] == "user@example.com"
            assert data["is_active"] == "Y"
            assert mock_conn.committed is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_create_user_login_email_not_found(self):
        """Test creation fails when email not in user_master"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=False):
            success, data, message = UserLoginManager.create_user_login(
                "nonexistent@example.com",
                "9876543210",
                "MyPassword123",
                mock_conn
            )

            assert success is False
            assert "not registered" in message.lower()

    @pytest.mark.database
    @pytest.mark.unit
    def test_create_user_login_mobile_mismatch(self):
        """Test creation fails when mobile doesn't match"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=True), \
             patch.object(UserLoginManager, 'mobile_matches_email', return_value=False):

            success, data, message = UserLoginManager.create_user_login(
                "user@example.com",
                "1111111111",
                "MyPassword123",
                mock_conn
            )

            assert success is False
            assert "doesn't match" in message.lower()

    @pytest.mark.database
    @pytest.mark.unit
    def test_create_user_login_user_not_active(self):
        """Test creation fails when user not active"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=True), \
             patch.object(UserLoginManager, 'mobile_matches_email', return_value=True), \
             patch.object(UserLoginManager, 'user_status_is_active', return_value=False):

            success, data, message = UserLoginManager.create_user_login(
                "user@example.com",
                "9876543210",
                "MyPassword123",
                mock_conn
            )

            assert success is False
            assert "not active" in message.lower()

    @pytest.mark.database
    @pytest.mark.unit
    def test_create_user_login_duplicate(self):
        """Test creation fails when login already exists"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=True), \
             patch.object(UserLoginManager, 'mobile_matches_email', return_value=True), \
             patch.object(UserLoginManager, 'user_status_is_active', return_value=True), \
             patch.object(UserLoginManager, 'login_exists_for_email', return_value=True):

            success, data, message = UserLoginManager.create_user_login(
                "user@example.com",
                "9876543210",
                "MyPassword123",
                mock_conn
            )

            assert success is False
            assert "already exist" in message.lower()

    @pytest.mark.database
    @pytest.mark.unit
    def test_create_user_login_with_default_password(self):
        """Test creation with default password"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=True), \
             patch.object(UserLoginManager, 'mobile_matches_email', return_value=True), \
             patch.object(UserLoginManager, 'user_status_is_active', return_value=True), \
             patch.object(UserLoginManager, 'login_exists_for_email', return_value=False):

            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$hasheddefault",
                9876543210,
                "Y",
                None,
                "2026-03-03 10:30:00",
                "2026-03-03 10:30:00"
            )

            success, data, message = UserLoginManager.create_user_login(
                "user@example.com",
                "9876543210",
                None,  # No password provided
                mock_conn
            )

            assert success is True
            assert "created successfully" in message.lower()


class TestUpdatePassword:
    """Test password update functionality"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_password_success(self):
        """Test successful password update"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'get_user_login_by_email') as mock_get:
            mock_get.return_value = {
                "email_id": "user@example.com",
                "password": "$2b$12$oldpassword",
                "mobile_number": "9876543210",
                "is_active": "Y",
                "last_login": None,
                "created_date": "2026-03-03 10:30:00",
                "updated_date": "2026-03-03 10:30:00"
            }

            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$newpassword",
                9876543210,
                "Y",
                None,
                "2026-03-03 10:30:00",
                "2026-03-03 10:35:00"
            )

            success, data, message = UserLoginManager.update_password(
                "user@example.com",
                "NewPassword123",
                mock_conn
            )

            assert success is True
            assert "password updated" in message.lower()
            assert mock_conn.committed is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_password_not_found(self):
        """Test password update when login not found"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'get_user_login_by_email', return_value=None):
            success, data, message = UserLoginManager.update_password(
                "nonexistent@example.com",
                "NewPassword123",
                mock_conn
            )

            assert success is False
            assert "not found" in message.lower()


class TestUpdateStatus:
    """Test status update functionality"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_status_to_active(self):
        """Test updating status to active"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'get_user_login_by_email') as mock_get:
            mock_get.return_value = {
                "email_id": "user@example.com",
                "password": "$2b$12$hashedpassword",
                "mobile_number": "9876543210",
                "is_active": "N",
                "last_login": None,
                "created_date": "2026-03-03 10:30:00",
                "updated_date": "2026-03-03 10:30:00"
            }

            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$hashedpassword",
                9876543210,
                "Y",
                None,
                "2026-03-03 10:30:00",
                "2026-03-03 10:40:00"
            )

            success, data, message = UserLoginManager.update_is_active(
                "user@example.com",
                "Y",
                mock_conn
            )

            assert success is True
            assert data["is_active"] == "Y"
            assert mock_conn.committed is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_status_invalid_value(self):
        """Test updating status with invalid value"""
        mock_conn = MockDbConnection()

        success, data, message = UserLoginManager.update_is_active(
            "user@example.com",
            "INVALID",
            mock_conn
        )

        assert success is False
        assert "must be Y or N" in message

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_status_not_found(self):
        """Test status update when login not found"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'get_user_login_by_email', return_value=None):
            success, data, message = UserLoginManager.update_is_active(
                "nonexistent@example.com",
                "Y",
                mock_conn
            )

            assert success is False
            assert "not found" in message.lower()


class TestUpdateLastLogin:
    """Test last login update functionality"""

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_last_login_success(self):
        """Test successful last login update"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'get_user_login_by_email') as mock_get:
            mock_get.return_value = {
                "email_id": "user@example.com",
                "password": "$2b$12$hashedpassword",
                "mobile_number": "9876543210",
                "is_active": "Y",
                "last_login": None,
                "created_date": "2026-03-03 10:30:00",
                "updated_date": "2026-03-03 10:30:00"
            }

            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$hashedpassword",
                9876543210,
                "Y",
                "2026-03-03 10:35:00",
                "2026-03-03 10:30:00",
                "2026-03-03 10:30:00"
            )

            success, data, message = UserLoginManager.update_last_login(
                "user@example.com",
                mock_conn
            )

            assert success is True
            assert data["last_login"] is not None
            assert mock_conn.committed is True

    @pytest.mark.database
    @pytest.mark.unit
    def test_update_last_login_not_found(self):
        """Test last login update when not found"""
        mock_conn = MockDbConnection()

        with patch.object(UserLoginManager, 'get_user_login_by_email', return_value=None):
            success, data, message = UserLoginManager.update_last_login(
                "nonexistent@example.com",
                mock_conn
            )

            assert success is False
            assert "not found" in message.lower()


class TestDatabaseIntegration:
    """Integration tests for database operations"""

    @pytest.mark.database
    @pytest.mark.integration
    def test_create_authenticate_update_flow(self):
        """Test complete flow: create -> authenticate -> update"""
        mock_conn = MockDbConnection()

        # Step 1: Create login
        with patch.object(UserLoginManager, 'email_exists_in_user_master', return_value=True), \
             patch.object(UserLoginManager, 'mobile_matches_email', return_value=True), \
             patch.object(UserLoginManager, 'user_status_is_active', return_value=True), \
             patch.object(UserLoginManager, 'login_exists_for_email', return_value=False):

            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$hashedpassword",
                9876543210,
                "Y",
                None,
                "2026-03-03 10:30:00",
                "2026-03-03 10:30:00"
            )

            success, data, msg = UserLoginManager.create_user_login(
                "user@example.com",
                "9876543210",
                "InitialPassword123",
                mock_conn
            )
            assert success is True

        # Step 2: Get login
        mock_conn.cursor_instance.result = (
            "user@example.com",
            "$2b$12$hashedpassword",
            9876543210,
            "Y",
            None,
            "2026-03-03 10:30:00",
            "2026-03-03 10:30:00"
        )

        login = UserLoginManager.get_user_login_by_email(
            "user@example.com",
            mock_conn
        )
        assert login is not None

        # Step 3: Update password
        with patch.object(UserLoginManager, 'get_user_login_by_email', return_value=login):
            mock_conn.cursor_instance.result = (
                "user@example.com",
                "$2b$12$newhashedpassword",
                9876543210,
                "Y",
                None,
                "2026-03-03 10:30:00",
                "2026-03-03 10:35:00"
            )

            success, data, msg = UserLoginManager.update_password(
                "user@example.com",
                "UpdatedPassword456",
                mock_conn
            )
            assert success is True
