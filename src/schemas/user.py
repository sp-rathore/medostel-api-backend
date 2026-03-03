"""
Pydantic schemas for user_master table
Phase 2.1: Schema & Model Definition
Updated: March 3, 2026

Schemas:
- UserBase: Base model with common fields
- UserCreate: POST request schema for creating new users
- UserUpdate: PUT request schema for updating users
- UserResponse: API response model with all fields

Validation Rules:
- Email: Standard email format + regex pattern
- Mobile: 10-digit numeric (1000000000-9999999999)
- Status: active, pending, deceased, inactive
- currentRole: References user_role_master.rolename
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    """Base schema for user with common fields"""
    firstName: str = Field(..., min_length=1, max_length=50, description="User first name (required)")
    lastName: str = Field(..., min_length=1, max_length=50, description="User last name (required)")
    currentRole: str = Field(..., max_length=50, description="Role name (required, references user_role_master.rolename)")
    emailId: str = Field(..., max_length=255, description="Email address (required, must be valid format and unique)")
    mobileNumber: int = Field(..., ge=1000000000, le=9999999999, description="Mobile number (required, 10 digits, must be unique)")
    organisation: Optional[str] = Field(None, max_length=255, description="Organization name (optional)")
    status: str = Field(default="active", max_length=50, description="User status (default: active)")


class UserCreate(UserBase):
    """Schema for creating a new user via POST request"""
    # Note: userId is NOT provided by client - it's auto-generated as max(userId) + 1
    # Note: createdDate and updatedDate are auto-set by system

    address1: Optional[str] = Field(None, max_length=255, description="Primary address (optional)")
    address2: Optional[str] = Field(None, max_length=255, description="Secondary address (optional)")
    stateId: Optional[str] = Field(None, max_length=10, description="State ID (optional, varchar reference)")
    stateName: Optional[str] = Field(None, max_length=100, description="State name (optional)")
    districtId: Optional[str] = Field(None, max_length=10, description="District ID (optional, varchar reference)")
    cityId: Optional[str] = Field(None, max_length=10, description="City ID (optional, varchar reference)")
    cityName: Optional[str] = Field(None, max_length=100, description="City name (optional)")
    pinCode: Optional[str] = Field(None, max_length=10, description="PIN code (optional, varchar reference)")

    @field_validator('emailId')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """
        Validate email format using regex pattern
        Pattern: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$
        """
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()  # Normalize to lowercase

    @field_validator('mobileNumber')
    @classmethod
    def validate_mobile_format(cls, v: int) -> int:
        """
        Validate mobile number is exactly 10 digits (1000000000-9999999999)
        """
        if v < 1000000000 or v > 9999999999:
            raise ValueError('Mobile number must be 10 digits (1000000000-9999999999)')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """
        Validate status is one of the allowed values
        Valid: active, pending, deceased, inactive
        """
        allowed_statuses = {'active', 'pending', 'deceased', 'inactive'}
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v.lower()

    @field_validator('currentRole')
    @classmethod
    def validate_role_name(cls, v: str) -> str:
        """
        Validate currentRole is one of the valid role names
        Valid roles: ADMIN, DOCTOR, HOSPITAL, NURSE, PARTNER, PATIENT, RECEPTION, TECHNICIAN
        """
        allowed_roles = {'ADMIN', 'DOCTOR', 'HOSPITAL', 'NURSE', 'PARTNER', 'PATIENT', 'RECEPTION', 'TECHNICIAN'}
        if v.upper() not in allowed_roles:
            raise ValueError(f"Invalid role. Valid roles: {', '.join(sorted(allowed_roles))}")
        return v.upper()


class UserUpdate(BaseModel):
    """Schema for updating a user via PUT request"""
    # Note: userId is immutable (cannot be updated)
    # Note: createdDate is immutable (cannot be updated)
    # Note: updatedDate is auto-updated by system
    # Note: commentLog is REQUIRED for all updates (audit trail)

    firstName: Optional[str] = Field(None, min_length=1, max_length=50, description="First name (optional)")
    lastName: Optional[str] = Field(None, min_length=1, max_length=50, description="Last name (optional)")
    currentRole: Optional[str] = Field(None, max_length=50, description="Role name (optional)")
    emailId: Optional[str] = Field(None, max_length=255, description="Email address (optional, must be unique if changed)")
    mobileNumber: Optional[int] = Field(None, ge=1000000000, le=9999999999, description="Mobile number (optional, must be unique if changed)")
    organisation: Optional[str] = Field(None, max_length=255, description="Organization (optional)")
    status: Optional[str] = Field(None, max_length=50, description="Status (optional)")
    address1: Optional[str] = Field(None, max_length=255, description="Primary address (optional)")
    address2: Optional[str] = Field(None, max_length=255, description="Secondary address (optional)")
    stateId: Optional[str] = Field(None, max_length=10, description="State ID (optional)")
    stateName: Optional[str] = Field(None, max_length=100, description="State name (optional)")
    districtId: Optional[str] = Field(None, max_length=10, description="District ID (optional)")
    cityId: Optional[str] = Field(None, max_length=10, description="City ID (optional)")
    cityName: Optional[str] = Field(None, max_length=100, description="City name (optional)")
    pinCode: Optional[str] = Field(None, max_length=10, description="PIN code (optional)")
    commentLog: str = Field(..., max_length=255, description="Change description/comment (REQUIRED for audit trail)")

    @field_validator('emailId')
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate email format if provided"""
        if v is None:
            return v
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('mobileNumber')
    @classmethod
    def validate_mobile_format(cls, v: Optional[int]) -> Optional[int]:
        """Validate mobile number if provided"""
        if v is None:
            return v
        if v < 1000000000 or v > 9999999999:
            raise ValueError('Mobile number must be 10 digits (1000000000-9999999999)')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status if provided"""
        if v is None:
            return v
        allowed_statuses = {'active', 'pending', 'deceased', 'inactive'}
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v.lower()

    @field_validator('currentRole')
    @classmethod
    def validate_role_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate role name if provided"""
        if v is None:
            return v
        allowed_roles = {'ADMIN', 'DOCTOR', 'HOSPITAL', 'NURSE', 'PARTNER', 'PATIENT', 'RECEPTION', 'TECHNICIAN'}
        if v.upper() not in allowed_roles:
            raise ValueError(f"Invalid role. Valid roles: {', '.join(sorted(allowed_roles))}")
        return v.upper()

    @model_validator(mode='after')
    def at_least_one_field(self):
        """Ensure at least one field is being updated"""
        # commentLog is always provided, so check if there's anything else to update
        update_fields = {
            self.firstName, self.lastName, self.currentRole, self.emailId,
            self.mobileNumber, self.organisation, self.status, self.address1,
            self.address2, self.stateId, self.stateName, self.districtId,
            self.cityId, self.cityName, self.pinCode
        }
        if all(field is None for field in update_fields):
            raise ValueError('At least one field must be provided for update')
        return self


