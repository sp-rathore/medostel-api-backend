"""
Pydantic schemas for new_user_request table
Phase 2.1: Schema & Model Definition
Date: March 3, 2026

Schemas:
- UserRequestBase: Base model with common fields
- UserRequestCreate: POST request schema for creating new requests
- UserRequestUpdate: PUT request schema for updating request status
- UserRequestResponse: API response model with all fields
- UserRequestSearchResponse: Search result wrapper with data and existsFlag

Validation Rules:
- userId (email): RFC 5322 regex pattern, case-insensitive uniqueness
- mobileNumber: 10-digit numeric (1000000000-9999999999)
- status: 'pending', 'active', 'rejected'
- currentRole: Validates against user_role_master.roleName
- Location fields: Validate against state_city_pincode_master
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
import re


class UserRequestBase(BaseModel):
    """Base schema for user request with common fields"""
    firstName: str = Field(..., min_length=1, max_length=100, description="First name (required)")
    lastName: str = Field(..., min_length=1, max_length=100, description="Last name (required)")
    mobileNumber: int = Field(..., ge=1000000000, le=9999999999, description="Mobile number (required, 10 digits)")
    organization: Optional[str] = Field(None, max_length=255, description="Organization (optional)")
    currentRole: str = Field(..., max_length=50, description="Role name (required)")
    city_name: Optional[str] = Field(None, max_length=100, description="City name (optional)")
    district_name: Optional[str] = Field(None, max_length=100, description="District name (optional)")
    pincode: Optional[str] = Field(None, max_length=10, description="PIN code (optional)")
    state_name: Optional[str] = Field(None, max_length=100, description="State name (optional)")
    status: str = Field(default="pending", max_length=50, description="Request status (default: pending)")


class UserRequestCreate(UserRequestBase):
    """Schema for creating a new user request via POST request"""
    # Note: requestId is NOT provided by client - it's auto-generated as max(requestId) + 1
    # Note: created_Date and updated_Date are auto-set by system
    # Note: status is auto-set to 'pending' if not provided

    userId: str = Field(..., max_length=255, description="Email address (required, must be valid format and unique)")

    @field_validator('userId')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """
        Validate email format using RFC 5322 regex pattern
        Pattern: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$
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
        Valid: pending, active, rejected
        """
        allowed_statuses = {'pending', 'active', 'rejected'}
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


class UserRequestUpdate(BaseModel):
    """Schema for updating a user request via PUT request"""
    # Note: requestId is immutable (cannot be updated)
    # Note: userId is immutable (cannot be updated)
    # Note: created_Date is immutable (cannot be updated)
    # Note: updated_Date is auto-updated by system
    # Note: status is REQUIRED for all updates

    status: str = Field(..., max_length=50, description="Request status (REQUIRED: pending, active, or rejected)")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """
        Validate status is one of the allowed values
        Valid: pending, active, rejected
        """
        allowed_statuses = {'pending', 'active', 'rejected'}
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v.lower()


class UserRequestResponse(UserRequestBase):
    """Schema for API response containing all user request fields"""
    requestId: str = Field(..., description="Unique request identifier")
    userId: str = Field(..., description="Email address (user identifier)")
    created_Date: datetime = Field(..., description="Record creation timestamp (immutable)")
    updated_Date: datetime = Field(..., description="Last update timestamp (auto-updated)")

    class Config:
        from_attributes = True  # Allow population from ORM models


class UserRequestSearchResponse(BaseModel):
    """Schema for search response (GET by status)"""
    data: Optional[List[UserRequestResponse]] = Field(None, description="List of user requests matching criteria")
    existsFlag: bool = Field(..., description="True if any requests found, False otherwise")

    class Config:
        from_attributes = True


class UserRequestCreateResponse(BaseModel):
    """Schema for create response (POST success)"""
    message: str = Field("User request created successfully", description="Success message")
    data: UserRequestResponse = Field(..., description="Created user request data")


class UserRequestUpdateResponse(BaseModel):
    """Schema for update response (PUT success)"""
    message: str = Field("User request updated successfully", description="Success message")
    data: UserRequestResponse = Field(..., description="Updated user request data")


class UserRequestListResponse(BaseModel):
    """Schema for list response containing multiple user requests"""
    data: List[UserRequestResponse] = Field(..., description="List of user requests")
    existsFlag: bool = Field(..., description="True if any requests found")

    class Config:
        from_attributes = True
