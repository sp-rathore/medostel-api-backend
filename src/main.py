"""
Medostel API Backend - Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.database import init_db_pool, close_db
from app.routes.v1 import (
    roles_router,
    locations_router,
    users_router,
    auth_router,
    registrations_router,
    reports_router,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events"""
    # Startup
    logger.info("Medostel API Starting...")
    try:
        init_db_pool()
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database pool: {e}")
        raise

    yield

    # Shutdown
    logger.info("Medostel API Shutting down...")
    try:
        close_db()
        logger.info("Database connection pool closed successfully")
    except Exception as e:
        logger.error(f"Error closing database pool: {e}")


# Create FastAPI application
app = FastAPI(
    title="Medostel Healthcare API",
    description="Healthcare AI Assistant - RESTful API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Medostel API is running",
        "version": "0.1.0"
    }


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check endpoint"""
    # In production, check database and external dependencies
    return {
        "status": "ready",
        "message": "Medostel API is ready to serve traffic"
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Medostel Healthcare API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "reports": "/api/v1/reports",
            "locations": "/api/v1/locations"
        }
    }


# Register API v1 routers
app.include_router(roles_router, prefix="/api/v1", tags=["User Roles"])
app.include_router(locations_router, prefix="/api/v1", tags=["Locations"])
app.include_router(users_router, prefix="/api/v1", tags=["Users"])
app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(registrations_router, prefix="/api/v1", tags=["User Registrations"])
app.include_router(reports_router, prefix="/api/v1", tags=["Reports"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return {
        "status": "error",
        "code": exc.status_code,
        "message": exc.detail,
        "path": str(request.url)
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "status": "error",
        "code": 500,
        "message": "Internal server error",
        "path": str(request.url)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
