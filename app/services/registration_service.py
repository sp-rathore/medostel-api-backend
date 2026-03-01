"""
Service layer for New_User_Request table (APIs 9 & 10)
Business logic for user registration request management
"""

import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


class RegistrationService:
    """Service class for New_User_Request operations"""

    @staticmethod
    async def get_all_requests(
        db,
        request_status: Optional[str] = None,
        current_role: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Retrieve all registration requests with filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM new_user_request WHERE 1=1"
            params = []

            if request_status:
                query += " AND requestStatus = %s"
                params.append(request_status)

            if current_role:
                query += " AND currentRole = %s"
                params.append(current_role)

            query += " ORDER BY createdDate DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            requests = cursor.fetchall()
            return requests or []
        except Exception as e:
            logger.error(f"Error retrieving registration requests: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_request(db, request_data: dict) -> Any:
        """Create new registration request"""
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO new_user_request
                (requestId, userName, firstName, lastName, currentRole, organisation,
                 emailId, mobileNumber, address1, address2, stateName, cityName, pinCode,
                 requestStatus, createdDate, updatedDate, approvedBy, approvalRemarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s)
                RETURNING *
            """
            cursor.execute(query, (
                request_data['requestId'],
                request_data['userName'],
                request_data['firstName'],
                request_data['lastName'],
                request_data['currentRole'],
                request_data.get('organisation'),
                request_data['emailId'],
                request_data['mobileNumber'],
                request_data.get('address1'),
                request_data.get('address2'),
                request_data.get('stateName'),
                request_data.get('cityName'),
                request_data.get('pinCode'),
                request_data.get('requestStatus', 'Pending'),
                request_data.get('approvedBy'),
                request_data.get('approvalRemarks')
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Registration request created: {request_data['requestId']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating registration request: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_request(db, request_id: str, request_data: dict) -> Any:
        """Update registration request"""
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if 'requestStatus' in request_data:
                updates.append("requestStatus = %s")
                params.append(request_data['requestStatus'])

            if 'approvedBy' in request_data:
                updates.append("approvedBy = %s")
                params.append(request_data['approvedBy'])

            if 'approvalRemarks' in request_data:
                updates.append("approvalRemarks = %s")
                params.append(request_data['approvalRemarks'])

            if not updates:
                return await RegistrationService.get_request_by_id(db, request_id)

            query = "UPDATE new_user_request SET "
            query += ", ".join(updates) + ", updatedDate = CURRENT_TIMESTAMP"
            query += " WHERE requestId = %s RETURNING *"
            params.append(request_id)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Registration request updated: {request_id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating registration request: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_request(db, request_id: str) -> bool:
        """Delete registration request"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM new_user_request WHERE requestId = %s"
            cursor.execute(query, (request_id,))
            db.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Registration request deleted: {request_id}")
            return deleted
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting registration request: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_request_by_id(db, request_id: str) -> Any:
        """Get registration request by ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM new_user_request WHERE requestId = %s"
            cursor.execute(query, (request_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    async def approve_request(db, request_id: str, approved_by: str, remarks: str = "") -> Any:
        """Approve registration request"""
        return await RegistrationService.update_request(
            db,
            request_id,
            {
                'requestStatus': 'Approved',
                'approvedBy': approved_by,
                'approvalRemarks': remarks
            }
        )

    @staticmethod
    async def reject_request(db, request_id: str, approved_by: str, remarks: str = "") -> Any:
        """Reject registration request"""
        return await RegistrationService.update_request(
            db,
            request_id,
            {
                'requestStatus': 'Rejected',
                'approvedBy': approved_by,
                'approvalRemarks': remarks
            }
        )
