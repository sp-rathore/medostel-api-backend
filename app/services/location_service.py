"""
Service layer for State_City_PinCode_Master table (APIs 1, 2, & 3)
Business logic for geographic location management
Updated: March 2, 2026 - Changed to numeric data types, pinCode as PK
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
        state_id: Optional[int] = None,
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
                (pinCode, stateId, stateName, cityId, cityName, countryName, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """
            cursor.execute(query, (
                location_data['pinCode'],
                location_data['stateId'],
                location_data['stateName'],
                location_data['cityId'],
                location_data['cityName'],
                location_data.get('countryName', 'India'),
                location_data.get('status', 'Active')
            ))
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Location created: {location_data['cityName']}, {location_data['stateName']}, {location_data['pinCode']}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating location: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def update_location(db, pin_code: int, location_data: dict) -> Any:
        """Update existing location by pinCode"""
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
                return await LocationService.get_location_by_pincode(db, pin_code)

            query = "UPDATE state_city_pincode_master SET "
            query += ", ".join(updates) + ", updatedDate = CURRENT_TIMESTAMP"
            query += " WHERE pinCode = %s RETURNING *"
            params.append(pin_code)

            cursor.execute(query, params)
            db.commit()
            result = cursor.fetchone()
            logger.info(f"Location updated: PinCode {pin_code}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating location: {e}")
            raise
        finally:
            cursor.close()

    @staticmethod
    async def get_location_by_pincode(db, pin_code: int) -> Any:
        """Get location by pinCode (primary key)"""
        cursor = db.cursor()
        try:
            query = "SELECT * FROM state_city_pincode_master WHERE pinCode = %s"
            cursor.execute(query, (pin_code,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    async def get_pincodes_by_city(
        db,
        city_id: Optional[int] = None,
        city_name: Optional[str] = None
    ) -> List[Any]:
        """Get all pinCodes for a specific city (by ID or name)"""
        cursor = db.cursor()
        try:
            if not city_id and not city_name:
                raise ValueError("Either city_id or city_name must be provided")

            query = "SELECT DISTINCT pinCode FROM state_city_pincode_master WHERE 1=1"
            params = []

            if city_id:
                query += " AND cityId = %s"
                params.append(city_id)

            if city_name:
                query += " AND cityName = %s"
                params.append(city_name)

            query += " ORDER BY pinCode"
            cursor.execute(query, params)
            pincodes = cursor.fetchall()
            return pincodes or []
        except Exception as e:
            logger.error(f"Error retrieving pinCodes for city: {e}")
            raise
        finally:
            cursor.close()
