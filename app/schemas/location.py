"""
Pydantic schemas for State_City_PinCode_Master (APIs 3 & 4)
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    """Base schema for geographic location"""
    stateId: str = Field(..., max_length=10)
    stateName: str = Field(..., max_length=100)
    cityId: str = Field(..., max_length=10)
    cityName: str = Field(..., max_length=100)
    pinCode: str = Field(..., max_length=10)
    countryName: str = Field(default="India", max_length=50)
    status: str = Field(default="Active", max_length=20)


class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating a location"""
    status: Optional[str] = None
    countryName: Optional[str] = None


class LocationResponse(LocationBase):
    """Schema for location response"""
    id: int
    createdDate: datetime
    updatedDate: datetime

    class Config:
        from_attributes = True
