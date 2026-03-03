"""
Pydantic schemas for Report_History (APIs 11 & 12)
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ReportBase(BaseModel):
    """Base schema for report"""
    userId: str = Field(..., max_length=100)
    fileName: str = Field(..., max_length=255)
    fileType: str = Field(..., max_length=10)
    reportType: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="Pending", max_length=20)


class ReportCreate(ReportBase):
    """Schema for creating a report"""
    id: str = Field(..., max_length=50)
    inferredDiagnosis: Optional[str] = None
    pdfUrl: Optional[str] = None
    bucketLocation: Optional[str] = Field(None, max_length=255)
    jsonData: Optional[Any] = None


class ReportUpdate(BaseModel):
    """Schema for updating a report"""
    status: Optional[str] = None
    inferredDiagnosis: Optional[str] = None
    jsonData: Optional[Any] = None
    pdfUrl: Optional[str] = None


class ReportResponse(ReportBase):
    """Schema for report response"""
    id: str
    timestamp: datetime
    inferredDiagnosis: Optional[str]
    pdfUrl: Optional[str]
    bucketLocation: Optional[str]
    jsonData: Optional[Any]

    class Config:
        from_attributes = True
