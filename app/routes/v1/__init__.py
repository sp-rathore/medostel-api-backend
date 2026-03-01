"""
API v1 routes module
Exports all route handlers for API endpoints
"""

from app.routes.v1.roles import router as roles_router
from app.routes.v1.locations import router as locations_router
from app.routes.v1.users import router as users_router
from app.routes.v1.auth import router as auth_router
from app.routes.v1.registrations import router as registrations_router
from app.routes.v1.reports import router as reports_router

__all__ = [
    "roles_router",
    "locations_router",
    "users_router",
    "auth_router",
    "registrations_router",
    "reports_router",
]
