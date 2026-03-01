"""
API routes for User_Master table (APIs 5 & 6)
SELECT operations (API 5) and CRUD operations (API 6)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/users", tags=["Users"])


# API 5: SELECT - Get all users
@router.get("/all", response_model=APIResponse)
async def get_all_users(
    db=Depends(get_db),
    status: str = Query(None),
    current_role: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    API 5: SELECT Operation - Retrieve all user profiles
    - Returns all users with optional filtering
    - Supports pagination with limit and offset
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
    API 6: CRUD Operation - Create new user profile
    - Creates a new user with provided data
    - Returns the created user
    """
    try:
        # Check if user already exists
        existing = await UserService.get_user_by_id(db, user.userId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User {user.userId} already exists"
            )

        new_user = await UserService.create_user(db, user.dict())

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="User created successfully",
            data={"user": new_user},
            timestamp=datetime.now()
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
    API 6: CRUD Operation - Update user profile
    - Updates an existing user
    - Returns the updated user
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 6: CRUD - Delete user
@router.delete("/{userId}", response_model=APIResponse, status_code=HTTPStatus.NO_CONTENT)
async def delete_user(
    userId: str,
    db=Depends(get_db)
):
    """
    API 6: CRUD Operation - Delete user profile
    - Deletes a user by ID
    - Returns 204 No Content on success
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

        return APIResponse(
            status="success",
            code=HTTPStatus.NO_CONTENT,
            message="User deleted successfully",
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
