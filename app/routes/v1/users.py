"""
API routes for User_Master table (APIs 5 & 6)
SELECT operations (API 5) and CRUD operations (API 6)
Enhanced with geographic hierarchy integration (Step 1.2)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/users", tags=["Users"])


# API 5: SELECT - Get all users
@router.get("/all", response_model=APIResponse)
async def get_all_users(
    db=Depends(get_db),
    status: str = Query(None, description="Filter by user status (Active/Inactive)"),
    current_role: str = Query(None, description="Filter by user role"),
    limit: int = Query(100, ge=1, le=1000, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    API 5: SELECT Operation - Retrieve all user profiles with geographic hierarchy

    Returns all users with optional filtering and pagination support.

    **Query Parameters**:
    - `status`: Filter by status (Active/Inactive)
    - `current_role`: Filter by user role
    - `limit`: Number of results (1-1000, default 100)
    - `offset`: Pagination offset (default 0)

    **Response Fields Include**:
    - Geographic references: `stateId`, `districtId`, `cityId`, `pinCode`
    - Display fields: `stateName`, `cityName`
    - Addresses: `address1`, `address2`

    **Example**: `/api/v1/users/all?status=Active&limit=50&offset=0`
    """
    try:
        users = await UserService.get_all_users(db, status, current_role, limit, offset)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Users retrieved successfully",
            data={"users": users, "count": len(users)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 6: CRUD - Create user
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_user(
    user: UserCreate,
    db=Depends(get_db)
):
    """
    API 6: CRUD Operation - Create new user profile with geographic hierarchy

    Creates a new user with provided data including optional geographic references.

    **Geographic Fields** (Optional):
    - `stateId` (int): State ID from State_City_PinCode_Master
    - `districtId` (int): District ID from State_City_PinCode_Master
    - `cityId` (int): City ID from State_City_PinCode_Master
    - `pinCode` (int): Postal code (5-6 digits) from State_City_PinCode_Master

    **Example Request**:
    ```json
    {
        "userId": "user@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "currentRole": "Doctor",
        "emailId": "john@example.com",
        "mobileNumber": "9876543210",
        "organisation": "Hospital XYZ",
        "address1": "123 Medical St",
        "address2": "Apt 101",
        "stateId": 1,
        "stateName": "Maharashtra",
        "districtId": 1,
        "cityId": 1,
        "cityName": "Mumbai",
        "pinCode": 400001
    }
    ```

    **Returns**: Created user profile with all fields
    """
    try:
        # Check if user already exists
        existing = await UserService.get_user_by_id(db, user.userId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User {user.userId} already exists"
            )

        new_user = await UserService.create_user(db, user.dict(exclude_unset=True))

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="User created successfully",
            data={"user": new_user},
            timestamp=datetime.now()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Invalid geographic reference: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 6: CRUD - Update user
@router.put("/{userId}", response_model=APIResponse)
async def update_user(
    userId: str,
    user: UserUpdate,
    db=Depends(get_db)
):
    """
    API 6: CRUD Operation - Update user profile (pinCode is immutable)

    Updates an existing user with partial or full data.

    **Immutable Fields**:
    - `pinCode`: Cannot be updated after creation. Set this during user creation.

    **Updatable Geographic Fields**:
    - `stateId` (int): State ID from State_City_PinCode_Master
    - `districtId` (int): District ID from State_City_PinCode_Master
    - `cityId` (int): City ID from State_City_PinCode_Master

    **Example Request**:
    ```json
    {
        "firstName": "Jonathan",
        "organisation": "New Hospital",
        "stateId": 2,
        "stateName": "Karnataka",
        "districtId": 2,
        "cityId": 2,
        "cityName": "Bangalore"
    }
    ```

    **Note**: Only provided fields will be updated. Omitted fields retain their current values.
    """
    try:
        # Check if user exists
        existing = await UserService.get_user_by_id(db, userId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User {userId} not found"
            )

        updated_user = await UserService.update_user(db, userId, user.dict(exclude_unset=True))

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="User updated successfully",
            data={"user": updated_user},
            timestamp=datetime.now()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Invalid geographic reference: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 6: CRUD - Delete user
@router.delete("/{userId}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(
    userId: str,
    db=Depends(get_db)
):
    """
    API 6: CRUD Operation - Delete user profile

    Deletes a user by their ID.

    **Note**: Deletion will fail with FOREIGN KEY constraint error if the user has
    associated records in other tables that reference this user (e.g., Report_History).

    **Returns**: 204 No Content on success
    """
    try:
        # Check if user exists
        existing = await UserService.get_user_by_id(db, userId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User {userId} not found"
            )

        success = await UserService.delete_user(db, userId)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
