"""
Pydantic schemas for User_Role_Master (APIs 1 & 2)
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class UserRoleBase(BaseModel):
    """Base schema for user role"""
    roleId: str = Field(..., max_length=10)
    roleName: str = Field(..., max_length=50)
    status: str = Field(default="Active")
    comments: Optional[str] = Field(None, max_length=250)


class UserRoleCreate(UserRoleBase):
    """Schema for creating a new user role"""
    pass


class UserRoleUpdate(BaseModel):
    """Schema for updating a user role"""
    status: Optional[str] = None
    comments: Optional[str] = None


class UserRoleResponse(UserRoleBase):
    """Schema for user role response"""
    createdDate: date
    updatedDate: date

    class Config:
        from_attributes = True
