"""
API routes for new_user_request table
Phase 2.3: API Endpoints Development
Date: 2026-03-03

Endpoints:
1. GET /api/v1/user-request/search - Search by status (returns list of requests)
2. POST /api/v1/user-request - Create new request (auto-generates requestId, status=pending)
3. PUT /api/v1/user-request/{requestId} - Update request status

Note: No DELETE endpoint per specification
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from src.schemas.user_request import (
    UserRequestCreate, UserRequestUpdate, UserRequestResponse, UserRequestSearchResponse,
    UserRequestCreateResponse, UserRequestUpdateResponse, UserRequestListResponse
)
from src.db.user_request_utils import user_request_db
from src.database import get_db

router = APIRouter(prefix="/api/v1/user-request", tags=["User Requests"])


# ============================================================================
# GET /api/v1/user-request/search - Search by status
# ============================================================================

@router.get("/search", response_model=UserRequestListResponse)
async def search_user_requests(
    status: str = Query(..., description="Request status to filter by: pending, active, or rejected"),
    db: Session = Depends(get_db)
):
    """
    Search for user requests by status

    Returns list of requests with given status, with existsFlag indicating whether any requests found.

    **Query Parameters**:
    - `status`: Request status filter (required, must be: pending, active, or rejected)

    **Returns**:
    ```json
    {
        "data": [
            {
                "requestId": "REQ_001",
                "userId": "john@example.com",
                "firstName": "John",
                "lastName": "Doe",
                "mobileNumber": 9876543210,
                "organization": "Hospital XYZ",
                "currentRole": "DOCTOR",
                "status": "pending",
                "city_name": "Mumbai",
                "district_name": "Mumbai",
                "pincode": "400001",
                "state_name": "Maharashtra",
                "created_Date": "2026-03-03T10:30:00",
                "updated_Date": "2026-03-03T10:30:00"
            }
        ],
        "existsFlag": true
    }
    ```

    **Or if no results found**:
    ```json
    {
        "data": [],
        "existsFlag": false
    }
    ```

    **Status Codes**:
    - 200: Success (requests found or not found)
    - 400: Validation error (missing or invalid status)
    - 500: Server error
    """
    try:
        # Validate status parameter
        allowed_statuses = {'pending', 'active', 'rejected'}
        if status.lower() not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(allowed_statuses)}"
            )

        # Search for requests by status
        requests_list = user_request_db.get_by_status(db, status.lower())

        # Return response with existsFlag
        if requests_list and len(requests_list) > 0:
            return UserRequestListResponse(
                data=[UserRequestResponse.from_orm(req) for req in requests_list],
                existsFlag=True
            )
        else:
            return UserRequestListResponse(
                data=[],
                existsFlag=False
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching for user requests: {str(e)}"
        )


# ============================================================================
# POST /api/v1/user-request - Create new request
# ============================================================================

@router.post("", response_model=UserRequestCreateResponse, status_code=201)
async def create_user_request(
    request: UserRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user request

    Creates a new user request with auto-generated requestId and default status 'pending'.
    Timestamps (created_Date, updated_Date) are auto-set by the system.

    **Request Body**:
    ```json
    {
        "userId": "john@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "mobileNumber": 9876543210,
        "organization": "Hospital XYZ",
        "currentRole": "DOCTOR",
        "city_name": "Mumbai",
        "district_name": "Mumbai",
        "pincode": "400001",
        "state_name": "Maharashtra",
        "status": "pending"
    }
    ```

    **Auto-Generated Fields**:
    - `requestId`: Generated as REQ_001, REQ_002, etc. (max + 1)
    - `created_Date`: Set to CURRENT_TIMESTAMP
    - `updated_Date`: Set to CURRENT_TIMESTAMP
    - `status`: Defaults to 'pending' if not provided

    **Validation Rules**:
    - userId: Must be valid email format, unique (not in pending/active requests)
    - mobileNumber: 10 digits (1000000000-9999999999)
    - currentRole: Must exist in user_role_master (ADMIN, DOCTOR, HOSPITAL, NURSE, PARTNER, PATIENT, RECEPTION, TECHNICIAN)
    - Location fields: city_name, district_name, pincode, state_name validate against state_city_pincode_master
    - status: Must be one of: pending, active, rejected (default: pending)

    **Returns**:
    ```json
    {
        "message": "User request created successfully",
        "data": {
            "requestId": "REQ_001",
            "userId": "john@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "organization": "Hospital XYZ",
            "currentRole": "DOCTOR",
            "status": "pending",
            "city_name": "Mumbai",
            "district_name": "Mumbai",
            "pincode": "400001",
            "state_name": "Maharashtra",
            "created_Date": "2026-03-03T10:30:00",
            "updated_Date": "2026-03-03T10:30:00"
        }
    }
    ```

    **Status Codes**:
    - 201: Request created successfully
    - 400: Validation error (invalid email, mobile, role, location, etc.)
    - 409: Conflict (email already exists in pending/active request)
    - 500: Server error
    """
    try:
        # Check if email already has a pending or active request
        if user_request_db.email_exists_in_pending(db, request.userId):
            raise HTTPException(
                status_code=409,
                detail=f"Email already has a pending or active request: {request.userId}"
            )

        # Create request (will validate all references inside create function)
        request_dict = request.model_dump(exclude_unset=True)
        created_request = user_request_db.create_user_request(db, request_dict)

        return UserRequestCreateResponse(
            message="User request created successfully",
            data=UserRequestResponse.from_orm(created_request)
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user request: {str(e)}"
        )


