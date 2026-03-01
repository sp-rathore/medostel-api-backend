"""
Service layer for User_Master table (APIs 5 & 6)
Business logic for user profile management
"""

import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


class UserService:
    """Service class for User_Master operations"""

    @staticmethod
    async def get_all_users(
        db,
        status: Optional[str] = None,
        current_role: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Retrieve all user profiles with filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_master WHERE 1=1"
            params = []

            if status:
                query += " AND status = %s"
                params.append(status)

            if current_role:
                query += " AND currentRole = %s"
                params.append(current_role)

            query += " ORDER BY createdDate DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            users = cursor.fetchall()
            return users or []
        except Exception as e:
            logger.error(f"Error retrieving users: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_user(db, user_data: dict) -> Any:
        """Create new user profile"""
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO user_master
                (userId, firstName, lastName, currentRole, organisation, emailId, mobileNumber,
                 address1, address2, stateName, cityName, pinCode, status, createdDate, updatedDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING *
            """
            cursor.execute(query, (
                user_data['userId'],
                user_data['firstName'],
                user_data['lastName'],
                user_data['currentRole'],
                user_data.get('organisation'),
                user_data['emailId'],
                user_data['mobileNumber'],
                user_data.get('address1'),
                user_data.get('address2'),
                user_data.get('stateName'),
                user_data.get('cityName'),
                user_data.get('pinCode'),
                user_data.get('status', 'Active')
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"User created: {user_data['userId']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_user(db, user_id: str, user_data: dict) -> Any:
        """Update existing user profile"""
        cursor = db.cursor()
        try:
            updates = []
            params = []

            fields = ['firstName', 'lastName', 'organisation', 'status', 'address1', 'address2',
                     'stateName', 'cityName', 'pinCode']

            for field in fields:
                if field in user_data:
                    updates.append(f"{field} = %s")
                    params.append(user_data[field])

            if not updates:
                return await UserService.get_user_by_id(db, user_id)

            query = "UPDATE user_master SET "
            query += ", ".join(updates) + ", updatedDate = CURRENT_TIMESTAMP"
            query += " WHERE userId = %s RETURNING *"
            params.append(user_id)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"User updated: {user_id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_user(db, user_id: str) -> bool:
        """Delete user profile"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM user_master WHERE userId = %s"
            cursor.execute(query, (user_id,))
            db.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"User deleted: {user_id}")
            return deleted
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_user_by_id(db, user_id: str) -> Any:
        """Get user by ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_master WHERE userId = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    async def user_exists(db, user_id: str) -> bool:
        """Check if user exists"""
        user = await UserService.get_user_by_id(db, user_id)
        return user is not None
