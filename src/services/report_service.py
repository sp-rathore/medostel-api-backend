"""
Service layer for Report_History table (APIs 11 & 12)
Business logic for medical report management
"""

import logging
from typing import List, Optional, Any
import json

logger = logging.getLogger(__name__)


class ReportService:
    """Service class for Report_History operations"""

    @staticmethod
    async def get_all_reports(
        db,
        status: Optional[str] = None,
        report_type: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Retrieve all reports with filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM report_history WHERE 1=1"
            params = []

            if status:
                query += " AND status = %s"
                params.append(status)

            if report_type:
                query += " AND reportType = %s"
                params.append(report_type)

            if user_id:
                query += " AND userId = %s"
                params.append(user_id)

            query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            reports = cursor.fetchall()
            return reports or []
        except Exception as e:
            logger.error(f"Error retrieving reports: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_report(db, report_data: dict) -> Any:
        """Create new report record"""
        cursor = db.cursor()
        try:
            json_data = None
            if 'jsonData' in report_data and report_data['jsonData']:
                json_data = json.dumps(report_data['jsonData'])

            query = """
                INSERT INTO report_history
                (id, userId, fileName, fileType, reportType, status,
                 inferredDiagnosis, pdfUrl, bucketLocation, jsonData,
                 timestamp, createdDate, updatedDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING *
            """
            cursor.execute(query, (
                report_data['id'],
                report_data['userId'],
                report_data['fileName'],
                report_data['fileType'],
                report_data.get('reportType'),
                report_data.get('status', 'Pending'),
                report_data.get('inferredDiagnosis'),
                report_data.get('pdfUrl'),
                report_data.get('bucketLocation'),
                json_data
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Report created: {report_data['id']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating report: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_report(db, report_id: str, report_data: dict) -> Any:
        """Update report record"""
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if 'status' in report_data:
                updates.append("status = %s")
                params.append(report_data['status'])

            if 'inferredDiagnosis' in report_data:
                updates.append("inferredDiagnosis = %s")
                params.append(report_data['inferredDiagnosis'])

            if 'jsonData' in report_data:
                json_data = json.dumps(report_data['jsonData']) if report_data['jsonData'] else None
                updates.append("jsonData = %s")
                params.append(json_data)

            if 'pdfUrl' in report_data:
                updates.append("pdfUrl = %s")
                params.append(report_data['pdfUrl'])

            if not updates:
                return await ReportService.get_report_by_id(db, report_id)

            query = "UPDATE report_history SET "
            query += ", ".join(updates) + ", updatedDate = CURRENT_TIMESTAMP"
            query += " WHERE id = %s RETURNING *"
            params.append(report_id)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Report updated: {report_id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating report: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_report(db, report_id: str) -> bool:
        """Delete report record"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM report_history WHERE id = %s"
            cursor.execute(query, (report_id,))
            db.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Report deleted: {report_id}")
            return deleted
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting report: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_report_by_id(db, report_id: str) -> Any:
        """Get report by ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM report_history WHERE id = %s"
            cursor.execute(query, (report_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    async def get_user_reports(db, user_id: str, limit: int = 100, offset: int = 0) -> List[Any]:
        """Get all reports for a specific user"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM report_history WHERE userId = %s ORDER BY timestamp DESC LIMIT %s OFFSET %s"
            cursor.execute(query, (user_id, limit, offset))
            reports = cursor.fetchall()
            return reports or []
        finally:
            cursor.close()
