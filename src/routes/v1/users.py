"""
API routes for user_master table
Phase 2.3: API Endpoints Development
Date: 2026-03-03

Endpoints:
1. GET /api/v1/users/search - Search by email or mobile (returns existsFlag)
2. POST /api/v1/users - Create new user (auto-generates userId)
3. PUT /api/v1/users/{userId} - Update user (requires commentLog)

Note: No DELETE endpoint per specification
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from src.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserSearchResponse,
    UserCreateResponse, UserUpdateResponse
)
from src.db.user_master_utils import user_master_db
from src.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# ============================================================================
# GET /api/v1/users/search - Search by email or mobile
# ============================================================================

@router.get("/search", response_model=UserSearchResponse)
async def search_user(
    emailId: Optional[str] = Query(None, description="Email address to search for"),
    mobileNumber: Optional[int] = Query(None, description="10-digit mobile number to search for"),
    db: Session = Depends(get_db)
):
    """
    Search for user by email or mobile number

    Returns user details if found, with existsFlag indicating whether user exists.

    **Query Parameters**:
    - `emailId`: Email address (optional)
    - `mobileNumber`: 10-digit mobile number (optional)
    - At least one parameter must be provided

    **Returns**:
    ```json
    {
        "data": {
            "userId": "USER_001",
            "firstName": "John",
            "lastName": "Doe",
            "currentRole": "ADMIN",
            "emailId": "john@example.com",
            "mobileNumber": 9876543210,
            "status": "active",
            ...all other fields...
        },
        "existsFlag": true
    }
    ```

    **Or if not found**:
    ```json
    {
        "data": null,
        "existsFlag": false
    }
    ```

    **Status Codes**:
    - 200: Success (user found or not found)
    - 400: Validation error (no search criteria, invalid format)
    """
    try:
        # Validate: at least one search parameter
        if not emailId and not mobileNumber:
            raise HTTPException(
                status_code=400,
                detail="At least one of emailId or mobileNumber must be provided"
            )

        user_data = None

        # Search by email
        if emailId:
            user_data = user_master_db.get_user_by_email(db, emailId)

        # Search by mobile (if email not found)
        elif mobileNumber:
            user_data = user_master_db.get_user_by_mobile(db, mobileNumber)

        # Return response with existsFlag
        if user_data:
            return UserSearchResponse(
                data=UserResponse.from_orm(user_data),
                existsFlag=True
            )
        else:
            return UserSearchResponse(
                data=None,
                existsFlag=False
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching for user: {str(e)}"
        )


# ============================================================================
# POST /api/v1/users - Create new user
# ============================================================================

@router.post("", response_model=UserCreateResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user

    Creates a new user with auto-generated userId (max + 1).
    Timestamps (createdDate, updatedDate) are auto-set by the system.

    **Request Body**:
    ```json
    {
        "firstName": "John",
        "lastName": "Doe",
        "currentRole": "ADMIN",
        "emailId": "john@example.com",
        "mobileNumber": 9876543210,
        "organisation": "Hospital XYZ",
        "address1": "123 Medical St",
        "address2": "Apt 101",
        "stateId": "MH",
        "stateName": "Maharashtra",
        "districtId": "DIST_01",
        "cityId": "CITY_01",
        "cityName": "Mumbai",
        "pinCode": "400001",
        "status": "active"
    }
    ```

    **Auto-Generated Fields**:
    - `userId`: Generated as max(userId) + 1
    - `createdDate`: Set to CURRENT_TIMESTAMP
    - `updatedDate`: Set to CURRENT_TIMESTAMP

    **Validation Rules**:
    - Email: Must match regex pattern and be unique
    - Mobile: 10 digits, unique
    - Combination of (email, mobile) must be unique
    - Status: Must be one of: active, pending, deceased, inactive
    - Role: Must be one of: ADMIN, DOCTOR, HOSPITAL, NURSE, PARTNER, PATIENT, RECEPTION, TECHNICIAN

    **Returns**:
    ```json
    {
        "message": "User created successfully",
        "data": {
            "userId": "USER_001",
            "firstName": "John",
            ...all fields including createdDate, updatedDate...
        }
    }
    ```

    **Status Codes**:
    - 201: User created successfully
    - 400: Validation error (invalid email, mobile, role, status, etc.)
    - 409: Conflict (email or mobile already exists, or duplicate combination)
    - 500: Server error
    """
    try:
        # Check if email already exists
        if user_master_db.email_exists(db, user.emailId):
            raise HTTPException(
                status_code=409,
                detail=f"Email already exists: {user.emailId}"
            )

        # Check if mobile already exists
        if user_master_db.mobile_exists(db, user.mobileNumber):
            raise HTTPException(
                status_code=409,
                detail=f"Mobile number already exists: {user.mobileNumber}"
            )

        # Check composite uniqueness (email + mobile)
        if user_master_db.email_mobile_combination_exists(db, user.emailId, user.mobileNumber):
            raise HTTPException(
                status_code=409,
                detail="Email and mobile number combination already exists"
            )

        # Create user (userId auto-generated)
        user_dict = user.model_dump(exclude_unset=True)
        created_user = user_master_db.create_user(db, user_dict)

        return UserCreateResponse(
            message="User created successfully",
            data=UserResponse.from_orm(created_user)
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
            detail=f"Error creating user: {str(e)}"
        )


