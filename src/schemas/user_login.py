"""
Pydantic schemas for User_Login (APIs 7 & 8)
Updated: March 3, 2026 - roleId changed from str to INTEGER (FK to user_role_master.roleId)
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserLoginBase(BaseModel):
    """Base schema for user login"""
    username: str = Field(..., max_length=100)
    roleId: Optional[int] = Field(None, ge=1, le=8, description="Role ID (1-8, FK to user_role_master)")
    isActive: bool = Field(default=True)


class UserLoginCreate(UserLoginBase):
    """Schema for creating user login credentials"""
    userId: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    mobilePhone: Optional[str] = Field(None, max_length=15)


class UserLoginUpdate(BaseModel):
    """Schema for updating user login credentials"""
    password: Optional[str] = Field(None, min_length=8)
    isActive: Optional[bool] = None
    roleId: Optional[int] = Field(None, ge=1, le=8, description="Role ID (1-8, FK to user_role_master)")


class UserLoginResponse(UserLoginBase):
    """Schema for user login response"""
    userId: str
    mobilePhone: Optional[str]
    lastLoginAt: Optional[datetime] = None
    passwordLastChangedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
