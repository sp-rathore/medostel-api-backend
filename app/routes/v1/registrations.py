"""
API routes for New_User_Request table (APIs 9 & 10)
SELECT operations (API 9) and CRUD operations (API 10)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.registration_service import RegistrationService
from app.schemas.registration import RegistrationCreate, RegistrationUpdate
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/requests", tags=["User Registrations"])


# API 9: SELECT - Get all registration requests
@router.get("/all", response_model=APIResponse)
async def get_all_registration_requests(
    db=Depends(get_db),
    request_status: str = Query(None),
    current_role: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    API 9: SELECT Operation - Retrieve all registration requests
    - Returns all registration requests with optional filtering
    - Supports pagination with limit and offset
    """
    try:
        requests = await RegistrationService.get_all_requests(
            db, request_status, current_role, limit, offset
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Registration requests retrieved successfully",
            data={"requests": requests, "count": len(requests)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 10: CRUD - Create registration request
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_registration_request(
    request_data: RegistrationCreate,
    db=Depends(get_db)
):
    """
    API 10: CRUD Operation - Create new registration request
    - Creates a new user registration request
    - Returns the created request
    """
    try:
        # Check if request already exists
        existing = await RegistrationService.get_request_by_id(db, request_data.requestId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Registration request {request_data.requestId} already exists"
            )

        new_request = await RegistrationService.create_request(db, request_data.dict())

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Registration request created successfully",
            data={"request": new_request},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 10: CRUD - Update registration request
@router.put("/{requestId}", response_model=APIResponse)
async def update_registration_request(
    requestId: str,
    request_data: RegistrationUpdate,
    db=Depends(get_db)
):
    """
    API 10: CRUD Operation - Update registration request
    - Updates a registration request (approve/reject)
    - Returns the updated request
    """
    try:
        # Check if request exists
        existing = await RegistrationService.get_request_by_id(db, requestId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Registration request {requestId} not found"
            )

        updated_request = await RegistrationService.update_request(
            db, requestId, request_data.dict(exclude_unset=True)
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Registration request updated successfully",
            data={"request": updated_request},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 10: CRUD - Delete registration request
@router.delete("/{requestId}", response_model=APIResponse, status_code=HTTPStatus.NO_CONTENT)
async def delete_registration_request(
    requestId: str,
    db=Depends(get_db)
):
    """
    API 10: CRUD Operation - Delete registration request
    - Deletes a registration request
    - Returns 204 No Content on success
    """
    try:
        # Check if request exists
        existing = await RegistrationService.get_request_by_id(db, requestId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Registration request {requestId} not found"
            )

        success = await RegistrationService.delete_request(db, requestId)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete registration request"
            )

        return APIResponse(
            status="success",
            code=HTTPStatus.NO_CONTENT,
            message="Registration request deleted successfully",
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
