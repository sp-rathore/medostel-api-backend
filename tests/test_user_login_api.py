"""
User_Login API Endpoint Tests
Date: March 3, 2026
Purpose: Test REST API endpoints for user login operations
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI
from src.routes.v1.user_login import router


# Create a test FastAPI app
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestAuthenticateEndpoint:
    """Test GET /api/v1/user-login/authenticate endpoint"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_with_email_success(self):
        """Test successful authentication with email"""
        with patch('src.routes.v1.user_login.UserLoginManager.get_user_login_by_email') as mock_get, \
             patch('src.routes.v1.user_login.UserLoginManager.update_last_login') as mock_update:

            mock_get.return_value = {
                "email_id": "user@example.com",
                "password": "hashed_password",
                "mobile_number": "9876543210",
                "is_active": "Y",
                "last_login": None
            }
            mock_update.return_value = (True, {}, "Updated")

            response = client.get(
                "/api/v1/user-login/authenticate",
                params={"email_id": "user@example.com"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert data["data"]["email_id"] == "user@example.com"

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_with_mobile_success(self):
        """Test successful authentication with mobile"""
        with patch('src.routes.v1.user_login.UserLoginManager.get_user_login_by_mobile') as mock_get, \
             patch('src.routes.v1.user_login.UserLoginManager.update_last_login') as mock_update:

            mock_get.return_value = {
                "email_id": "user@example.com",
                "password": "hashed_password",
                "mobile_number": "9876543210",
                "is_active": "Y",
                "last_login": None
            }
            mock_update.return_value = (True, {}, "Updated")

            response = client.get(
                "/api/v1/user-login/authenticate",
                params={"mobile_number": "9876543210"}
            )

            assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_missing_both_params(self):
        """Test authenticate without email or mobile"""
        response = client.get("/api/v1/user-login/authenticate")
        assert response.status_code == 400
        assert "must be provided" in response.json()["detail"].lower()

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_invalid_email_format(self):
        """Test authenticate with invalid email format"""
        response = client.get(
            "/api/v1/user-login/authenticate",
            params={"email_id": "invalid_email"}
        )
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_invalid_mobile_format(self):
        """Test authenticate with invalid mobile format"""
        response = client.get(
            "/api/v1/user-login/authenticate",
            params={"mobile_number": "123"}
        )
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_not_found(self):
        """Test authenticate when login not found"""
        with patch('src.routes.v1.user_login.UserLoginManager.get_user_login_by_email', return_value=None):
            response = client.get(
                "/api/v1/user-login/authenticate",
                params={"email_id": "notfound@example.com"}
            )
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()


class TestCreateEndpoint:
    """Test POST /api/v1/user-login/create endpoint"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_success_with_password(self):
        """Test successful login creation with password"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:30:00"
                },
                "User login created successfully"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "password": "SecurePassword123"
                }
            )

            assert response.status_code == 201
            data = response.json()
            assert data["data"]["email_id"] == "user@example.com"
            assert data["data"]["is_active"] == "Y"

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_success_without_password(self):
        """Test successful login creation without password (uses default)"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:30:00"
                },
                "User login created successfully"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210"
                }
            )

            assert response.status_code == 201

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_email_not_found(self):
        """Test create when email not in user_master"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                False,
                {},
                "Email not registered in user_master"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "notfound@example.com",
                    "mobile_number": "9876543210",
                    "password": "SecurePassword123"
                }
            )

            assert response.status_code == 404
            assert "not registered" in response.json()["detail"].lower()

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_mobile_mismatch(self):
        """Test create when mobile doesn't match email"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                False,
                {},
                "Mobile number doesn't match registered mobile for this email"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "1111111111",
                    "password": "SecurePassword123"
                }
            )

            assert response.status_code == 409
            assert "doesn't match" in response.json()["detail"].lower()

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_user_not_active(self):
        """Test create when user not active in user_master"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                False,
                {},
                "User account is not active in user_master"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "password": "SecurePassword123"
                }
            )

            assert response.status_code == 422
            assert "not active" in response.json()["detail"].lower()

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_duplicate_login(self):
        """Test create when login already exists"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                False,
                {},
                "Login credentials already exist for this email"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "password": "SecurePassword123"
                }
            )

            assert response.status_code == 409
            assert "already exist" in response.json()["detail"].lower()

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_invalid_email(self):
        """Test create with invalid email format"""
        response = client.post(
            "/api/v1/user-login/create",
            json={
                "email_id": "invalid_email",
                "mobile_number": "9876543210",
                "password": "SecurePassword123"
            }
        )
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_invalid_mobile(self):
        """Test create with invalid mobile format"""
        response = client.post(
            "/api/v1/user-login/create",
            json={
                "email_id": "user@example.com",
                "mobile_number": "123",
                "password": "SecurePassword123"
            }
        )
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_short_password(self):
        """Test create with password too short"""
        response = client.post(
            "/api/v1/user-login/create",
            json={
                "email_id": "user@example.com",
                "mobile_number": "9876543210",
                "password": "short"
            }
        )
        assert response.status_code == 422


class TestUpdatePasswordEndpoint:
    """Test PUT /api/v1/user-login/password endpoint"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_password_success(self):
        """Test successful password update"""
        with patch('src.routes.v1.user_login.UserLoginManager.update_password') as mock_update:
            mock_update.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": "2026-03-03T10:25:00",
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:35:00"
                },
                "Password updated successfully"
            )

            response = client.put(
                "/api/v1/user-login/password",
                json={
                    "email_id": "user@example.com",
                    "new_password": "NewSecurePassword456"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["updated_date"] != data["data"]["created_date"]

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_password_not_found(self):
        """Test password update when login not found"""
        with patch('src.routes.v1.user_login.UserLoginManager.update_password') as mock_update:
            mock_update.return_value = (
                False,
                {},
                "User login record not found"
            )

            response = client.put(
                "/api/v1/user-login/password",
                json={
                    "email_id": "notfound@example.com",
                    "new_password": "NewSecurePassword456"
                }
            )

            assert response.status_code == 404

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_password_short_password(self):
        """Test password update with password too short"""
        response = client.put(
            "/api/v1/user-login/password",
            json={
                "email_id": "user@example.com",
                "new_password": "short"
            }
        )
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_password_invalid_email(self):
        """Test password update with invalid email"""
        response = client.put(
            "/api/v1/user-login/password",
            json={
                "email_id": "invalid_email",
                "new_password": "NewSecurePassword456"
            }
        )
        assert response.status_code == 422


class TestUpdateStatusEndpoint:
    """Test PUT /api/v1/user-login/status endpoint"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_status_to_active(self):
        """Test updating status to active"""
        with patch('src.routes.v1.user_login.UserLoginManager.update_is_active') as mock_update:
            mock_update.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:40:00"
                },
                "User status updated successfully"
            )

            response = client.put(
                "/api/v1/user-login/status",
                json={
                    "email_id": "user@example.com",
                    "is_active": "Y"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["is_active"] == "Y"

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_status_to_inactive(self):
        """Test updating status to inactive"""
        with patch('src.routes.v1.user_login.UserLoginManager.update_is_active') as mock_update:
            mock_update.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "N",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:40:00"
                },
                "User status updated successfully"
            )

            response = client.put(
                "/api/v1/user-login/status",
                json={
                    "email_id": "user@example.com",
                    "is_active": "N"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["is_active"] == "N"

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_status_invalid_value(self):
        """Test status update with invalid value"""
        response = client.put(
            "/api/v1/user-login/status",
            json={
                "email_id": "user@example.com",
                "is_active": "INVALID"
            }
        )
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_status_not_found(self):
        """Test status update when login not found"""
        with patch('src.routes.v1.user_login.UserLoginManager.update_is_active') as mock_update:
            mock_update.return_value = (
                False,
                {},
                "User login record not found"
            )

            response = client.put(
                "/api/v1/user-login/status",
                json={
                    "email_id": "notfound@example.com",
                    "is_active": "Y"
                }
            )

            assert response.status_code == 404

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_status_invalid_email(self):
        """Test status update with invalid email"""
        response = client.put(
            "/api/v1/user-login/status",
            json={
                "email_id": "invalid_email",
                "is_active": "Y"
            }
        )
        assert response.status_code == 422


class TestHealthCheckEndpoint:
    """Test GET /api/v1/user-login/health endpoint"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_health_check_success(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/user-login/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "user_login"
        assert "timestamp" in data


class TestResponseFormats:
    """Test response format consistency"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_response_format(self):
        """Test create response has correct format"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:30:00"
                },
                "User login created successfully"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210"
                }
            )

            data = response.json()
            assert "message" in data
            assert "data" in data
            assert data["data"]["email_id"] == "user@example.com"
            assert data["data"]["mobile_number"] == "9876543210"
            assert data["data"]["is_active"] == "Y"
            assert "password" not in data["data"]  # Password should not be in response

    @pytest.mark.api
    @pytest.mark.unit
    def test_update_response_format(self):
        """Test update response has correct format"""
        with patch('src.routes.v1.user_login.UserLoginManager.update_password') as mock_update:
            mock_update.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:35:00"
                },
                "Password updated successfully"
            )

            response = client.put(
                "/api/v1/user-login/password",
                json={
                    "email_id": "user@example.com",
                    "new_password": "NewPassword123"
                }
            )

            data = response.json()
            assert "message" in data
            assert "data" in data
            assert "password" not in data["data"]  # Password should not be in response


