"""
Pydantic schemas for User_Role_Master (APIs 1 & 2)
Updated: March 3, 2026 - roleId changed from VARCHAR(10) to SERIAL INTEGER
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class UserRoleCreate(BaseModel):
    """Schema for creating a new user role (roleId is auto-generated)"""
    roleName: str = Field(..., max_length=50, description="Role name (must be unique)")
    status: str = Field(default="Active", description="Role status: Active, Inactive, Closed, or Pending")
    comments: Optional[str] = Field(None, max_length=250, description="Optional comments about the role")


class UserRoleUpdate(BaseModel):
    """Schema for updating a user role"""
    status: Optional[str] = Field(None, description="Role status: Active, Inactive, Closed, or Pending")
    comments: Optional[str] = Field(None, max_length=250, description="Optional comments about the role")


class UserRoleResponse(BaseModel):
    """Schema for user role response (includes auto-generated roleId)"""
    roleId: int = Field(..., ge=1, description="Unique role identifier (auto-generated)")
    roleName: str = Field(..., max_length=50, description="Role name")
    status: str = Field(..., description="Role status: Active, Inactive, Closed, or Pending")
    comments: Optional[str] = Field(None, max_length=250, description="Comments about the role")
    createdDate: date = Field(..., description="Date when role was created")
    updatedDate: date = Field(..., description="Date when role was last updated")

    class Config:
        from_attributes = True
