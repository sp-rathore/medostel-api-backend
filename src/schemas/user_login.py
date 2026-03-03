"""
Pydantic schemas for User_Login module
Date: March 3, 2026
Purpose: Define request/response models with validation for user login credentials
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class UserLoginBase(BaseModel):
    """Base schema for user login - common fields"""
    email_id: str = Field(..., description="Email ID (PK, from user_master)")
    mobile_number: str = Field(..., description="10-digit mobile number")

    @field_validator('email_id')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """
        Validate email format using RFC 5322 compliant regex.

        Args:
            v: Email address to validate

        Returns:
            Lowercase email address

        Raises:
            ValueError: If email format is invalid
        """
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('mobile_number')
    @classmethod
    def validate_mobile_format(cls, v: str) -> str:
        """
        Validate mobile number is exactly 10 digits.

        Args:
            v: Mobile number to validate

        Returns:
            Mobile number string

        Raises:
            ValueError: If not exactly 10 digits
        """
        # Remove spaces and special chars if present
        v = v.strip()

        # Check if it's numeric
        if not v.isdigit():
            raise ValueError('Mobile number must contain only digits')

        # Check if it's exactly 10 digits
        if len(v) != 10:
            raise ValueError('Mobile number must be exactly 10 digits')

        # Validate range: 1000000000 to 9999999999
        mobile_int = int(v)
        if mobile_int < 1000000000 or mobile_int > 9999999999:
            raise ValueError('Mobile number must be between 1000000000 and 9999999999')

        return v


class UserLoginCreate(UserLoginBase):
    """Schema for creating new user login credentials"""
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=255,
        description="Password (optional, uses default if not provided)"
    )

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate password if provided.

        Args:
            v: Password to validate (can be None for default)

        Returns:
            Password string or None

        Raises:
            ValueError: If password provided but less than 8 characters
        """
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLoginUpdate(BaseModel):
    """Schema for updating user login credentials"""

    # Option 1: Update password
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=255,
        description="New password (min 8 chars)"
    )

    # Option 2: Update active status
    is_active: Optional[str] = Field(
        None,
        description="Active status: Y or N"
    )

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """Validate password if provided"""
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @field_validator('is_active')
    @classmethod
    def validate_is_active(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate is_active is Y or N.

        Args:
            v: Status value to validate

        Returns:
            Uppercase status (Y or N)

        Raises:
            ValueError: If not Y or N
        """
        if v is not None:
            v_upper = v.upper()
            if v_upper not in ['Y', 'N']:
                raise ValueError('is_active must be Y or N')
            return v_upper
        return v


class UserLoginResponse(UserLoginBase):
    """Schema for user login response (read-only)"""
    is_active: str = Field(..., description="Active status: Y or N")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    created_date: datetime = Field(..., description="Record creation date")
    updated_date: datetime = Field(..., description="Record last update date")

    class Config:
        from_attributes = True


class UserLoginAuthenticateRequest(BaseModel):
    """Schema for authentication request"""
    email_id: Optional[str] = Field(None, description="Email ID")
    mobile_number: Optional[str] = Field(None, description="Mobile number")

    @field_validator('email_id')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Validate email if provided"""
        if v is not None:
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Invalid email format')
            return v.lower()
        return v

    @field_validator('mobile_number')
    @classmethod
    def validate_mobile(cls, v: Optional[str]) -> Optional[str]:
        """Validate mobile number if provided"""
        if v is not None:
            v = v.strip()
            if not v.isdigit() or len(v) != 10:
                raise ValueError('Mobile number must be exactly 10 digits')
        return v


class UserLoginPasswordUpdate(BaseModel):
    """Schema for password change request"""
    email_id: str = Field(..., description="Email ID")
    new_password: str = Field(..., min_length=8, max_length=255, description="New password")

    @field_validator('email_id')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate new password"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserLoginStatusUpdate(BaseModel):
    """Schema for status change request"""
    email_id: str = Field(..., description="Email ID")
    is_active: str = Field(..., description="New status: Y or N")

    @field_validator('email_id')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('is_active')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is Y or N"""
        v_upper = v.upper()
        if v_upper not in ['Y', 'N']:
            raise ValueError('is_active must be Y or N')
        return v_upper


class UserLoginPasswordResponse(BaseModel):
    """Schema for authentication response with password"""
    email_id: str
    password: str = Field(..., description="Unhashed password (for display only)")
    is_active: str
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLoginCreateResponse(BaseModel):
    """Schema for create user login response"""
    message: str
    data: UserLoginResponse


class UserLoginUpdateResponse(BaseModel):
    """Schema for update user login response"""
    message: str
    data: UserLoginResponse


class UserLoginAuthenticateResponse(BaseModel):
    """Schema for authenticate endpoint response"""
    message: str
    data: UserLoginPasswordResponse
