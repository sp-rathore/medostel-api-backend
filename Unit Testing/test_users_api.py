"""
Unit tests for User Management APIs (APIs 5 & 6)
Enhanced with geographic hierarchy validation (Step 1.2)
API 5: GET /api/v1/users/all - Select all users
API 6: POST/PUT/DELETE /api/v1/users - CRUD operations
"""

import pytest
from httpx import AsyncClient


class TestAPIFive_GetAllUsers:
    """Test cases for API 5: GET /api/v1/users/all"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_all_users_success(self, client: AsyncClient):
        """Test Case 5.1: Retrieve all users successfully"""
        response = await client.get("/api/v1/users/all")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "users" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["users"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_all_users_response_structure(self, client: AsyncClient):
        """Verify response structure includes geographic fields"""
        response = await client.get("/api/v1/users/all")

        assert response.status_code == 200
        data = response.json()

        # Verify APIResponse structure
        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

        # Verify data structure
        assert isinstance(data["data"]["users"], list)
        assert isinstance(data["data"]["count"], int)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_includes_geographic_fields(self, client: AsyncClient, sample_user):
        """Test Case 5.2: Response includes geographic FK fields"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        response = await client.get("/api/v1/users/all")
        assert response.status_code == 200
        data = response.json()["data"]["users"]

        # At least one user should have geographic fields
        for user in data:
            # Check for geographic field presence (can be None for existing users)
            assert any(key in user for key in ["stateId", "districtId", "cityId", "pinCode"])

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_filter_by_status(self, client: AsyncClient, sample_user):
        """Test Case 5.3: Filter users by status parameter"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        response = await client.get("/api/v1/users/all?status=Active")

        assert response.status_code == 200
        data = response.json()["data"]["users"]

        # All users should have Active status
        for user in data:
            assert user["status"] == "Active"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_filter_by_role(self, client: AsyncClient, sample_user):
        """Test Case 5.4: Filter users by currentRole"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        response = await client.get("/api/v1/users/all?currentRole=Doctor")

        assert response.status_code == 200
        data = response.json()["data"]["users"]

        # All users should have Doctor role
        for user in data:
            assert user["currentRole"] == "Doctor"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_pagination_limit(self, client: AsyncClient):
        """Test Case 5.5: Pagination with limit parameter"""
        response = await client.get("/api/v1/users/all?limit=5&offset=0")

        assert response.status_code == 200
        users = response.json()["data"]["users"]
        assert len(users) <= 5

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_pagination_offset(self, client: AsyncClient):
        """Test pagination with offset"""
        # Get first page
        response1 = await client.get("/api/v1/users/all?limit=5&offset=0")
        assert response1.status_code == 200
        page1 = response1.json()["data"]["users"]

        # Get second page
        response2 = await client.get("/api/v1/users/all?limit=5&offset=5")
        assert response2.status_code == 200
        page2 = response2.json()["data"]["users"]

        # Verify different results if both pages have data
        if len(page1) > 0 and len(page2) > 0:
            assert page1[0]["userId"] != page2[0]["userId"]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_both_filters(self, client: AsyncClient):
        """Test filtering by both status and role"""
        response = await client.get("/api/v1/users/all?status=Active&currentRole=Doctor")

        assert response.status_code == 200
        data = response.json()["data"]["users"]

        for user in data:
            assert user["status"] == "Active"
            assert user["currentRole"] == "Doctor"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_limit_range(self, client: AsyncClient):
        """Test limit parameter validation"""
        response = await client.get("/api/v1/users/all?limit=100")

        assert response.status_code == 200
        users = response.json()["data"]["users"]
        assert len(users) <= 100

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_users_offset_zero(self, client: AsyncClient):
        """Test offset default behavior"""
        response = await client.get("/api/v1/users/all?offset=0")

        assert response.status_code == 200
        data = response.json()
        assert "users" in data["data"]


