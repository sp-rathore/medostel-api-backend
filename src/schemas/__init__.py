"""
Schemas package - Pydantic models for request/response validation
"""

# Import user schemas
try:
    from src.schemas.user import UserCreate, UserUpdate, UserResponse
except ImportError:
    UserCreate = None
    UserUpdate = None
    UserResponse = None

# Import other schemas (optional - may not exist)
try:
    from src.schemas.user_role import UserRoleCreate, UserRoleUpdate, UserRoleResponse
except (ImportError, ModuleNotFoundError):
    pass

try:
    from src.schemas.location import LocationCreate, LocationUpdate, LocationResponse
except (ImportError, ModuleNotFoundError):
    pass

try:
    from src.schemas.user_login import UserLoginCreate, UserLoginUpdate, UserLoginResponse
except (ImportError, ModuleNotFoundError):
    pass

try:
    from src.schemas.registration import RegistrationCreate, RegistrationUpdate, RegistrationResponse
except (ImportError, ModuleNotFoundError):
    pass

try:
    from src.schemas.report import ReportCreate, ReportUpdate, ReportResponse
except (ImportError, ModuleNotFoundError):
    pass

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
