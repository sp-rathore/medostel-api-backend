"""
Service layer for User_Role_Master table (APIs 1 & 2)
Business logic for role management operations
"""

import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


class UserRoleService:
    """Service class for User_Role_Master operations"""

    @staticmethod
    async def get_all_roles(
        db,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Retrieve all user roles with optional filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_role_master WHERE 1=1"
            params = []

            if status:
                query += " AND status = %s"
                params.append(status)

            query += " ORDER BY createdDate DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            roles = cursor.fetchall()
            return roles or []
        except Exception as e:
            logger.error(f"Error retrieving roles: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_role(db, role_data: dict) -> Any:
        """Create new user role"""
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO user_role_master
                (roleId, roleName, status, createdDate, updatedDate, comments)
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_DATE, %s)
                RETURNING *
            """
            cursor.execute(query, (
                role_data['roleId'],
                role_data['roleName'],
                role_data.get('status', 'Active'),
                role_data.get('comments')
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Role created: {role_data['roleId']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_role(db, role_id: str, role_data: dict) -> Any:
        """Update existing user role"""
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if 'status' in role_data:
                updates.append("status = %s")
                params.append(role_data['status'])

            if 'comments' in role_data:
                updates.append("comments = %s")
                params.append(role_data['comments'])

            if not updates:
                # No updates provided, return existing role
                return await UserRoleService.get_role_by_id(db, role_id)

            query = "UPDATE user_role_master SET "
            query += ", ".join(updates) + ", updatedDate = CURRENT_DATE"
            query += " WHERE roleId = %s RETURNING *"
            params.append(role_id)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Role updated: {role_id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_role(db, role_id: str) -> bool:
        """Delete user role"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM user_role_master WHERE roleId = %s"
            cursor.execute(query, (role_id,))
            db.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Role deleted: {role_id}")
            return deleted
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting role: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_role_by_id(db, role_id: str) -> Any:
        """Get role by ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM user_role_master WHERE roleId = %s"
            cursor.execute(query, (role_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    async def role_exists(db, role_id: str) -> bool:
        """Check if role exists"""
        role = await UserRoleService.get_role_by_id(db, role_id)
        return role is not None