# ============================================================================
# PUT /api/v1/user-request/{requestId} - Update request status
# ============================================================================

@router.put("/{requestId}", response_model=UserRequestUpdateResponse)
async def update_user_request(
    requestId: str,
    request: UserRequestUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user request status

    Updates the status of an existing request. Only status field can be updated.

    **Path Parameter**:
    - `requestId`: Request ID to update (e.g., REQ_001)

    **Request Body**:
    ```json
    {
        "status": "active"
    }
    ```

    **Valid Status Values**:
    - `pending`: Request is pending approval
    - `active`: Request has been approved and user can be created
    - `rejected`: Request has been rejected

    **Immutable Fields** (ignored if provided):
    - `requestId`: Cannot change
    - `userId`: Cannot change
    - `created_Date`: Cannot change

    **Auto-Updated Fields**:
    - `updated_Date`: Always set to current timestamp

    **Returns**:
    ```json
    {
        "message": "User request updated successfully",
        "data": {
            "requestId": "REQ_001",
            "userId": "john@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "mobileNumber": 9876543210,
            "organization": "Hospital XYZ",
            "currentRole": "DOCTOR",
            "status": "active",
            "city_name": "Mumbai",
            "district_name": "Mumbai",
            "pincode": "400001",
            "state_name": "Maharashtra",
            "created_Date": "2026-03-03T10:30:00",
            "updated_Date": "2026-03-03T10:35:00"
        }
    }
    ```

    **Status Codes**:
    - 200: Request updated successfully
    - 400: Validation error (invalid status value)
    - 404: Request not found
    - 500: Server error
    """
    try:
        # Check if request exists
        existing_request = user_request_db.get_by_request_id(db, requestId)
        if not existing_request:
            raise HTTPException(
                status_code=404,
                detail=f"Request not found: {requestId}"
            )

        # Update status
        updated_request = user_request_db.update_status(db, requestId, request.status)

        return UserRequestUpdateResponse(
            message="User request updated successfully",
            data=UserRequestResponse.from_orm(updated_request)
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating user request: {str(e)}"
        )


# ============================================================================
# NOTE: No DELETE endpoint per specification
# The specification states "no Delete operation required"
# ============================================================================
