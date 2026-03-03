"""
Pydantic schemas for New_User_Request (APIs 9 & 10)
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegistrationBase(BaseModel):
    """Base schema for registration request"""
    userName: str = Field(..., max_length=100)
    firstName: str = Field(..., max_length=50)
    lastName: str = Field(..., max_length=50)
    currentRole: str = Field(..., max_length=50)
    emailId: EmailStr
    mobileNumber: str = Field(..., max_length=15)
    requestStatus: str = Field(default="Pending", max_length=20)


class RegistrationCreate(RegistrationBase):
    """Schema for creating a registration request"""
    requestId: str = Field(..., max_length=20)
    organisation: Optional[str] = Field(None, max_length=100)
    address1: Optional[str] = Field(None, max_length=255)
    address2: Optional[str] = Field(None, max_length=255)
    stateName: Optional[str] = Field(None, max_length=100)
    cityName: Optional[str] = Field(None, max_length=100)
    pinCode: Optional[str] = Field(None, max_length=10)


class RegistrationUpdate(BaseModel):
    """Schema for updating a registration request"""
    requestStatus: Optional[str] = None
    approvedBy: Optional[str] = Field(None, max_length=100)
    approvalRemarks: Optional[str] = None


class RegistrationResponse(RegistrationBase):
    """Schema for registration response"""
    requestId: str
    organisation: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    stateName: Optional[str]
    cityName: Optional[str]
    pinCode: Optional[str]
    createdDate: datetime
    approvedBy: Optional[str] = None
    approvalRemarks: Optional[str] = None

    class Config:
        from_attributes = True
