"""
API routes for User_Role_Master table (APIs 1 & 2)
SELECT operations (API 1) and CRUD operations (API 2)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime
from app.database import get_db
from app.services.user_role_service import UserRoleService
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate, UserRoleResponse
from app.schemas.common import APIResponse
from app.constants import ErrorCodes, HTTPStatus

router = APIRouter(prefix="/roles", tags=["User Roles"])


# API 1: SELECT - Get all user roles
@router.get("/all", response_model=APIResponse)
async def get_all_roles(
    db=Depends(get_db),
    status: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    API 1: SELECT Operation - Retrieve all user roles
    - Returns all roles with optional filtering by status
    - Supports pagination with limit and offset
    """
    try:
        roles = await UserRoleService.get_all_roles(db, status, limit, offset)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="User roles retrieved successfully",
            data={"roles": roles, "count": len(roles)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 2: CRUD - Create role
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_role(
    role: UserRoleCreate,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Create new user role
    - Creates a new role with provided data
    - Returns the created role
    """
    try:
        # Check if role already exists
        existing = await UserRoleService.get_role_by_id(db, role.roleId)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Role {role.roleId} already exists"
            )

        new_role = await UserRoleService.create_role(db, role.dict())

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Role created successfully",
            data={"role": new_role},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 2: CRUD - Update role
@router.put("/{roleId}", response_model=APIResponse)
async def update_role(
    roleId: str,
    role: UserRoleUpdate,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Update user role
    - Updates an existing role
    - Returns the updated role
    """
    try:
        # Check if role exists
        existing = await UserRoleService.get_role_by_id(db, roleId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Role {roleId} not found"
            )

        updated_role = await UserRoleService.update_role(db, roleId, role.dict(exclude_unset=True))

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Role updated successfully",
            data={"role": updated_role},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 2: CRUD - Delete role
@router.delete("/{roleId}", response_model=APIResponse, status_code=HTTPStatus.NO_CONTENT)
async def delete_role(
    roleId: str,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Delete user role
    - Deletes a role by ID
    - Returns 204 No Content on success
    """
    try:
        # Check if role exists
        existing = await UserRoleService.get_role_by_id(db, roleId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Role {roleId} not found"
            )

        success = await UserRoleService.delete_role(db, roleId)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete role"
            )

        return APIResponse(
            status="success",
            code=HTTPStatus.NO_CONTENT,
            message="Role deleted successfully",
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
