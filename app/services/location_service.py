"""
Service layer for State_City_PinCode_Master table (APIs 3 & 4)
Business logic for geographic location management
"""

import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


class LocationService:
    """Service class for State_City_PinCode_Master operations"""

    @staticmethod
    async def get_all_locations(
        db,
        country: Optional[str] = None,
        state_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Retrieve all geographic locations with filtering"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM state_city_pincode_master WHERE 1=1"
            params = []

            if country:
                query += " AND countryName = %s"
                params.append(country)

            if state_id:
                query += " AND stateId = %s"
                params.append(state_id)

            if status:
                query += " AND status = %s"
                params.append(status)

            query += " ORDER BY stateName, cityName LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            locations = cursor.fetchall()
            return locations or []
        except Exception as e:
            logger.error(f"Error retrieving locations: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def create_location(db, location_data: dict) -> Any:
        """Create new geographic location"""
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO state_city_pincode_master
                (stateId, stateName, cityId, cityName, pinCode, countryName, status, createdDate, updatedDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING *
            """
            cursor.execute(query, (
                location_data['stateId'],
                location_data['stateName'],
                location_data['cityId'],
                location_data['cityName'],
                location_data['pinCode'],
                location_data.get('countryName', 'India'),
                location_data.get('status', 'Active')
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Location created: {location_data['cityName']}, {location_data['stateName']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating location: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_location(db, location_id: int, location_data: dict) -> Any:
        """Update existing location"""
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if 'status' in location_data:
                updates.append("status = %s")
                params.append(location_data['status'])

            if 'countryName' in location_data:
                updates.append("countryName = %s")
                params.append(location_data['countryName'])

            if not updates:
                return await LocationService.get_location_by_id(db, location_id)

            query = "UPDATE state_city_pincode_master SET "
            query += ", ".join(updates) + ", updatedDate = CURRENT_TIMESTAMP"
            query += " WHERE id = %s RETURNING *"
            params.append(location_id)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Location updated: {location_id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating location: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def delete_location(db, location_id: int) -> bool:
        """Delete location"""
        cursor = db.cursor()
        try:
            query = "DELETE FROM state_city_pincode_master WHERE id = %s"
            cursor.execute(query, (location_id,))
            db.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Location deleted: {location_id}")
            return deleted
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting location: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_location_by_id(db, location_id: int) -> Any:
        """Get location by ID"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM state_city_pincode_master WHERE id = %s"
            cursor.execute(query, (location_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
