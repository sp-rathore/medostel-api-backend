"""
API v1 routes module
Exports all route handlers for API endpoints
"""

try:
    from src.routes.v1.roles import router as roles_router
except ImportError:
    roles_router = None

try:
    from src.routes.v1.locations import router as locations_router
except ImportError:
    locations_router = None

try:
    from src.routes.v1.users import router as users_router
except ImportError:
    users_router = None

try:
    from src.routes.v1.auth import router as auth_router
except ImportError:
    auth_router = None

try:
    from src.routes.v1.registrations import router as registrations_router
except ImportError:
    registrations_router = None

try:
    from src.routes.v1.reports import router as reports_router
except ImportError:
    reports_router = None

try:
    from src.routes.v1.user_request import router as user_request_router
except ImportError:
    user_request_router = None

__all__ = [
    "roles_router",
    "locations_router",
    "users_router",
    "auth_router",
    "registrations_router",
    "reports_router",
    "user_request_router",
]
