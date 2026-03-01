"""
Common Pydantic models for all API responses
"""

from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class APIResponse(BaseModel):
    """Standard API response model for successful operations"""
    status: str  # "success" or "error"
    code: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime


class ErrorResponse(APIResponse):
    """Error response model"""
    status: str = "error"
    data: Optional[Any] = None


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    limit: int = 100
    offset: int = 0
