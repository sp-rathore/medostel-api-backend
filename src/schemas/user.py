"""
Pydantic schemas for User_Master (APIs 5 & 6)
Enhanced with geographic hierarchy integration (Step 1.2)
Updated: March 3, 2026 - currentRole changed from str to INTEGER (FK to user_role_master.roleId)
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for user"""
    firstName: str = Field(..., max_length=50)
    lastName: str = Field(..., max_length=50)
    currentRole: int = Field(..., ge=1, le=8, description="Role ID (1-8, FK to user_role_master)")
    emailId: EmailStr
    mobileNumber: str = Field(..., max_length=15)
    organisation: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="Active", max_length=20)


class UserCreate(UserBase):
    """Schema for creating a new user with geographic hierarchy"""
    userId: str = Field(..., max_length=100, description="User ID (Email address)")
    address1: Optional[str] = Field(None, max_length=255, description="Address line 1")
    address2: Optional[str] = Field(None, max_length=255, description="Address line 2")
    stateId: Optional[int] = Field(None, gt=0, description="State ID (FK to State_City_PinCode_Master)")
    stateName: Optional[str] = Field(None, max_length=100, description="State name (for display)")
    districtId: Optional[int] = Field(None, gt=0, description="District ID (FK to State_City_PinCode_Master)")
    cityId: Optional[int] = Field(None, gt=0, description="City ID (FK to State_City_PinCode_Master)")
    cityName: Optional[str] = Field(None, max_length=100, description="City name (for display)")
    pinCode: Optional[int] = Field(None, ge=100000, le=999999, description="Postal code (5-6 digits, FK to State_City_PinCode_Master)")

    @field_validator('stateId', 'districtId', 'cityId', 'pinCode', mode='before')
    @classmethod
    def validate_geographic_fields(cls, v):
        """Validate that geographic fields are positive integers"""
        if v is not None and not isinstance(v, int):
            raise ValueError('Geographic fields must be integers')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user (pinCode is immutable)"""
    firstName: Optional[str] = Field(None, max_length=50)
    lastName: Optional[str] = Field(None, max_length=50)
    organisation: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)
    address1: Optional[str] = Field(None, max_length=255)
    address2: Optional[str] = Field(None, max_length=255)
    stateId: Optional[int] = Field(None, gt=0, description="State ID (cannot update if not initially set)")
    stateName: Optional[str] = Field(None, max_length=100)
    districtId: Optional[int] = Field(None, gt=0, description="District ID (cannot update if not initially set)")
    cityId: Optional[int] = Field(None, gt=0, description="City ID (cannot update if not initially set)")
    cityName: Optional[str] = Field(None, max_length=100)


class UserResponse(UserBase):
    """Schema for user response with geographic hierarchy"""
    userId: str
    address1: Optional[str]
    address2: Optional[str]
    stateId: Optional[int]
    stateName: Optional[str]
    districtId: Optional[int]
    cityId: Optional[int]
    cityName: Optional[str]
    pinCode: Optional[int]
    createdDate: datetime
    updatedDate: Optional[datetime] = None

    class Config:
        from_attributes = True
