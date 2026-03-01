"""
API routes for State_City_PinCode_Master table (APIs 3 & 4)
SELECT operations (API 3) and CRUD operations (API 4)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.location_service import LocationService
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/locations", tags=["Locations"])


# API 3: SELECT - Get all locations
@router.get("/all", response_model=APIResponse)
async def get_all_locations(
    db=Depends(get_db),
    country: str = Query(None),
    state_id: str = Query(None),
    status: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    API 3: SELECT Operation - Retrieve all geographic locations
    - Returns all locations with optional filtering
    - Supports pagination with limit and offset
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


# API 4: CRUD - Create location
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_location(
    location: LocationCreate,
    db=Depends(get_db)
):
    """
    API 4: CRUD Operation - Create new geographic location
    - Creates a new location with provided data
    - Returns the created location
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


# API 4: CRUD - Update location
@router.put("/{location_id}", response_model=APIResponse)
async def update_location(
    location_id: int,
    location: LocationUpdate,
    db=Depends(get_db)
):
    """
    API 4: CRUD Operation - Update geographic location
    - Updates an existing location
    - Returns the updated location
    """
    try:
        # Check if location exists
        existing = await LocationService.get_location_by_id(db, location_id)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Location {location_id} not found"
            )

        updated_location = await LocationService.update_location(
            db, location_id, location.dict(exclude_unset=True)
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


# API 4: CRUD - Delete location
@router.delete("/{location_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_location(
    location_id: int,
    db=Depends(get_db)
):
    """
    API 4: CRUD Operation - Delete geographic location
    - Deletes a location by ID
    - Returns 204 No Content on success
    """
    try:
        # Check if location exists
        existing = await LocationService.get_location_by_id(db, location_id)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Location {location_id} not found"
            )

        success = await LocationService.delete_location(db, location_id)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete location"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
