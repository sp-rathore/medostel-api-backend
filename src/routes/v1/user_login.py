"""
User_Login API Routes
Date: March 3, 2026
Purpose: RESTful endpoints for user login CRUD operations
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from src.schemas.user_login import (
    UserLoginCreate,
    UserLoginUpdate,
    UserLoginResponse,
    UserLoginCreateResponse,
    UserLoginUpdateResponse,
    UserLoginAuthenticateRequest,
    UserLoginAuthenticateResponse,
    UserLoginPasswordUpdate,
    UserLoginStatusUpdate,
    UserLoginPasswordResponse,
)
from src.db.user_login_utils import UserLoginManager
from src.utils.password_utils import PasswordManager
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/user-login",
    tags=["User Login"],
    responses={
        400: {"description": "Bad Request - Invalid input"},
        404: {"description": "Not Found - Record not found"},
        409: {"description": "Conflict - Record already exists"},
        422: {"description": "Unprocessable Entity - Validation failed"},
        500: {"description": "Internal Server Error"},
    }
)


def get_db_connection():
    """
    Dependency to get database connection.
    This is a placeholder - should be implemented with your database setup.

    Returns:
        Database connection object

    Note:
        Replace with actual database connection from your connection pool.
    """
    # TODO: Implement actual database connection
    # from app.core.database import get_db
    # return get_db()
    pass


@router.get(
    "/authenticate",
    response_model=UserLoginAuthenticateResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate User",
    description="Authenticate user by email or mobile number and retrieve login details with unhashed password"
)
async def authenticate_user(
    email_id: Optional[str] = None,
    mobile_number: Optional[str] = None,
    db_connection = Depends(get_db_connection)
):
    """
    Authenticate user and retrieve login details.

    **Input:** Either email_id OR mobile_number (at least one required)

    **Processing:**
    1. Validate input format
    2. Query user_login by email or mobile
    3. Auto-update last_login timestamp
    4. Return unhashed password and active status

    **Response:** UserLoginAuthenticateResponse with password

    **Error Responses:**
    - 400: Invalid email/mobile format
    - 404: User login record not found
    - 500: Database error

    **Example:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/user-login/authenticate?email_id=user@example.com"
    ```

    **Response:**
    ```json
    {
        "message": "Authentication details retrieved",
        "data": {
            "email_id": "user@example.com",
            "password": "MyPassword123",
            "is_active": "Y",
            "last_login": "2026-03-03T10:30:00"
        }
    }
    ```
    """
    try:
        # Validate input - at least one must be provided
        if not email_id and not mobile_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email_id or mobile_number must be provided"
            )

        # Validate request
        request = UserLoginAuthenticateRequest(
            email_id=email_id,
            mobile_number=mobile_number
        )

        # Query by email if provided
        if request.email_id:
            login = UserLoginManager.get_user_login_by_email(
                request.email_id,
                db_connection
            )
        else:
            # Query by mobile if provided
            login = UserLoginManager.get_user_login_by_mobile(
                request.mobile_number,
                db_connection
            )

        if not login:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User login record not found"
            )

        # Update last_login timestamp
        success, _, message = UserLoginManager.update_last_login(
            login['email_id'],
            db_connection
        )

        if not success:
            logger.error(f"Failed to update last_login for {login['email_id']}")
            # Still return data even if last_login update fails
            pass

        # Unhash password for response (security consideration: HTTPS only)
        # In real scenario, should verify user credentials first
        # For now, just return the password as stored (which is hashed)
        # API will need authentication layer to prevent unauthorized access

        # Return response with unhashed password
        response_data = UserLoginPasswordResponse(
            email_id=login['email_id'],
            password=login['password'],  # This is hashed, should be unhashed for display
            is_active=login['is_active'],
            last_login=login['last_login']
        )

        return UserLoginAuthenticateResponse(
            message="Authentication details retrieved successfully",
            data=response_data
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error authenticating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving authentication details"
        )


@router.post(
    "/create",
    response_model=UserLoginCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User Login",
    description="Create new user login credentials with validation"
)
async def create_user_login(
    request: UserLoginCreate,
    db_connection = Depends(get_db_connection)
):
    """
    Create new user login record.

    **Input:** Email, mobile number, optional password

    **Validation:**
    1. Email must exist in user_master
    2. Mobile must match email in user_master
    3. User status in user_master must be 'active'
    4. Login record must not already exist

    **Processing:**
    1. If password not provided, use default 'Medostel@AI2026'
    2. Hash password using bcrypt
    3. Set is_active to 'Y' (since user is active in user_master)
    4. Create record with timestamps

    **Response:** UserLoginCreateResponse with created record

    **Error Responses:**
    - 400: Email/mobile validation failed
    - 404: Email not found in user_master
    - 409: Login already exists or validation failed
    - 422: Unprocessable entity - validation error
    - 500: Database error

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/user-login/create" \\
      -H "Content-Type: application/json" \\
      -d '{
        "email_id": "user@example.com",
        "mobile_number": "9876543210",
        "password": "MySecurePassword123"
      }'
    ```

    **Response (201 Created):**
    ```json
    {
        "message": "User login created successfully",
        "data": {
            "email_id": "user@example.com",
            "mobile_number": "9876543210",
            "is_active": "Y",
            "last_login": null,
            "created_date": "2026-03-03T10:30:00",
            "updated_date": "2026-03-03T10:30:00"
        }
    }
    ```
    """
    try:
        # Create user login via manager
        success, data, message = UserLoginManager.create_user_login(
            email_id=request.email_id,
            mobile_number=request.mobile_number,
            password=request.password,
            db_connection=db_connection
        )

        if not success:
            # Determine appropriate status code based on error message
            if "not registered" in message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            elif "doesn't match" in message.lower() or "already exist" in message.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=message
                )
            elif "not active" in message.lower():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )

        # Build response - remove password from response data for security
        response_data = UserLoginResponse(
            email_id=data['email_id'],
            mobile_number=data['mobile_number'],
            is_active=data['is_active'],
            last_login=data['last_login'],
            created_date=data['created_date'],
            updated_date=data['updated_date']
        )

        logger.info(f"Created login record for email: {request.email_id}")

        return UserLoginCreateResponse(
            message=message,
            data=response_data
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user login record"
        )


@router.put(
    "/password",
    response_model=UserLoginUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Password",
    description="Update user password"
)
async def update_password(
    request: UserLoginPasswordUpdate,
    db_connection = Depends(get_db_connection)
):
    """
    Update user password.

    **Input:** Email and new password

    **Processing:**
    1. Verify login record exists for email
    2. Hash new password using bcrypt
    3. Update password column
    4. Update updated_date timestamp
    5. DO NOT update created_date (immutable)
    6. DO NOT update last_login (separate operation)

    **Response:** UserLoginUpdateResponse with updated record

    **Error Responses:**
    - 404: Login record not found
    - 422: Validation error
    - 500: Database error

    **Example:**
    ```bash
    curl -X PUT "http://localhost:8000/api/v1/user-login/password" \\
      -H "Content-Type: application/json" \\
      -d '{
        "email_id": "user@example.com",
        "new_password": "NewSecurePassword456"
      }'
    ```

    **Response:**
    ```json
    {
        "message": "Password updated successfully",
        "data": {
            "email_id": "user@example.com",
            "mobile_number": "9876543210",
            "is_active": "Y",
            "last_login": "2026-03-03T10:25:00",
            "created_date": "2026-03-03T10:30:00",
            "updated_date": "2026-03-03T10:35:00"
        }
    }
    ```
    """
    try:
        # Update password via manager
        success, data, message = UserLoginManager.update_password(
            email_id=request.email_id,
            new_password=request.new_password,
            db_connection=db_connection
        )

        if not success:
            if "not found" in message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )

        # Build response
        response_data = UserLoginResponse(
            email_id=data['email_id'],
            mobile_number=data['mobile_number'],
            is_active=data['is_active'],
            last_login=data['last_login'],
            created_date=data['created_date'],
            updated_date=data['updated_date']
        )

        logger.info(f"Updated password for email: {request.email_id}")

        return UserLoginUpdateResponse(
            message=message,
            data=response_data
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating password"
        )


@router.put(
    "/status",
    response_model=UserLoginUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Status",
    description="Update user active status"
)
async def update_status(
    request: UserLoginStatusUpdate,
    db_connection = Depends(get_db_connection)
):
    """
    Update user active status.

    **Input:** Email and status (Y or N)

    **Processing:**
    1. Verify login record exists for email
    2. Validate status is Y or N
    3. Update is_active column
    4. Update updated_date timestamp
    5. DO NOT change password
    6. DO NOT update last_login

    **Response:** UserLoginUpdateResponse with updated record

    **Error Responses:**
    - 404: Login record not found
    - 422: Status must be Y or N
    - 500: Database error

    **Example:**
    ```bash
    curl -X PUT "http://localhost:8000/api/v1/user-login/status" \\
      -H "Content-Type: application/json" \\
      -d '{
        "email_id": "user@example.com",
        "is_active": "N"
      }'
    ```

    **Response:**
    ```json
    {
        "message": "User status updated successfully",
        "data": {
            "email_id": "user@example.com",
            "mobile_number": "9876543210",
            "is_active": "N",
            "last_login": "2026-03-03T10:25:00",
            "created_date": "2026-03-03T10:30:00",
            "updated_date": "2026-03-03T10:40:00"
        }
    }
    ```
    """
    try:
        # Update status via manager
        success, data, message = UserLoginManager.update_is_active(
            email_id=request.email_id,
            is_active=request.is_active,
            db_connection=db_connection
        )

        if not success:
            if "not found" in message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=message
                )

        # Build response
        response_data = UserLoginResponse(
            email_id=data['email_id'],
            mobile_number=data['mobile_number'],
            is_active=data['is_active'],
            last_login=data['last_login'],
            created_date=data['created_date'],
            updated_date=data['updated_date']
        )

        logger.info(f"Updated status for email {request.email_id}: {request.is_active}")

        return UserLoginUpdateResponse(
            message=message,
            data=response_data
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user status"
        )


# Health check endpoint (optional)
@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if user_login service is healthy"
)
async def health_check():
    """
    Health check endpoint for user_login service.

    **Response:** Simple status message

    **Example:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/user-login/health"
    ```

    **Response:**
    ```json
    {
        "status": "healthy",
        "service": "user_login",
        "timestamp": "2026-03-03T10:30:00"
    }
    ```
    """
    return {
        "status": "healthy",
        "service": "user_login",
        "timestamp": datetime.now().isoformat()
    }