class UserResponse(UserBase):
    """Schema for API response containing all user fields"""
    userId: str = Field(..., description="Unique user identifier")
    address1: Optional[str] = Field(None, description="Primary address")
    address2: Optional[str] = Field(None, description="Secondary address")
    stateId: Optional[str] = Field(None, description="State ID")
    stateName: Optional[str] = Field(None, description="State name")
    districtId: Optional[str] = Field(None, description="District ID")
    cityId: Optional[str] = Field(None, description="City ID")
    cityName: Optional[str] = Field(None, description="City name")
    pinCode: Optional[str] = Field(None, description="PIN code")
    commentLog: Optional[str] = Field(None, description="Most recent change comment")
    createdDate: datetime = Field(..., description="Record creation timestamp (immutable)")
    updatedDate: datetime = Field(..., description="Last update timestamp (auto-updated)")

    class Config:
        from_attributes = True  # Allow population from ORM models


class UserSearchResponse(BaseModel):
    """Schema for search response (GET by email or mobile)"""
    data: Optional[UserResponse] = Field(None, description="User data if found")
    existsFlag: bool = Field(..., description="True if user exists, False otherwise")

    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    """Schema for create response (POST success)"""
    message: str = Field("User created successfully", description="Success message")
    data: UserResponse = Field(..., description="Created user data")


class UserUpdateResponse(BaseModel):
    """Schema for update response (PUT success)"""
    message: str = Field("User updated successfully", description="Success message")
    data: UserResponse = Field(..., description="Updated user data")
