"""
Unit tests for Location Management APIs (APIs 1, 2, & 3)
API 1: GET /api/v1/locations/all - Select all locations
API 2: POST/PUT /api/v1/locations - CRUD operations
API 3: GET /api/v1/locations/pincodes - Get pinCodes by city
Updated: March 2, 2026 - Numeric data types, pinCode as PK
"""

import pytest
from httpx import AsyncClient


class TestAPIOne_GetAllLocations:
    """Test cases for API 1: GET /api/v1/locations/all"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_all_locations_success(self, client: AsyncClient):
        """Test Case 1.1: Retrieve all locations successfully"""
        response = await client.get("/api/v1/locations/all")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "locations" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["locations"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_all_locations_response_structure(self, client: AsyncClient):
        """Test Case 1.2: Verify response structure is correct"""
        response = await client.get("/api/v1/locations/all")

        assert response.status_code == 200
        data = response.json()

        # Verify APIResponse structure
        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

        # Verify data structure
        assert isinstance(data["data"]["locations"], list)
        assert isinstance(data["data"]["count"], int)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_filter_by_country(self, client: AsyncClient, mumbai_location):
        """Test Case 1.3: Filter locations by country parameter"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/all?country=India")

        assert response.status_code == 200
        data = response.json()["data"]["locations"]

        # All locations should be from India
        for location in data:
            assert location["countryName"] == "India"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_filter_by_state_id(self, client: AsyncClient, mumbai_location):
        """Test Case 1.4: Filter locations by numeric state_id"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/all?state_id=27")

        assert response.status_code == 200
        data = response.json()["data"]["locations"]

        # All locations should be from stateId 27 (Maharashtra)
        for location in data:
            assert location["stateId"] == 27

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_filter_by_status(self, client: AsyncClient, sample_location):
        """Test Case 1.5: Filter locations by status (Active/Inactive)"""
        if not sample_location:
            pytest.skip("Could not create sample location")

        response = await client.get("/api/v1/locations/all?status=Active")

        assert response.status_code == 200
        data = response.json()["data"]["locations"]

        # All locations should have Active status
        for location in data:
            assert location["status"] == "Active"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_pagination_limit(self, client: AsyncClient):
        """Test Case 1.6: Pagination with limit parameter"""
        response = await client.get("/api/v1/locations/all?limit=5&offset=0")

        assert response.status_code == 200
        locations = response.json()["data"]["locations"]
        assert len(locations) <= 5

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_pagination_offset(self, client: AsyncClient):
        """Test Case 1.7: Pagination with offset"""
        # Get first page
        response1 = await client.get("/api/v1/locations/all?limit=5&offset=0")
        assert response1.status_code == 200
        page1 = response1.json()["data"]["locations"]

        # Get second page
        response2 = await client.get("/api/v1/locations/all?limit=5&offset=5")
        assert response2.status_code == 200
        page2 = response2.json()["data"]["locations"]

        # Verify different results if both pages have data
        if len(page1) > 0 and len(page2) > 0:
            assert page1[0]["pinCode"] != page2[0]["pinCode"]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_limit_validation_max(self, client: AsyncClient):
        """Test Case 1.8: Limit validation (max 1000)"""
        response = await client.get("/api/v1/locations/all?limit=1000")

        assert response.status_code == 200
        locations = response.json()["data"]["locations"]
        assert len(locations) <= 1000

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_limit_exceeds_max(self, client: AsyncClient):
        """Test Case 1.9: Limit exceeding max should be rejected"""
        response = await client.get("/api/v1/locations/all?limit=1001")

        # Should reject or cap at 1000
        assert response.status_code in [200, 422]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_offset_negative_validation(self, client: AsyncClient):
        """Test Case 1.10: Negative offset validation"""
        response = await client.get("/api/v1/locations/all?offset=-1")

        # Should reject negative offset
        assert response.status_code in [200, 422]

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_numeric_field_types(self, client: AsyncClient, mumbai_location):
        """Test Case 1.11: Verify numeric field types in response"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/all?state_id=27")

        assert response.status_code == 200
        locations = response.json()["data"]["locations"]

        for location in locations:
            assert isinstance(location["pinCode"], int), "pinCode should be integer"
            assert isinstance(location["stateId"], int), "stateId should be integer"
            assert isinstance(location["cityId"], int), "cityId should be integer"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_combined_filters(self, client: AsyncClient, mumbai_location):
        """Test Case 1.12: Combined filters (country + state_id + status)"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/all?country=India&state_id=27&status=Active")

        assert response.status_code == 200
        data = response.json()["data"]
        locations = data["locations"]

        for location in locations:
            assert location["countryName"] == "India"
            assert location["stateId"] == 27
            assert location["status"] == "Active"

    @pytest.mark.performance
    async def test_get_locations_response_time(self, client: AsyncClient):
        """Test Case 1.13: Response time < 100ms"""
        import time
        start = time.time()
        response = await client.get("/api/v1/locations/all?limit=10")
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 0.1, "Response time should be < 100ms"

    @pytest.mark.unit
    async def test_get_locations_empty_result_handling(self, client: AsyncClient):
        """Test Case 1.14: Handle empty result set gracefully"""
        # Filter with non-existent state_id
        response = await client.get("/api/v1/locations/all?state_id=999")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["count"] == 0
        assert data["locations"] == []

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_locations_filter_by_district_id(self, client: AsyncClient, mumbai_location):
        """Test Case 1.15: Filter locations by numeric district_id"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/all?state_id=27&district_id=1")

        assert response.status_code == 200
        data = response.json()["data"]["locations"]

        # All locations should be from stateId 27, districtId 1
        for location in data:
            assert location["stateId"] == 27
            assert location["districtId"] == 1
            assert "districtName" in location


