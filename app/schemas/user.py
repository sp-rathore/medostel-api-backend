"""
Pydantic schemas for User_Master (APIs 5 & 6)
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for user"""
    firstName: str = Field(..., max_length=50)
    lastName: str = Field(..., max_length=50)
    currentRole: str = Field(..., max_length=50)
    emailId: EmailStr
    mobileNumber: str = Field(..., max_length=15)
    organisation: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="Active", max_length=20)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    userId: str = Field(..., max_length=100)
    address1: Optional[str] = Field(None, max_length=255)
    address2: Optional[str] = Field(None, max_length=255)
    stateName: Optional[str] = Field(None, max_length=100)
    cityName: Optional[str] = Field(None, max_length=100)
    pinCode: Optional[str] = Field(None, max_length=10)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    organisation: Optional[str] = None
    status: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    stateName: Optional[str] = None
    cityName: Optional[str] = None
    pinCode: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    userId: str
    address1: Optional[str]
    address2: Optional[str]
    stateName: Optional[str]
    cityName: Optional[str]
    pinCode: Optional[str]
    createdDate: datetime

    class Config:
        from_attributes = True
