"""
Pydantic schemas for State_City_PinCode_Master (APIs 1, 2, & 3)
Updated: March 2, 2026 - Changed to numeric data types
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    """Base schema for geographic location with numeric fields"""
    stateId: int = Field(..., gt=0, description="State Identifier (numeric)")
    stateName: str = Field(..., max_length=100, description="Name of the State")
    cityId: int = Field(..., gt=0, description="City Identifier (numeric)")
    cityName: str = Field(..., max_length=100, description="Name of the City")
    pinCode: int = Field(..., ge=100000, le=999999, description="Postal Code (5-6 digits for India)")
    countryName: str = Field(default="India", max_length=50, description="Country Name")
    status: str = Field(default="Active", max_length=20, description="Location status (Active/Inactive)")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in ['Active', 'Inactive']:
            raise ValueError("Status must be 'Active' or 'Inactive'")
        return v


class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    # All fields from LocationBase are required
    pass


class LocationUpdate(BaseModel):
    """Schema for updating a location (pinCode is immutable)"""
    status: Optional[str] = Field(None, max_length=20, description="Updated status (Active/Inactive)")
    countryName: Optional[str] = Field(None, max_length=50, description="Updated country name")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ['Active', 'Inactive']:
            raise ValueError("Status must be 'Active' or 'Inactive'")
        return v


class LocationResponse(LocationBase):
    """Schema for location response"""
    createdDate: datetime
    updatedDate: datetime

    class Config:
        from_attributes = True