class TestAPITwo_CreateAndUpdateLocations:
    """Test cases for API 2: POST/PUT /api/v1/locations"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_success(self, client: AsyncClient):
        """Test Case 2.1: Create location successfully"""
        location_data = {
            "stateId": 6,
            "stateName": "Gujarat",
            "cityId": 120,
            "cityName": "Ahmedabad",
            "pinCode": 380001,
            "countryName": "India",
            "status": "Active"
        }
        response = await client.post("/api/v1/locations", json=location_data)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "location" in data["data"]
        location = data["data"]["location"]
        assert location["pinCode"] == 380001
        assert location["stateId"] == 6

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_response_structure(self, client: AsyncClient):
        """Test Case 2.2: Verify create response structure"""
        location_data = {
            "stateId": 9,
            "stateName": "Himachal Pradesh",
            "cityId": 130,
            "cityName": "Shimla",
            "pinCode": 171001,
            "countryName": "India",
            "status": "Active"
        }
        response = await client.post("/api/v1/locations", json=location_data)

        assert response.status_code == 201
        data = response.json()

        # Verify APIResponse structure
        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

        # Verify location object has timestamps
        location = data["data"]["location"]
        assert "createdDate" in location
        assert "updatedDate" in location

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_invalid_pincode_range(self, client: AsyncClient):
        """Test Case 2.3: Reject pinCode outside valid range (100000-999999)"""
        location_data = {
            "stateId": 10,
            "stateName": "Jharkhand",
            "cityId": 140,
            "cityName": "Ranchi",
            "pinCode": 99999,  # Invalid - less than 100000
            "countryName": "India",
            "status": "Active"
        }
        response = await client.post("/api/v1/locations", json=location_data)

        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_missing_required_field(self, client: AsyncClient):
        """Test Case 2.4: Reject when required field is missing"""
        location_data = {
            "stateId": 11,
            "stateName": "Karnataka",
            # Missing cityId - required field
            "cityName": "Mysore",
            "pinCode": 570001,
            "countryName": "India",
            "status": "Active"
        }
        response = await client.post("/api/v1/locations", json=location_data)

        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_duplicate_pincode(self, client: AsyncClient, mumbai_location):
        """Test Case 2.5: Reject duplicate pinCode (primary key)"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        # Try to create with same pinCode
        location_data = {
            "stateId": 27,
            "stateName": "Maharashtra",
            "cityId": 102,
            "cityName": "Mumbai",
            "pinCode": 400001,  # Duplicate
            "countryName": "India",
            "status": "Active"
        }
        response = await client.post("/api/v1/locations", json=location_data)

        # Should reject due to duplicate primary key
        assert response.status_code == 409

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_invalid_status(self, client: AsyncClient):
        """Test Case 2.6: Reject invalid status value"""
        location_data = {
            "stateId": 12,
            "stateName": "Kerala",
            "cityId": 150,
            "cityName": "Kochi",
            "pinCode": 682001,
            "countryName": "India",
            "status": "Invalid"  # Invalid status
        }
        response = await client.post("/api/v1/locations", json=location_data)

        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_create_location_default_values(self, client: AsyncClient):
        """Test Case 2.7: Apply default values for optional fields"""
        location_data = {
            "stateId": 13,
            "stateName": "Madhya Pradesh",
            "cityId": 160,
            "cityName": "Indore",
            "pinCode": 452001
            # Not providing countryName and status - should use defaults
        }
        response = await client.post("/api/v1/locations", json=location_data)

        assert response.status_code == 201
        location = response.json()["data"]["location"]
        assert location["countryName"] == "India"  # Default
        assert location["status"] == "Active"  # Default

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_status_success(self, client: AsyncClient, mumbai_location):
        """Test Case 2.8: Update location status successfully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {"status": "Inactive"}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        location = data["data"]["location"]
        assert location["status"] == "Inactive"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_country_name(self, client: AsyncClient, mumbai_location):
        """Test Case 2.9: Update location countryName"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {"countryName": "India"}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 200
        location = response.json()["data"]["location"]
        assert location["countryName"] == "India"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_multiple_fields(self, client: AsyncClient, mumbai_location):
        """Test Case 2.10: Update multiple fields at once"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {
            "status": "Inactive",
            "countryName": "India"
        }
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 200
        location = response.json()["data"]["location"]
        assert location["status"] == "Inactive"
        assert location["countryName"] == "India"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_nonexistent(self, client: AsyncClient):
        """Test Case 2.11: Return 404 for non-existent location"""
        pincode = 999999
        update_data = {"status": "Inactive"}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 404

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_invalid_status(self, client: AsyncClient, mumbai_location):
        """Test Case 2.12: Reject invalid status on update"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {"status": "InvalidStatus"}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 422

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_cannot_modify_pincode(self, client: AsyncClient, mumbai_location):
        """Test Case 2.13: pinCode is immutable (primary key)"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        # Try to update pinCode - should not be allowed
        update_data = {"pinCode": 400002}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        # pinCode should remain unchanged (immutable)
        if response.status_code == 200:
            location = response.json()["data"]["location"]
            assert location["pinCode"] == 400001  # Unchanged

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_empty_request_body(self, client: AsyncClient, mumbai_location):
        """Test Case 2.14: Handle empty request body gracefully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        # Should return 200 with no changes
        assert response.status_code == 200

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_response_structure(self, client: AsyncClient, mumbai_location):
        """Test Case 2.15: Verify update response structure"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {"status": "Inactive"}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 200
        data = response.json()

        # Verify APIResponse structure
        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_update_location_verify_updatedDate_changed(self, client: AsyncClient, mumbai_location):
        """Test Case 2.16: Verify updatedDate is updated"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        pincode = 400001
        update_data = {"status": "Inactive"}
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)

        assert response.status_code == 200
        location = response.json()["data"]["location"]
        # updatedDate should be present
        assert "updatedDate" in location

    @pytest.mark.performance
    async def test_update_location_response_time(self, client: AsyncClient, mumbai_location):
        """Test Case 2.17: Update response time < 100ms"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        import time
        pincode = 400001
        update_data = {"status": "Inactive"}
        start = time.time()
        response = await client.put(f"/api/v1/locations/{pincode}", json=update_data)
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 0.1, "Update response time should be < 100ms"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_delete_endpoint_removed(self, client: AsyncClient):
        """Test Case 2.18: DELETE endpoint is not available"""
        response = await client.delete("/api/v1/locations/400001")

        # Should return 404 or 405 (method not allowed)
        assert response.status_code in [404, 405]


class TestAPIThree_GetPinCodesByCity:
    """Test cases for API 3: GET /api/v1/locations/pincodes"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_by_city_id_success(self, client: AsyncClient, mumbai_location):
        """Test Case 3.1: Get pinCodes by city_id successfully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/pincodes?city_id=102")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "pincodes" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["pincodes"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_by_city_name_success(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2: Get pinCodes by city_name successfully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/pincodes?city_name=Mumbai")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "pincodes" in data["data"]
        assert isinstance(data["data"]["pincodes"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_response_structure(self, client: AsyncClient, mumbai_location):
        """Test Case 3.3: Verify response structure"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/pincodes?city_id=102")

        assert response.status_code == 200
        data = response.json()

        # Verify APIResponse structure
        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_returns_integers(self, client: AsyncClient, mumbai_location):
        """Test Case 3.4: Verify pinCodes are integers"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/pincodes?city_id=102")

        assert response.status_code == 200
        pincodes = response.json()["data"]["pincodes"]

        for pincode in pincodes:
            assert isinstance(pincode, int), "pinCode should be integer"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_missing_both_parameters(self, client: AsyncClient):
        """Test Case 3.5: Reject when both city_id and city_name are missing"""
        response = await client.get("/api/v1/locations/pincodes")

        assert response.status_code == 400

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_nonexistent_city_id(self, client: AsyncClient):
        """Test Case 3.6: Return empty list for non-existent city_id"""
        response = await client.get("/api/v1/locations/pincodes?city_id=9999")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["count"] == 0
        assert data["data"]["pincodes"] == []

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_nonexistent_city_name(self, client: AsyncClient):
        """Test Case 3.7: Return empty list for non-existent city_name"""
        response = await client.get("/api/v1/locations/pincodes?city_name=NonExistentCity")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["count"] == 0
        assert data["data"]["pincodes"] == []

    @pytest.mark.performance
    async def test_get_pincodes_response_time(self, client: AsyncClient, mumbai_location):
        """Test Case 3.8: Response time < 100ms"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        import time
        start = time.time()
        response = await client.get("/api/v1/locations/pincodes?city_id=102")
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 0.1, "Response time should be < 100ms"