# ============================================================================
# PUT /api/v1/users/{userId} - Update user
# ============================================================================

@router.put("/{userId}", response_model=UserUpdateResponse)
async def update_user(
    userId: str,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing user

    Updates user fields partially or fully. At least one field must be provided along with commentLog.

    **Path Parameter**:
    - `userId`: User ID to update

    **Request Body**:
    ```json
    {
        "firstName": "Jonathan",
        "organisation": "New Hospital",
        "status": "pending",
        "commentLog": "Updated status from active to pending due to contract renewal"
    }
    ```

    **Immutable Fields** (ignored if provided):
    - `userId`: Cannot change
    - `createdDate`: Cannot change

    **Auto-Updated Fields**:
    - `updatedDate`: Always set to current timestamp

    **Required Field**:
    - `commentLog`: REQUIRED for all updates (provides audit trail)

    **Validation Rules**:
    - Email: Must match regex pattern if provided (must be unique unless unchanged)
    - Mobile: 10 digits if provided (must be unique unless unchanged)
    - Status: Must be one of: active, pending, deceased, inactive
    - Role: Must be one of the valid roles if provided

    **Returns**:
    ```json
    {
        "message": "User updated successfully",
        "data": {
            "userId": "USER_001",
            "firstName": "Jonathan",
            "updatedDate": "2026-03-03T13:35:00",
            ...updated fields...
        }
    }
    ```

    **Status Codes**:
    - 200: User updated successfully
    - 400: Validation error (no update fields, invalid values)
    - 404: User not found
    - 409: Conflict (email/mobile already in use)
    - 500: Server error
    """
    try:
        # Check if user exists
        existing_user = user_master_db.get_user_by_id(db, userId)
        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail=f"User not found: {userId}"
            )

        # Get update data
        update_dict = user.model_dump(exclude_unset=True, exclude_none=True)

        # Validate email uniqueness if being updated
        if 'emailId' in update_dict:
            new_email = update_dict['emailId']
            # Check if different from current and already exists
            if new_email.lower() != existing_user.emailId.lower():
                if user_master_db.email_exists(db, new_email):
                    raise HTTPException(
                        status_code=409,
                        detail=f"Email already exists: {new_email}"
                    )

        # Validate mobile uniqueness if being updated
        if 'mobileNumber' in update_dict:
            new_mobile = update_dict['mobileNumber']
            # Check if different from current and already exists
            if new_mobile != existing_user.mobileNumber:
                if user_master_db.mobile_exists(db, new_mobile):
                    raise HTTPException(
                        status_code=409,
                        detail=f"Mobile number already exists: {new_mobile}"
                    )

        # Update user
        updated_user = user_master_db.update_user(db, userId, update_dict)

        return UserUpdateResponse(
            message="User updated successfully",
            data=UserResponse.from_orm(updated_user)
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
            detail=f"Error updating user: {str(e)}"
        )


# ============================================================================
# NOTE: No DELETE endpoint per specification
# The specification states "no Delete operation required"
# ============================================================================
