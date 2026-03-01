"""
API routes for User_Login table (APIs 7 & 8)
SELECT operations (API 7) and CRUD operations (API 8)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user_login import UserLoginCreate, UserLoginUpdate
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/auth", tags=["Authentication"])


# API 7: SELECT - Get all login records
@router.get("/users", response_model=APIResponse)
async def get_all_login_users(
    db=Depends(get_db),
    is_active: bool = Query(None),
    role_id: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    API 7: SELECT Operation - Retrieve all user login records
    - Returns all login records with optional filtering
    - Supports pagination with limit and offset
    """
    try:
        records = await AuthService.get_all_login_records(db, is_active, role_id, limit, offset)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="User login records retrieved successfully",
            data={"loginRecords": records, "count": len(records)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 8: CRUD - Create login credentials
@router.post("/credentials", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_login_credentials(
    login: UserLoginCreate,
    db=Depends(get_db)
):
    """
    API 8: CRUD Operation - Create user login credentials
    - Creates login credentials for a user
    - Password is hashed before storage
    """
    try:
        # Check if login already exists
        existing = await AuthService.get_login_by_id(db, login.userId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Login credentials already exist for user {login.userId}"
            )

        new_login = await AuthService.create_login(db, login.dict())

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Login credentials created successfully",
            data={"login": new_login},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 8: CRUD - Update login credentials
@router.put("/credentials/{userId}", response_model=APIResponse)
async def update_login_credentials(
    userId: str,
    login: UserLoginUpdate,
    db=Depends(get_db)
):
    """
    API 8: CRUD Operation - Update user login credentials
    - Updates login credentials for a user
    - Returns the updated login record
    """
    try:
        # Check if login exists
        existing = await AuthService.get_login_by_id(db, userId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Login credentials not found for user {userId}"
            )

        updated_login = await AuthService.update_login(db, userId, login.dict(exclude_unset=True))

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Login credentials updated successfully",
            data={"login": updated_login},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 8: CRUD - Delete login credentials
@router.delete("/credentials/{userId}", response_model=APIResponse, status_code=HTTPStatus.NO_CONTENT)
async def delete_login_credentials(
    userId: str,
    db=Depends(get_db)
):
    """
    API 8: CRUD Operation - Delete user login credentials
    - Deletes login credentials for a user
    - Returns 204 No Content on success
    """
    try:
        # Check if login exists
        existing = await AuthService.get_login_by_id(db, userId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Login credentials not found for user {userId}"
            )

        success = await AuthService.delete_login(db, userId)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete login credentials"
            )

        return APIResponse(
            status="success",
            code=HTTPStatus.NO_CONTENT,
            message="Login credentials deleted successfully",
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