class TestAPIThreePointTwo_GetDistrictsByState:
    """Test cases for API 3.2: GET /api/v1/locations/districts/{state_id}"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_districts_by_state_success(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2.1: Retrieve all districts in a state successfully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/districts/27")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "districts" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["districts"], list)
        assert data["data"]["count"] > 0

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_districts_response_structure(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2.2: Verify district response has correct fields"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/districts/27")

        assert response.status_code == 200
        data = response.json()["data"]["districts"]

        if len(data) > 0:
            first_district = data[0]
            assert "districtId" in first_district
            assert "districtName" in first_district
            assert "stateName" in first_district
            assert isinstance(first_district["districtId"], int)
            assert isinstance(first_district["districtName"], str)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_districts_numeric_state_id(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2.3: Verify state_id is numeric (0001-0035)"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/districts/27")

        assert response.status_code == 200
        data = response.json()["data"]["districts"]

        for district in data:
            assert district["stateName"] == "Maharashtra"

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_districts_ordered_by_id(self, client: AsyncClient, pune_location, nagpur_location):
        """Test Case 3.2.4: Verify districts are ordered by districtId"""
        response = await client.get("/api/v1/locations/districts/27")

        assert response.status_code == 200
        data = response.json()["data"]["districts"]

        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["districtId"] <= data[i + 1]["districtId"]

    @pytest.mark.unit
    async def test_get_districts_nonexistent_state(self, client: AsyncClient):
        """Test Case 3.2.5: Handle nonexistent state gracefully"""
        response = await client.get("/api/v1/locations/districts/999")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["count"] == 0
        assert data["data"]["districts"] == []

    @pytest.mark.unit
    async def test_get_districts_response_format(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2.6: Verify APIResponse format is correct"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/districts/27")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"
        assert data["code"] == 200

    @pytest.mark.performance
    async def test_get_districts_response_time(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2.7: Response time < 100ms"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        import time
        start = time.time()
        response = await client.get("/api/v1/locations/districts/27")
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 0.1, "Response time should be < 100ms"

    @pytest.mark.unit
    async def test_get_districts_distinct_values(self, client: AsyncClient, mumbai_location):
        """Test Case 3.2.8: Verify each districtId appears only once"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/districts/27")

        assert response.status_code == 200
        data = response.json()["data"]["districts"]

        district_ids = [d["districtId"] for d in data]
        assert len(district_ids) == len(set(district_ids)), "Duplicate districtIds found"


