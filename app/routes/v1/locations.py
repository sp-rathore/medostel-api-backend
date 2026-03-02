"""
API routes for State_City_PinCode_Master table (APIs 1, 2, & 3)
API 1: SELECT - Get all locations
API 2: CRUD - Create and Update locations
API 3: SELECT - Get pinCodes by city
Updated: March 2, 2026 - Changed to numeric data types, pinCode as PK
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
    state_id: int = Query(None, description="Filter by state ID (numeric)"),
    status: str = Query(None, description="Filter by status (Active/Inactive)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    API 1: SELECT Operation - Retrieve all geographic locations

    **Parameters:**
    - country: Filter by country name (optional)
    - state_id: Filter by state ID (numeric, optional)
    - status: Filter by status (Active/Inactive, optional)
    - limit: Number of results (default 100, max 1000)
    - offset: Skip N results for pagination (default 0)

    **Response:** List of locations with count
    """
    try:
        locations = await LocationService.get_all_locations(
            db, country, state_id, status, limit, offset
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
    API 2: CRUD Operation - Create new geographic location

    **Request Body:**
    - stateId: State identifier (numeric)
    - stateName: State name
    - cityId: City identifier (numeric)
    - cityName: City name
    - pinCode: Postal code (5-6 digits for India)
    - countryName: Country name (default: "India")
    - status: Status (default: "Active", options: "Active"/"Inactive")

    **Response:** Created location object with HTTP 201
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
    - pin_code: Postal code (primary key, 5-6 digits for India)

    **Request Body (all optional):**
    - status: Updated status ("Active"/"Inactive")
    - countryName: Updated country name

    **Note:** pinCode is immutable and cannot be updated. Use pinCode to identify the location.

    **Response:** Updated location object with HTTP 200
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
    city_id: int = Query(None, description="Filter by city ID (numeric)"),
    city_name: str = Query(None, description="Filter by city name")
):
    """
    API 3: SELECT Operation - Retrieve pinCodes for a specific city

    **Query Parameters (provide at least one):**
    - city_id: City identifier (numeric, optional)
    - city_name: City name (string, optional)

    **Response:** List of distinct pinCodes for the specified city

    **Example:**
    - GET /api/v1/locations/pincodes?city_id=102
    - GET /api/v1/locations/pincodes?city_name=Mumbai
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
