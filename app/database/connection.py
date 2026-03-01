"""
Database connection management and connection pooling
"""

import logging
from psycopg2.pool import SimpleConnectionPool
from app.config import settings

logger = logging.getLogger(__name__)

# Global connection pool
db_pool = None


def init_db_pool():
    """Initialize database connection pool"""
    global db_pool
    try:
        db_pool = SimpleConnectionPool(
            settings.DB_POOL_SIZE,
            settings.DB_POOL_SIZE + settings.DB_POOL_MAX_OVERFLOW,
            settings.DATABASE_URL,
            timeout=settings.DB_POOL_TIMEOUT
        )
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database connection pool: {e}")
        raise


def get_db():
    """
    Database dependency for FastAPI endpoints.
    Yields a database connection from the pool.
    """
    if db_pool is None:
        raise RuntimeError("Database pool not initialized. Call init_db_pool() first.")

    conn = db_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db_pool.putconn(conn)


def close_db():
    """Close all database connections in the pool"""
    global db_pool
    if db_pool:
        try:
            db_pool.closeall()
            logger.info("Database connection pool closed")
        except Exception as e:
            logger.error(f"Error closing database pool: {e}")
        finally:
            db_pool = None