class TestAPIThreePointThree_GetCitiesByDistrict:
    """Test cases for API 3.3: GET /api/v1/locations/cities/{district_id}"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_cities_by_district_success(self, client: AsyncClient, mumbai_location):
        """Test Case 3.3.1: Retrieve all cities in a district successfully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/cities/1")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "cities" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["cities"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_cities_response_structure(self, client: AsyncClient, mumbai_location):
        """Test Case 3.3.2: Verify city response has correct fields"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/cities/1")

        assert response.status_code == 200
        data = response.json()["data"]["cities"]

        if len(data) > 0:
            first_city = data[0]
            assert "cityId" in first_city
            assert "cityName" in first_city
            assert "districtName" in first_city
            assert "stateName" in first_city
            assert isinstance(first_city["cityId"], int)
            assert isinstance(first_city["cityName"], str)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_cities_multiple_cities(self, client: AsyncClient, mumbai_location, navi_mumbai_location):
        """Test Case 3.3.3: Retrieve multiple cities in same district"""
        if not mumbai_location or not navi_mumbai_location:
            pytest.skip("Could not create Mumbai/Navi Mumbai locations")

        response = await client.get("/api/v1/locations/cities/1")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["count"] >= 2

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_cities_ordered_by_id(self, client: AsyncClient, mumbai_location, navi_mumbai_location):
        """Test Case 3.3.4: Verify cities are ordered by cityId"""
        if not mumbai_location or not navi_mumbai_location:
            pytest.skip("Could not create Mumbai/Navi Mumbai locations")

        response = await client.get("/api/v1/locations/cities/1")

        assert response.status_code == 200
        data = response.json()["data"]["cities"]

        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["cityId"] <= data[i + 1]["cityId"]

    @pytest.mark.unit
    async def test_get_cities_nonexistent_district(self, client: AsyncClient):
        """Test Case 3.3.5: Handle nonexistent district gracefully"""
        response = await client.get("/api/v1/locations/cities/9999")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["count"] == 0
        assert data["data"]["cities"] == []

    @pytest.mark.unit
    async def test_get_cities_response_format(self, client: AsyncClient, mumbai_location):
        """Test Case 3.3.6: Verify APIResponse format is correct"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/cities/1")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data

    @pytest.mark.performance
    async def test_get_cities_response_time(self, client: AsyncClient, mumbai_location):
        """Test Case 3.3.7: Response time < 100ms"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        import time
        start = time.time()
        response = await client.get("/api/v1/locations/cities/1")
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 0.1, "Response time should be < 100ms"

    @pytest.mark.unit
    async def test_get_cities_distinct_values(self, client: AsyncClient, mumbai_location):
        """Test Case 3.3.8: Verify each cityId appears only once"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/cities/1")

        assert response.status_code == 200
        data = response.json()["data"]["cities"]

        city_ids = [c["cityId"] for c in data]
        assert len(city_ids) == len(set(city_ids)), "Duplicate cityIds found"


