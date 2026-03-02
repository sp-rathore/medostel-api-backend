"""
API routes for State_City_PinCode_Master table (APIs 1-5)
API 1: SELECT - Get all locations with district filtering
API 2: CRUD - Create and Update locations with district hierarchy
API 3: SELECT - Get pinCodes by city
API 4: SELECT - Get districts by state
API 5: SELECT - Get cities/pincodes by district
Updated: March 2, 2026 - Changed to numeric data types, pinCode as PK
Updated: March 3, 2026 - Added district hierarchy and new endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.location_service import LocationService
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/locations", tags=["Locations"])


# API 1: SELECT - Get all locations
@router.get("/all", response_model=APIResponse)
async def get_all_locations(
    db=Depends(get_db),
    country: str = Query(None, description="Filter by country name"),
    state_id: int = Query(None, description="Filter by state ID (numeric, 0001-0035)"),
    district_id: int = Query(None, description="Filter by district ID (numeric, 0001-N per state)"),
    status: str = Query(None, description="Filter by status (Active/Inactive)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of results to return (max 1000)"),
    offset: int = Query(0, ge=0, description="Number of results to skip for pagination")
):
    """
    API 1: SELECT Operation - Retrieve all geographic locations with hierarchical filtering

    **Query Parameters (all optional):**
    - country: Filter by country name (e.g., "India")
    - state_id: Filter by state ID (numeric, 0001-0035)
    - district_id: Filter by district ID (numeric, 0001-N per state)
    - status: Filter by status ("Active" or "Inactive")
    - limit: Number of results to return (default 100, max 1000)
    - offset: Skip N results for pagination (default 0)

    **Response:** List of locations with geographic hierarchy (state, district, city) and count

    **Examples:**
    - GET /api/v1/locations/all?state_id=1 - Get all locations in state 1 (Maharashtra)
    - GET /api/v1/locations/all?district_id=5 - Get all locations in district 5
    - GET /api/v1/locations/all?state_id=1&district_id=1 - Get locations in state 1, district 1
    """
    try:
        locations = await LocationService.get_all_locations(
            db, country, state_id, district_id, status, limit, offset
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Geographic locations retrieved successfully",
            data={"locations": locations, "count": len(locations)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 2: CRUD - Create location
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_location(
    location: LocationCreate,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Create new geographic location with district hierarchy

    **Request Body (all required):**
    - stateId: State identifier (numeric, 0001-0035)
    - stateName: State/UT name (e.g., "Maharashtra")
    - districtId: District identifier (numeric, 0001-N per state)
    - districtName: District name (e.g., "Mumbai")
    - cityId: City identifier (numeric, 0001-N per district)
    - cityName: City name - proper city name, not post office name (e.g., "Mumbai")
    - pinCode: Postal code (5-6 digits for India, PRIMARY KEY, e.g., 400001)
    - countryName: Country name (optional, default: "India")
    - status: Status (optional, default: "Active", options: "Active"/"Inactive")

    **Response:** Created location object with HTTP 201 status

    **Example Request:**
    ```json
    {
      "stateId": 1,
      "stateName": "Maharashtra",
      "districtId": 1,
      "districtName": "Mumbai",
      "cityId": 1,
      "cityName": "Mumbai",
      "pinCode": 400001,
      "countryName": "India",
      "status": "Active"
    }
    ```
    """
    try:
        new_location = await LocationService.create_location(db, location.dict())

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Location created successfully",
            data={"location": new_location},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 2: CRUD - Update location
