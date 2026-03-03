"""
Schemas package - Pydantic models for request/response validation
"""

from app.schemas.common import APIResponse, ErrorResponse, PaginationParams
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate, UserRoleResponse
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.user_login import UserLoginCreate, UserLoginUpdate, UserLoginResponse
from app.schemas.registration import RegistrationCreate, RegistrationUpdate, RegistrationResponse
from app.schemas.report import ReportCreate, ReportUpdate, ReportResponse

__all__ = [
    "APIResponse",
    "ErrorResponse",
    "PaginationParams",
    "UserRoleCreate",
    "UserRoleUpdate",
    "UserRoleResponse",
    "LocationCreate",
    "LocationUpdate",
    "LocationResponse",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLoginCreate",
    "UserLoginUpdate",
    "UserLoginResponse",
    "RegistrationCreate",
    "RegistrationUpdate",
    "RegistrationResponse",
    "ReportCreate",
    "ReportUpdate",
    "ReportResponse",
]
