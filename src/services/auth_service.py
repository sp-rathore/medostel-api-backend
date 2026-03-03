"""
Service layer for User_Login table (APIs 7 & 8)
Business logic for authentication and login credentials
"""

import logging
from typing import List, Optional, Any
import hashlib

logger = logging.getLogger(__name__)


class AuthService:
    """Service class for User_Login operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    async def get_all_login_records(
        db,
        is_active: Optional[bool] = None,
        role_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Retrieve all user login records with filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_login WHERE 1=1"
            params = []

            if is_active is not None:
                query += " AND isActive = %s"
                params.append(is_active)

            if role_id:
                query += " AND roleId = %s"
                params.append(role_id)

            query += " ORDER BY createdAt DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            records = cursor.fetchall()
            return records or []
        except Exception as e:
            logger.error(f"Error retrieving login records: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_login(db, login_data: dict) -> Any:
        """Create new user login credentials"""
        cursor = db.cursor()
        try:
            password_hash = AuthService.hash_password(login_data['password'])

            query = """
                INSERT INTO user_login
                (userId, username, passwordHash, mobilePhone, roleId, isActive,
                 createdAt, updatedAt, lastLoginAt, passwordLastChangedAt)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP)
                RETURNING userId, username, isActive, createdAt
            """
            cursor.execute(query, (
                login_data['userId'],
                login_data['username'],
                password_hash,
                login_data.get('mobilePhone'),
                login_data.get('roleId'),
                True
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Login credentials created for: {login_data['userId']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating login credentials: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_login(db, user_id: str, login_data: dict) -> Any:
        """Update user login credentials"""
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if 'password' in login_data:
                updates.append("passwordHash = %s")
                params.append(AuthService.hash_password(login_data['password']))
                updates.append("passwordLastChangedAt = CURRENT_TIMESTAMP")

            if 'isActive' in login_data:
                updates.append("isActive = %s")
                params.append(login_data['isActive'])

            if 'roleId' in login_data:
                updates.append("roleId = %s")
                params.append(login_data['roleId'])

            if not updates:
                return await AuthService.get_login_by_id(db, user_id)

            query = "UPDATE user_login SET "
            query += ", ".join(updates) + ", updatedAt = CURRENT_TIMESTAMP"
            query += " WHERE userId = %s RETURNING *"
            params.append(user_id)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Login credentials updated: {user_id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating login credentials: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_login(db, user_id: str) -> bool:
        """Delete user login credentials"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM user_login WHERE userId = %s"
            cursor.execute(query, (user_id,))
            db.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Login credentials deleted: {user_id}")
            return deleted
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting login credentials: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_login_by_id(db, user_id: str) -> Any:
        """Get login record by user ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_login WHERE userId = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    async def verify_password(db, user_id: str, password: str) -> bool:
        """Verify user password"""
        login = await AuthService.get_login_by_id(db, user_id)
        if not login:
            return False

        password_hash = AuthService.hash_password(password)
        return login[2] == password_hash  # Column 2 is passwordHash