@router.put("/{pin_code}", response_model=APIResponse)
async def update_location(
    pin_code: int,
    location: LocationUpdate,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Update geographic location by pinCode

    **Path Parameters:**
    - pin_code: Postal code (primary key, 5-6 digits for India, e.g., 400001)

    **Request Body (all optional):**
    - status: Updated status ("Active" or "Inactive")
    - countryName: Updated country name

    **Immutable Fields (cannot be updated):**
    - pinCode: Primary key, uniquely identifies the location
    - stateId: Geographic hierarchy (use new pinCode for different state)
    - stateName: Geographic hierarchy
    - districtId: Geographic hierarchy
    - districtName: Geographic hierarchy
    - cityId: Geographic hierarchy
    - cityName: Geographic hierarchy

    **Note:** To move a location to a different state/district/city, create a new record with the new pinCode.

    **Response:** Updated location object with HTTP 200

    **Example Request:**
    ```json
    {
      "status": "Active",
      "countryName": "India"
    }
    ```
    """
    try:
        # Check if location exists
        existing = await LocationService.get_location_by_pincode(db, pin_code)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Location with pinCode {pin_code} not found"
            )

        updated_location = await LocationService.update_location(
            db, pin_code, location.dict(exclude_unset=True)
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Location updated successfully",
            data={"location": updated_location},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 3: SELECT - Get pinCodes by city
@router.get("/pincodes", response_model=APIResponse)
async def get_pincodes_by_city(
    db=Depends(get_db),
    city_id: int = Query(None, description="Filter by city ID (numeric, 0001-N per district)"),
    city_name: str = Query(None, description="Filter by city name (e.g., 'Mumbai')")
):
    """
    API 3: SELECT Operation - Retrieve pinCodes for a specific city

    **Query Parameters (provide at least one):**
    - city_id: City identifier (numeric, 0001-N per district)
    - city_name: City name (string)

    **Response:** List of distinct pinCodes for the specified city with count

    **Examples:**
    - GET /api/v1/locations/pincodes?city_id=1 - Get all pincodes in city 1
    - GET /api/v1/locations/pincodes?city_name=Mumbai - Get all pincodes in Mumbai
    - GET /api/v1/locations/pincodes?city_id=1&city_name=Mumbai - Both parameters
    """
    try:
        if not city_id and not city_name:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="At least one of city_id or city_name must be provided"
            )

        pincodes = await LocationService.get_pincodes_by_city(
            db, city_id, city_name
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="PinCodes retrieved successfully for the city",
            data={"pincodes": pincodes, "count": len(pincodes)},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 4: SELECT - Get all districts in a state
@router.get("/districts/{state_id}", response_model=APIResponse)
async def get_districts_by_state(
    state_id: int,
    db=Depends(get_db)
):
    """
    API 4: SELECT Operation - Retrieve all districts in a specific state

    **Path Parameters:**
    - state_id: State identifier (numeric, 0001-0035)

    **Response:** List of all districts in the specified state with names

    **Examples:**
    - GET /api/v1/locations/districts/1 - Get all districts in state 1 (Maharashtra)
    - GET /api/v1/locations/districts/27 - Get all districts in state 27
    """
    try:
        districts = await LocationService.get_districts_by_state(db, state_id)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"Districts retrieved successfully for state {state_id}",
            data={"districts": districts, "count": len(districts)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 5: SELECT - Get cities and pincodes by district
@router.get("/cities/{district_id}", response_model=APIResponse)
async def get_cities_by_district(
    district_id: int,
    db=Depends(get_db)
):
    """
    API 5: SELECT Operation - Retrieve all cities in a specific district

    **Path Parameters:**
    - district_id: District identifier (numeric, 0001-N per state)

    **Response:** List of all cities in the specified district with names and state/district info

    **Examples:**
    - GET /api/v1/locations/cities/1 - Get all cities in district 1
    - GET /api/v1/locations/cities/10 - Get all cities in district 10
    """
    try:
        cities = await LocationService.get_cities_by_district(db, district_id)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"Cities retrieved successfully for district {district_id}",
            data={"cities": cities, "count": len(cities)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 5 Alternative: GET - Get all pincodes by district
@router.get("/by-district/{district_id}", response_model=APIResponse)
async def get_pincodes_by_district(
    district_id: int,
    db=Depends(get_db)
):
    """
    API 5 Alternative: SELECT Operation - Retrieve all pinCodes in a specific district

    **Path Parameters:**
    - district_id: District identifier (numeric, 0001-N per state)

    **Response:** List of all pinCodes in the specified district organized by city

    **Examples:**
    - GET /api/v1/locations/by-district/1 - Get all pincodes in district 1
    - GET /api/v1/locations/by-district/5 - Get all pincodes in district 5
    """
    try:
        pincodes = await LocationService.get_pincodes_by_district(db, district_id)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"PinCodes retrieved successfully for district {district_id}",
            data={"pincodes": pincodes, "count": len(pincodes)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