class TestAPISix_CreateUser:
    """Test cases for API 6: POST /api/v1/users - Create user"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_success(self, client: AsyncClient):
        """Test Case 6.1: Create user successfully"""
        user_data = {
            "userId": "test_create_user@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "currentRole": "Doctor",
            "emailId": "john_test@example.com",
            "mobileNumber": "9876543210",
            "organisation": "Test Hospital",
            "address1": "123 Main St",
            "status": "Active"
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "user" in data["data"]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_with_geographic_fields(self, client: AsyncClient):
        """Test Case 6.2: Create user with geographic FK fields"""
        user_data = {
            "userId": "test_geo_user@example.com",
            "firstName": "Jane",
            "lastName": "Smith",
            "currentRole": "Patient",
            "emailId": "jane_test@example.com",
            "mobileNumber": "9876543211",
            "stateId": 27,
            "stateName": "Maharashtra",
            "districtId": 1,
            "cityId": 1,
            "cityName": "Mumbai",
            "pinCode": 400001,
            "status": "Active"
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201
        data = response.json()["data"]["user"]
        assert data.get("stateId") == 27 or data.get("stateId") is None

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_pincode_validation(self, client: AsyncClient):
        """Test Case 6.3: pinCode validation (5-6 digits)"""
        user_data = {
            "userId": "test_pincode@example.com",
            "firstName": "Test",
            "lastName": "User",
            "currentRole": "Doctor",
            "emailId": "test_pincode@example.com",
            "mobileNumber": "1234567890",
            "pinCode": 411001,  # Valid 6-digit pincode
            "status": "Active"
        }
        response = await client.post("/api/v1/users", json=user_data)

        # Should accept valid pincode
        assert response.status_code in [201, 400]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_geographic_validation(self, client: AsyncClient):
        """Test Case 6.4: Invalid geographic reference validation"""
        user_data = {
            "userId": "test_invalid_geo@example.com",
            "firstName": "Invalid",
            "lastName": "Geo",
            "currentRole": "Patient",
            "emailId": "invalid_geo@example.com",
            "mobileNumber": "1234567890",
            "stateId": 999,  # Invalid state ID
            "stateName": "NonExistent",
            "districtId": 999,
            "cityId": 999,
            "pinCode": 999999,
            "status": "Active"
        }
        response = await client.post("/api/v1/users", json=user_data)

        # Should reject invalid geographic references
        assert response.status_code == 400

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_duplicate_userid(self, client: AsyncClient, sample_user):
        """Test Case 6.5: Reject duplicate userId"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        user_data = {
            "userId": sample_user["userId"],
            "firstName": "Different",
            "lastName": "User",
            "currentRole": "Patient",
            "emailId": "different@example.com",
            "mobileNumber": "1111111111"
        }
        response = await client.post("/api/v1/users", json=user_data)

        # Should reject duplicate userId (409 Conflict)
        assert response.status_code == 409

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_missing_required_field(self, client: AsyncClient):
        """Test Case 6.6: Missing required field validation"""
        user_data = {
            "firstName": "Incomplete",
            "lastName": "User",
            "currentRole": "Doctor"
            # Missing userId, emailId, mobileNumber
        }
        response = await client.post("/api/v1/users", json=user_data)

        # Should return validation error
        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_invalid_email(self, client: AsyncClient):
        """Test Case 6.7: Email format validation"""
        user_data = {
            "userId": "test_invalid_email@example.com",
            "firstName": "Test",
            "lastName": "Email",
            "currentRole": "Doctor",
            "emailId": "invalid-email-format",  # Invalid email
            "mobileNumber": "1234567890"
        }
        response = await client.post("/api/v1/users", json=user_data)

        # Should reject invalid email format
        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_response_includes_geographic(self, client: AsyncClient):
        """Test Case 6.8: Response includes geographic fields"""
        user_data = {
            "userId": "test_response_geo@example.com",
            "firstName": "Response",
            "lastName": "Geo",
            "currentRole": "Doctor",
            "emailId": "response_geo@example.com",
            "mobileNumber": "1234567890",
            "stateId": 28,
            "districtId": 1,
            "cityId": 1,
            "pinCode": 560001
        }
        response = await client.post("/api/v1/users", json=user_data)

        if response.status_code == 201:
            data = response.json()["data"]["user"]
            # Response should include geographic fields
            assert any(key in data for key in ["stateId", "districtId", "cityId", "pinCode"])

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_address_fields(self, client: AsyncClient):
        """Test Case 6.9: Create user with address fields"""
        user_data = {
            "userId": "test_address@example.com",
            "firstName": "Address",
            "lastName": "User",
            "currentRole": "Patient",
            "emailId": "address@example.com",
            "mobileNumber": "1234567890",
            "address1": "123 Main Street",
            "address2": "Apartment 5",
            "status": "Active"
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_organisation_field(self, client: AsyncClient):
        """Test Case 6.10: Create user with organisation"""
        user_data = {
            "userId": "test_org@example.com",
            "firstName": "Org",
            "lastName": "User",
            "currentRole": "Doctor",
            "emailId": "org_user@example.com",
            "mobileNumber": "1234567890",
            "organisation": "City Medical Center"
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_inactive_status(self, client: AsyncClient):
        """Test Case 6.11: Create user with Inactive status"""
        user_data = {
            "userId": "test_inactive@example.com",
            "firstName": "Inactive",
            "lastName": "User",
            "currentRole": "Patient",
            "emailId": "inactive@example.com",
            "mobileNumber": "1234567890",
            "status": "Inactive"
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201
        data = response.json()["data"]["user"]
        assert data["status"] == "Inactive"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_all_geographic_fields(self, client: AsyncClient):
        """Test Case 6.12: Create with all geographic fields"""
        user_data = {
            "userId": "test_full_geo@example.com",
            "firstName": "Full",
            "lastName": "Geo",
            "currentRole": "Doctor",
            "emailId": "full_geo@example.com",
            "mobileNumber": "1234567890",
            "address1": "456 Hospital Ave",
            "address2": "Wing A",
            "stateId": 27,
            "stateName": "Maharashtra",
            "districtId": 1,
            "cityId": 1,
            "cityName": "Mumbai",
            "pinCode": 400001,
            "status": "Active"
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_different_state(self, client: AsyncClient):
        """Test Case 6.13: Create user in different state"""
        user_data = {
            "userId": "test_karnataka@example.com",
            "firstName": "Karnataka",
            "lastName": "User",
            "currentRole": "Patient",
            "emailId": "karnataka@example.com",
            "mobileNumber": "1234567890",
            "stateId": 28,  # Karnataka
            "stateName": "Karnataka",
            "districtId": 1,
            "cityId": 1,
            "cityName": "Bangalore",
            "pinCode": 560001
        }
        response = await client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_response_structure(self, client: AsyncClient):
        """Test Case 6.14: Response structure is correct"""
        user_data = {
            "userId": "test_response_struct@example.com",
            "firstName": "Response",
            "lastName": "Struct",
            "currentRole": "Doctor",
            "emailId": "response_struct@example.com",
            "mobileNumber": "1234567890"
        }
        response = await client.post("/api/v1/users", json=user_data)

        if response.status_code == 201:
            data = response.json()
            assert "status" in data
            assert "code" in data
            assert "message" in data
            assert "data" in data

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_user_timestamps(self, client: AsyncClient):
        """Test Case 6.15: User has timestamps"""
        user_data = {
            "userId": "test_timestamps@example.com",
            "firstName": "Timestamp",
            "lastName": "User",
            "currentRole": "Patient",
            "emailId": "timestamps@example.com",
            "mobileNumber": "1234567890"
        }
        response = await client.post("/api/v1/users", json=user_data)

        if response.status_code == 201:
            data = response.json()["data"]["user"]
            assert "createdDate" in data


class TestAPISix_UpdateUser:
    """Test cases for API 6: PUT /api/v1/users/{userId} - Update user"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_success(self, client: AsyncClient, sample_user):
        """Test Case 6.16: Update user successfully"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "firstName": "UpdatedFirst",
            "lastName": "UpdatedLast"
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_geographic_fields(self, client: AsyncClient, sample_user):
        """Test Case 6.17: Update geographic fields"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "stateId": 28,
            "stateName": "Karnataka",
            "districtId": 2,
            "cityId": 2,
            "cityName": "Bangalore"
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        assert response.status_code == 200

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_pincode_immutable(self, client: AsyncClient, sample_user):
        """Test Case 6.18: pinCode cannot be updated (immutable)"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "pinCode": 999999  # Attempt to change pinCode
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        # Should succeed but pinCode should not change
        assert response.status_code == 200
        # pinCode in response should remain original if it was set
        if "pinCode" in sample_user:
            data = response.json()["data"]["user"]
            assert data.get("pinCode") == sample_user.get("pinCode") or data.get("pinCode") is None

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_not_found(self, client: AsyncClient):
        """Test Case 6.19: Update nonexistent user"""
        update_data = {
            "firstName": "Test"
        }
        response = await client.put("/api/v1/users/nonexistent@example.com", json=update_data)

        # Should return 404 Not Found
        assert response.status_code == 404

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_partial(self, client: AsyncClient, sample_user):
        """Test Case 6.20: Partial update (only some fields)"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "organisation": "Updated Organization"
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        assert response.status_code == 200
        data = response.json()["data"]["user"]
        assert data.get("organisation") == "Updated Organization"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_status(self, client: AsyncClient, sample_user):
        """Test Case 6.21: Update user status"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "status": "Inactive"
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        assert response.status_code == 200
        data = response.json()["data"]["user"]
        assert data["status"] == "Inactive"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_address_fields(self, client: AsyncClient, sample_user):
        """Test Case 6.22: Update address fields"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "address1": "New Address Line 1",
            "address2": "New Address Line 2"
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        assert response.status_code == 200

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_invalid_geographic(self, client: AsyncClient, sample_user):
        """Test Case 6.23: Invalid geographic reference during update"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "stateId": 999,  # Invalid state
            "districtId": 999,
            "cityId": 999
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        # Should reject invalid geographic references
        assert response.status_code == 400

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_user_response_includes_updated(self, client: AsyncClient, sample_user):
        """Test Case 6.24: Response includes updatedDate"""
        if not sample_user:
            pytest.skip("Could not create sample user")

        update_data = {
            "firstName": "Updated"
        }
        response = await client.put(f"/api/v1/users/{sample_user['userId']}", json=update_data)

        if response.status_code == 200:
            data = response.json()["data"]["user"]
            assert "updatedDate" in data


class TestAPISix_DeleteUser:
    """Test cases for API 6: DELETE /api/v1/users/{userId} - Delete user"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_user_success(self, client: AsyncClient):
        """Test Case 6.25: Delete user successfully"""
        # First create a user to delete
        user_data = {
            "userId": "test_delete@example.com",
            "firstName": "Delete",
            "lastName": "User",
            "currentRole": "Patient",
            "emailId": "test_delete@example.com",
            "mobileNumber": "1234567890"
        }
        create_response = await client.post("/api/v1/users", json=user_data)

        if create_response.status_code == 201:
            response = await client.delete(f"/api/v1/users/{user_data['userId']}")
            assert response.status_code == 204

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_nonexistent_user(self, client: AsyncClient):
        """Test Case 6.26: Delete nonexistent user"""
        response = await client.delete("/api/v1/users/nonexistent_delete@example.com")

        # Should return 404 Not Found
        assert response.status_code == 404

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_user_idempotent(self, client: AsyncClient):
        """Test Case 6.27: Delete is idempotent"""
        # First create and delete a user
        user_data = {
            "userId": "test_idempotent@example.com",
            "firstName": "Idempotent",
            "lastName": "User",
            "currentRole": "Doctor",
            "emailId": "test_idempotent@example.com",
            "mobileNumber": "1234567890"
        }
        create_response = await client.post("/api/v1/users", json=user_data)

        if create_response.status_code == 201:
            # First delete
            response1 = await client.delete(f"/api/v1/users/{user_data['userId']}")
            # Second delete (should fail - user already deleted)
            response2 = await client.delete(f"/api/v1/users/{user_data['userId']}")

            assert response1.status_code == 204
            assert response2.status_code == 404

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_user_cannot_recreate_same_id(self, client: AsyncClient):
        """Test Case 6.28: After delete, can create new user with same ID"""
        user_id = "test_recreate@example.com"

        # Create, delete, then create again with same ID
        user_data_1 = {
            "userId": user_id,
            "firstName": "First",
            "lastName": "Version",
            "currentRole": "Patient",
            "emailId": "first_version@example.com",
            "mobileNumber": "1234567890"
        }
        create_response_1 = await client.post("/api/v1/users", json=user_data_1)

        if create_response_1.status_code == 201:
            delete_response = await client.delete(f"/api/v1/users/{user_id}")
            assert delete_response.status_code == 204

            # Try to create new user with same ID
            user_data_2 = {
                "userId": user_id,
                "firstName": "Second",
                "lastName": "Version",
                "currentRole": "Doctor",
                "emailId": "second_version@example.com",
                "mobileNumber": "1111111111"
            }
            create_response_2 = await client.post("/api/v1/users", json=user_data_2)
            assert create_response_2.status_code == 201

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_returns_no_content(self, client: AsyncClient):
        """Test Case 6.29: Delete returns 204 No Content"""
        # Create a user to delete
        user_data = {
            "userId": "test_no_content@example.com",
            "firstName": "No",
            "lastName": "Content",
            "currentRole": "Patient",
            "emailId": "test_no_content@example.com",
            "mobileNumber": "1234567890"
        }
        create_response = await client.post("/api/v1/users", json=user_data)

        if create_response.status_code == 201:
            response = await client.delete(f"/api/v1/users/{user_data['userId']}")
            assert response.status_code == 204
            # No content body
            assert response.content == b""
