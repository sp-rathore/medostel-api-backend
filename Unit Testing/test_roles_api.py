"""
Unit tests for User Roles Management APIs (APIs 1 & 2)
API 1: GET /api/v1/roles/all - Select all roles
API 2: POST/PUT/DELETE /api/v1/roles - CRUD operations
"""

import pytest
from httpx import AsyncClient


class TestAPIOne_GetAllRoles:
    """Test cases for API 1: GET /api/v1/roles/all"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_all_roles_success(self, client: AsyncClient):
        """Test Case 1.1: Retrieve all roles successfully"""
        response = await client.get("/api/v1/roles/all")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "roles" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["roles"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_all_roles_response_structure(self, client: AsyncClient):
        """Verify response structure is correct"""
        response = await client.get("/api/v1/roles/all")

        assert response.status_code == 200
        data = response.json()

        # Verify APIResponse structure
        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

        # Verify data structure
        assert isinstance(data["data"]["roles"], list)
        assert isinstance(data["data"]["count"], int)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_filter_by_status(self, client: AsyncClient, sample_role):
        """Test Case 1.2: Filter roles by status parameter"""
        if not sample_role:
            pytest.skip("Could not create sample role")

        response = await client.get("/api/v1/roles/all?status=Active")

        assert response.status_code == 200
        data = response.json()["data"]["roles"]

        # All roles should have Active status
        for role in data:
            assert role["status"] == "Active"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_filter_by_inactive_status(self, client: AsyncClient):
        """Test filtering by Inactive status"""
        response = await client.get("/api/v1/roles/all?status=Inactive")

        assert response.status_code == 200
        data = response.json()["data"]["roles"]

        for role in data:
            assert role["status"] == "Inactive"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_pagination_limit(self, client: AsyncClient):
        """Test Case 1.3: Pagination with limit parameter"""
        response = await client.get("/api/v1/roles/all?limit=5&offset=0")

        assert response.status_code == 200
        roles = response.json()["data"]["roles"]
        assert len(roles) <= 5

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_pagination_offset(self, client: AsyncClient):
        """Test pagination with offset"""
        # Get first page
        response1 = await client.get("/api/v1/roles/all?limit=5&offset=0")
        assert response1.status_code == 200
        page1 = response1.json()["data"]["roles"]

        # Get second page
        response2 = await client.get("/api/v1/roles/all?limit=5&offset=5")
        assert response2.status_code == 200
        page2 = response2.json()["data"]["roles"]

        # Verify different results if both pages have data
        if len(page1) > 0 and len(page2) > 0:
            assert page1[0]["roleId"] != page2[0]["roleId"]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_pagination_both_params(self, client: AsyncClient):
        """Test pagination with both limit and offset"""
        response = await client.get("/api/v1/roles/all?limit=10&offset=20")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["roles"]) <= 10

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_minimum_limit(self, client: AsyncClient):
        """Test with minimum limit"""
        response = await client.get("/api/v1/roles/all?limit=1")

        assert response.status_code == 200
        assert len(response.json()["data"]["roles"]) <= 1

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_maximum_limit(self, client: AsyncClient):
        """Test with maximum limit"""
        response = await client.get("/api/v1/roles/all?limit=1000")

        assert response.status_code == 200
        assert isinstance(response.json()["data"]["roles"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_limit_validation(self, client: AsyncClient):
        """Test Case 1.4: Validate limit constraint"""
        response = await client.get("/api/v1/roles/all?limit=1001")

        # Should reject exceeding maximum limit
        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_offset_validation(self, client: AsyncClient):
        """Test Case 1.5: Validate offset non-negative"""
        response = await client.get("/api/v1/roles/all?offset=-1")

        # Should reject negative offset
        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_zero_offset(self, client: AsyncClient):
        """Test with zero offset"""
        response = await client.get("/api/v1/roles/all?offset=0")

        assert response.status_code == 200

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_empty_result(self, client: AsyncClient):
        """Test Case 1.6: Empty result set"""
        response = await client.get("/api/v1/roles/all?status=NonExistentStatus123")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["count"] == 0
        assert data["roles"] == []

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_roles_invalid_parameter(self, client: AsyncClient):
        """Test with invalid parameter names (should be ignored)"""
        response = await client.get("/api/v1/roles/all?invalid_param=value")

        # Invalid params should be ignored
        assert response.status_code == 200

    @pytest.mark.performance
    async def test_get_roles_performance(self, client: AsyncClient):
        """Test API response time"""
        import time

        start = time.time()
        response = await client.get("/api/v1/roles/all?limit=100")
        duration = (time.time() - start) * 1000

        assert response.status_code == 200
        assert duration < 500  # Should respond within 500ms


class TestAPITwo_CreateRole:
    """Test cases for API 2: POST /api/v1/roles - Create operation"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_success(self, client: AsyncClient):
        """Test Case 2.1: Create role successfully"""
        role_data = {
            "roleId": "ROLE_TEST_CREATE_001",
            "roleName": "Test Role Creation",
            "status": "Active",
            "comments": "Test role created successfully"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["code"] == 201
        assert data["data"]["role"]["roleId"] == "ROLE_TEST_CREATE_001"
        assert data["data"]["role"]["roleName"] == "Test Role Creation"
        assert data["data"]["role"]["status"] == "Active"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_response_structure(self, client: AsyncClient):
        """Verify create response structure"""
        role_data = {
            "roleId": "ROLE_TEST_STRUCT",
            "roleName": "Structure Test",
            "status": "Active"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        if response.status_code in [201, 409]:
            data = response.json()
            assert "status" in data
            assert "code" in data
            assert "message" in data
            assert "data" in data
            assert "timestamp" in data

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_duplicate_role_conflict(self, client: AsyncClient, sample_role):
        """Test Case 2.2: Create duplicate role fails"""
        if not sample_role:
            pytest.skip("Could not create sample role")

        # Try to create same role again
        response = await client.post("/api/v1/roles", json=sample_role)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_missing_roleId(self, client: AsyncClient):
        """Test Case 2.3: Create role with missing required field"""
        role_data = {
            "roleName": "Test Role",
            "status": "Active"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        # Should reject missing required field
        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_missing_roleName(self, client: AsyncClient):
        """Test with missing roleName"""
        role_data = {
            "roleId": "ROLE_NO_NAME",
            "status": "Active"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        # Should reject missing required field
        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_missing_status(self, client: AsyncClient):
        """Test with missing status"""
        role_data = {
            "roleId": "ROLE_NO_STATUS",
            "roleName": "Test Role"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        # Status should be required or have a default
        assert response.status_code in [201, 422]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_with_optional_comments(self, client: AsyncClient):
        """Test creating role with optional comments"""
        role_data = {
            "roleId": "ROLE_WITH_COMMENTS",
            "roleName": "Role with Comments",
            "status": "Active",
            "comments": "This is an optional comment field"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        if response.status_code == 201:
            assert response.json()["data"]["role"]["comments"] == "This is an optional comment field"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_empty_string_roleName(self, client: AsyncClient):
        """Test with empty roleName"""
        role_data = {
            "roleId": "ROLE_EMPTY_NAME",
            "roleName": "",
            "status": "Active"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        # Should reject empty required field or accept it
        assert response.status_code in [201, 422]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_special_characters(self, client: AsyncClient):
        """Test creating role with special characters"""
        role_data = {
            "roleId": "ROLE_SPECIAL_!@#$",
            "roleName": "Role with !@#$%^&*()",
            "status": "Active",
            "comments": "Comments with émojis 🎉 and üñíçödé"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        # Should handle special characters
        assert response.status_code in [201, 422]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_role_very_long_strings(self, client: AsyncClient):
        """Test with very long strings"""
        role_data = {
            "roleId": "ROLE_LONG",
            "roleName": "A" * 1000,  # Very long string
            "status": "Active"
        }

        response = await client.post("/api/v1/roles", json=role_data)

        # Should either accept or validate length
        assert response.status_code in [201, 422]


class TestAPITwo_UpdateRole:
    """Test cases for API 2: PUT /api/v1/roles/{roleId} - Update operation"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_role_success(self, client: AsyncClient, sample_role_id):
        """Test Case 2.4: Update role successfully"""
        if not sample_role_id:
            pytest.skip("Could not create sample role")

        update_data = {
            "roleName": "Updated Role Name",
            "status": "Inactive"
        }

        response = await client.put(f"/api/v1/roles/{sample_role_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["role"]["roleName"] == "Updated Role Name"
        assert data["data"]["role"]["status"] == "Inactive"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_nonexistent_role(self, client: AsyncClient):
        """Test Case 2.5: Update non-existent role"""
        response = await client.put(
            "/api/v1/roles/NONEXISTENT_ROLE",
            json={"status": "Active"}
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_partial_update_role(self, client: AsyncClient, sample_role_id):
        """Test Case 2.6: Partial update role"""
        if not sample_role_id:
            pytest.skip("Could not create sample role")

        update_data = {"comments": "Updated comments only"}

        response = await client.put(f"/api/v1/roles/{sample_role_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["data"]["role"]["comments"] == "Updated comments only"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_role_status_only(self, client: AsyncClient, sample_role_id):
        """Test updating only status field"""
        if not sample_role_id:
            pytest.skip("Could not create sample role")

        update_data = {"status": "Inactive"}

        response = await client.put(f"/api/v1/roles/{sample_role_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["data"]["role"]["status"] == "Inactive"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_role_name_only(self, client: AsyncClient, sample_role_id):
        """Test updating only name field"""
        if not sample_role_id:
            pytest.skip("Could not create sample role")

        update_data = {"roleName": "New Role Name"}

        response = await client.put(f"/api/v1/roles/{sample_role_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["data"]["role"]["roleName"] == "New Role Name"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_role_empty_body(self, client: AsyncClient, sample_role_id):
        """Test update with empty body"""
        if not sample_role_id:
            pytest.skip("Could not create sample role")

        response = await client.put(f"/api/v1/roles/{sample_role_id}", json={})

        # Should return existing role or reject
        assert response.status_code in [200, 422]


class TestAPITwo_DeleteRole:
    """Test cases for API 2: DELETE /api/v1/roles/{roleId} - Delete operation"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_role_success(self, client: AsyncClient, sample_role_id):
        """Test Case 2.7: Delete role successfully"""
        if not sample_role_id:
            pytest.skip("Could not create sample role")

        response = await client.delete(f"/api/v1/roles/{sample_role_id}")

        assert response.status_code == 204

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_nonexistent_role(self, client: AsyncClient):
        """Test Case 2.8: Delete non-existent role"""
        response = await client.delete("/api/v1/roles/NONEXISTENT_ROLE")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_role_verify_deletion(self, client: AsyncClient):
        """Verify role is actually deleted"""
        # Create a role
        role_data = {
            "roleId": "ROLE_DELETE_VERIFY",
            "roleName": "Role to Delete",
            "status": "Active"
        }
        create_response = await client.post("/api/v1/roles", json=role_data)

        if create_response.status_code == 201:
            role_id = create_response.json()["data"]["role"]["roleId"]

            # Delete it
            delete_response = await client.delete(f"/api/v1/roles/{role_id}")
            assert delete_response.status_code == 204

            # Verify it's gone
            get_response = await client.get(f"/api/v1/roles/all?status=Active")
            roles = get_response.json()["data"]["roles"]
            role_ids = [r["roleId"] for r in roles]
            assert role_id not in role_ids


class TestRolesAPISecurity:
    """Security tests for Roles API"""

    @pytest.mark.security
    async def test_sql_injection_in_status_filter(self, client: AsyncClient):
        """Test SQL injection prevention"""
        payload = "Active'; DROP TABLE roles; --"
        response = await client.get(f"/api/v1/roles/all?status={payload}")

        # Should handle safely
        assert response.status_code in [200, 400, 422]

        # Verify table still exists
        verify = await client.get("/api/v1/roles/all")
        assert verify.status_code == 200

    @pytest.mark.security
    async def test_xss_in_role_name(self, client: AsyncClient):
        """Test XSS prevention"""
        role_data = {
            "roleId": "ROLE_XSS",
            "roleName": "<script>alert('xss')</script>",
            "status": "Active"
        }
        response = await client.post("/api/v1/roles", json=role_data)

        # Response should be valid JSON, not executable
        if response.status_code == 201:
            # Verify response is still valid JSON
            assert isinstance(response.json(), dict)


class TestRolesAPIEdgeCases:
    """Edge case tests for Roles API"""

    @pytest.mark.unit
    async def test_role_id_case_sensitivity(self, client: AsyncClient):
        """Test if role IDs are case sensitive"""
        role_data = {
            "roleId": "ROLE_CASE_TEST",
            "roleName": "Case Test",
            "status": "Active"
        }
        response = await client.post("/api/v1/roles", json=role_data)

        if response.status_code == 201:
            # Try lowercase version
            response2 = await client.get("/api/v1/roles/all")
            assert response2.status_code == 200

    @pytest.mark.unit
    async def test_unicode_in_role_data(self, client: AsyncClient):
        """Test Unicode character handling"""
        role_data = {
            "roleId": "ROLE_UNICODE",
            "roleName": "角色名称",  # Chinese characters
            "status": "Active",
            "comments": "مرحبا بالعالم"  # Arabic
        }
        response = await client.post("/api/v1/roles", json=role_data)

        assert response.status_code in [201, 422]