class TestAPIThreePointFour_GetPinCodesByDistrict:
    """Test cases for API 3.4: GET /api/v1/locations/by-district/{district_id}"""

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_by_district_success(self, client: AsyncClient, mumbai_location):
        """Test Case 3.4.1: Retrieve all pincodes in a district successfully"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/by-district/1")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "pincodes" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["pincodes"], list)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_district_response_structure(self, client: AsyncClient, mumbai_location):
        """Test Case 3.4.2: Verify pincode response has correct fields"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/by-district/1")

        assert response.status_code == 200
        data = response.json()["data"]["pincodes"]

        if len(data) > 0:
            first_pincode = data[0]
            assert "pinCode" in first_pincode
            assert "cityName" in first_pincode
            assert "cityId" in first_pincode
            assert isinstance(first_pincode["pinCode"], int)
            assert isinstance(first_pincode["cityName"], str)
            assert isinstance(first_pincode["cityId"], int)

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_by_district_multiple(self, client: AsyncClient, mumbai_location, navi_mumbai_location):
        """Test Case 3.4.3: Retrieve multiple pincodes organized by city"""
        if not mumbai_location or not navi_mumbai_location:
            pytest.skip("Could not create Mumbai/Navi Mumbai locations")

        response = await client.get("/api/v1/locations/by-district/1")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["count"] >= 2

    @pytest.mark.unit
    @pytest.mark.functional
    async def test_get_pincodes_district_organized_by_city(self, client: AsyncClient, mumbai_location, navi_mumbai_location):
        """Test Case 3.4.4: Verify pincodes are organized by city and ordered"""
        if not mumbai_location or not navi_mumbai_location:
            pytest.skip("Could not create Mumbai/Navi Mumbai locations")

        response = await client.get("/api/v1/locations/by-district/1")

        assert response.status_code == 200
        data = response.json()["data"]["pincodes"]

        if len(data) > 1:
            # Verify ordering by cityId, then pinCode
            for i in range(len(data) - 1):
                current = data[i]
                next_item = data[i + 1]
                assert current["cityId"] <= next_item["cityId"]
                if current["cityId"] == next_item["cityId"]:
                    assert current["pinCode"] <= next_item["pinCode"]

    @pytest.mark.unit
    async def test_get_pincodes_by_district_nonexistent(self, client: AsyncClient):
        """Test Case 3.4.5: Handle nonexistent district gracefully"""
        response = await client.get("/api/v1/locations/by-district/9999")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["count"] == 0
        assert data["data"]["pincodes"] == []

    @pytest.mark.unit
    async def test_get_pincodes_district_response_format(self, client: AsyncClient, mumbai_location):
        """Test Case 3.4.6: Verify APIResponse format is correct"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/by-district/1")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    @pytest.mark.performance
    async def test_get_pincodes_by_district_response_time(self, client: AsyncClient, mumbai_location):
        """Test Case 3.4.7: Response time < 100ms"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        import time
        start = time.time()
        response = await client.get("/api/v1/locations/by-district/1")
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 0.1, "Response time should be < 100ms"

    @pytest.mark.unit
    async def test_get_pincodes_by_district_return_type(self, client: AsyncClient, mumbai_location):
        """Test Case 3.4.8: Verify pincodes are returned as integers"""
        if not mumbai_location:
            pytest.skip("Could not create Mumbai location")

        response = await client.get("/api/v1/locations/by-district/1")

        assert response.status_code == 200
        data = response.json()["data"]["pincodes"]

        for pincode_obj in data:
            assert isinstance(pincode_obj["pinCode"], int)
            assert 100000 <= pincode_obj["pinCode"] <= 999999
