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
    roleId: str = Query(None, description="Fetch by specific Role ID (converted to uppercase)"),
    status: str = Query(None, description="Filter by role status (Active, Inactive, Pending)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    API 1: SELECT Operation - Retrieve user roles with flexible filtering

    Supports three request scenarios:

    1. **Request with roleId parameter**:
       - Fetch all details for a specific role by ID
       - Role ID is automatically converted to UPPERCASE for case-insensitive matching
       - Example: ?roleId=admin → fetches ADMIN role

    2. **Request with status parameter**:
       - Fetch all roles with a specific status
       - Valid values: Active, Inactive, Pending
       - Example: ?status=Active → fetches all active roles

    3. **Request with no parameters**:
       - Fetch all roles from User_Role_Master table
       - Returns all columns and all rows irrespective of status
       - Example: /api/v1/roles/all → fetches all 8 roles

    Pagination: Use limit and offset parameters for result pagination
    """
    try:
        # Scenario 1: Fetch by specific Role ID (case-insensitive)
        if roleId:
            # Convert roleId to uppercase for case-insensitive matching
            roleId_upper = roleId.upper()
            role = await UserRoleService.get_role_by_id(db, roleId_upper)

            if not role:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Role with ID '{roleId}' not found"
                )

            return APIResponse(
                status="success",
                code=HTTPStatus.OK,
                message=f"Role '{roleId_upper}' retrieved successfully",
                data={"roles": [role], "count": 1, "scenario": "Fetch by Role ID"},
                timestamp=datetime.now()
            )

        # Scenario 2: Fetch by status or Scenario 3: Fetch all
        roles = await UserRoleService.get_all_roles(db, status, limit, offset)

        scenario_message = "Fetch all roles with status filter" if status else "Fetch all roles"
        detail_message = f"Retrieved {len(roles)} role(s) with status '{status}'" if status else "Retrieved all roles from User_Role_Master"

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=detail_message,
            data={"roles": roles, "count": len(roles), "scenario": scenario_message},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
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
@router.delete("/{roleId}", status_code=HTTPStatus.NO_CONTENT)
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