class TestErrorHandling:
    """Test error handling in endpoints"""

    @pytest.mark.api
    @pytest.mark.unit
    def test_authenticate_database_error(self):
        """Test authenticate endpoint handles database error"""
        with patch('src.routes.v1.user_login.UserLoginManager.get_user_login_by_email') as mock_get:
            mock_get.side_effect = Exception("Database error")

            response = client.get(
                "/api/v1/user-login/authenticate",
                params={"email_id": "user@example.com"}
            )

            assert response.status_code == 500

    @pytest.mark.api
    @pytest.mark.unit
    def test_create_database_error(self):
        """Test create endpoint handles database error"""
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.side_effect = Exception("Database error")

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210"
                }
            )

            assert response.status_code == 500


class TestAPIWorkflows:
    """Test complete API workflows"""

    @pytest.mark.api
    @pytest.mark.integration
    def test_create_then_authenticate_workflow(self):
        """Test create login then authenticate flow"""
        # First create
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:30:00"
                },
                "User login created successfully"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "password": "SecurePassword123"
                }
            )
            assert response.status_code == 201

        # Then authenticate
        with patch('src.routes.v1.user_login.UserLoginManager.get_user_login_by_email') as mock_get, \
             patch('src.routes.v1.user_login.UserLoginManager.update_last_login') as mock_update:

            mock_get.return_value = {
                "email_id": "user@example.com",
                "password": "hashed_password",
                "mobile_number": "9876543210",
                "is_active": "Y",
                "last_login": None
            }
            mock_update.return_value = (True, {}, "Updated")

            response = client.get(
                "/api/v1/user-login/authenticate",
                params={"email_id": "user@example.com"}
            )
            assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.integration
    def test_create_update_password_workflow(self):
        """Test create login then update password flow"""
        # Create
        with patch('src.routes.v1.user_login.UserLoginManager.create_user_login') as mock_create:
            mock_create.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:30:00"
                },
                "User login created successfully"
            )

            response = client.post(
                "/api/v1/user-login/create",
                json={
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210"
                }
            )
            assert response.status_code == 201

        # Update password
        with patch('src.routes.v1.user_login.UserLoginManager.update_password') as mock_update:
            mock_update.return_value = (
                True,
                {
                    "email_id": "user@example.com",
                    "mobile_number": "9876543210",
                    "is_active": "Y",
                    "last_login": None,
                    "created_date": "2026-03-03T10:30:00",
                    "updated_date": "2026-03-03T10:35:00"
                },
                "Password updated successfully"
            )

            response = client.put(
                "/api/v1/user-login/password",
                json={
                    "email_id": "user@example.com",
                    "new_password": "NewPassword123"
                }
            )
            assert response.status_code == 200
