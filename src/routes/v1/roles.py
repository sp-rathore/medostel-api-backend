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


# API 2: CRUD - Create role (Insert)
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_role(
    role: UserRoleCreate,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Insert new user role

    **Request Scenario: Insert New Role**

    Input required:
    - roleId: Unique role identifier (max 10 chars, uppercase)
    - roleName: Human-readable role name (max 50 chars)
    - status: Role status (Active, Inactive, or Closed)
    - comments: Optional description (max 250 chars)

    System-generated fields (auto-populated):
    - createdDate: Set to current system timestamp
    - updatedDate: Set to current system timestamp

    Returns: Created role with all fields including timestamps
    """
    try:
        # Check if role already exists
        role_id_upper = role.roleId.upper()
        existing = await UserRoleService.get_role_by_id(db, role_id_upper)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Role '{role_id_upper}' already exists"
            )

        # Validate status is one of the allowed values
        allowed_statuses = ["Active", "Inactive", "Closed"]
        if role.status not in allowed_statuses:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(allowed_statuses)}"
            )

        # Create role data with uppercase roleId
        role_data = role.dict()
        role_data['roleId'] = role_id_upper

        # createdDate and updatedDate are auto-set to current timestamp in the service layer
        new_role = await UserRoleService.create_role(db, role_data)

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Role created successfully",
            data={
                "role": new_role,
                "scenario": "Insert new role",
                "info": "createdDate and updatedDate set to current system timestamp"
            },
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 2: CRUD - Update role (Status Update only)
@router.put("/{roleId}", response_model=APIResponse)
async def update_role(
    roleId: str,
    status_update: dict,
    db=Depends(get_db)
):
    """
    API 2: CRUD Operation - Update user role status

    **Request Scenario: Update Role Status**

    URL Parameter:
    - roleId: The role ID to update (will be converted to uppercase)

    Input required:
    - status: New status value (must be one of: Active, Inactive, Closed)

    System-managed fields:
    - updatedDate: Automatically set to current system timestamp
    - Other fields (roleId, roleName, comments): Cannot be updated through this endpoint

    Returns: Updated role with new status and updated timestamp
    """
    try:
        # Convert roleId to uppercase for consistency
        role_id_upper = roleId.upper()

        # Check if role exists
        existing = await UserRoleService.get_role_by_id(db, role_id_upper)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Role '{role_id_upper}' not found"
            )

        # Extract status from request body
        if "status" not in status_update:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Request body must contain 'status' field"
            )

        new_status = status_update.get("status")

        # Validate status is one of the allowed values
        allowed_statuses = ["Active", "Inactive", "Closed"]
        if new_status not in allowed_statuses:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(allowed_statuses)}. Received: '{new_status}'"
            )

        # Update only the status field
        update_data = {"status": new_status}
        updated_role = await UserRoleService.update_role(db, role_id_upper, update_data)

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message=f"Role '{role_id_upper}' status updated to '{new_status}' successfully",
            data={
                "role": updated_role,
                "scenario": "Update role status",
                "info": "updatedDate set to current system timestamp. Other fields cannot be modified."
            },
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
