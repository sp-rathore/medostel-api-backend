"""
Database utilities for new_user_request table
Phase 2.2: Database Utilities & Helpers
Date: March 3, 2026

Functions:
- get_next_request_id(): Auto-increment request ID (max + 1)
- get_by_request_id(request_id): Fetch request by requestId
- get_by_status(status): Fetch all requests by status
- request_id_exists(request_id): Check if requestId exists
- email_exists_in_pending(email): Check if email exists in pending/active requests
- create_user_request(db, request_data): Create new request
- update_status(db, request_id, new_status): Update request status
- Validation helpers: city_exists, district_exists, pincode_exists, state_exists, role_exists
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging
import re

logger = logging.getLogger(__name__)


class UserRequestUtils:
    """Utility class for new_user_request database operations"""

    @staticmethod
    def get_next_request_id(db: Session) -> str:
        """
        Generate next request ID by finding max(requestId) and incrementing by 1

        Pattern: If max requestId is "REQ_001", next would be "REQ_002"
        If table is empty, start from "REQ_001"

        Args:
            db: SQLAlchemy database session

        Returns:
            Next request ID as string (format: REQ_XXX)

        Raises:
            Exception: If unable to generate request ID
        """
        try:
            # Import here to avoid circular imports
            from src.db.models import NewUserRequest

            # Get the maximum requestId
            max_request_id = db.query(func.max(NewUserRequest.requestId)).scalar()

            if max_request_id is None:
                # Table is empty, start from REQ_001
                return "REQ_001"

            # Try to extract numeric portion and increment
            try:
                # If requestId is in format "REQ_XXX"
                import re
                match = re.search(r'(\d+)', max_request_id)
                if match:
                    numeric_str = match.group(1)
                    numeric_part = int(numeric_str)
                    prefix = max_request_id[:match.start()]
                    suffix = max_request_id[match.end():]
                    # Preserve the zero-padding of the original numeric part
                    next_number = str(numeric_part + 1).zfill(len(numeric_str))
                    return f"{prefix}{next_number}{suffix}"
                else:
                    # Fallback if no numeric part found
                    logger.warning(f"Unable to parse requestId format: {max_request_id}")
                    return f"REQ_{int(max_request_id) + 1}"
            except (ValueError, AttributeError) as e:
                logger.error(f"Error parsing requestId: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"Error generating next request ID: {str(e)}")
            raise

    @staticmethod
    def get_by_request_id(db: Session, request_id: str) -> Optional[Any]:
        """
        Fetch user request by requestId

        Args:
            db: SQLAlchemy database session
            request_id: Request ID to search for

        Returns:
            UserRequest object if found, None otherwise
        """
        try:
            from src.db.models import NewUserRequest

            request = db.query(NewUserRequest).filter(
                NewUserRequest.requestId == request_id
            ).first()

            return request
        except Exception as e:
            logger.error(f"Error fetching request by ID {request_id}: {str(e)}")
            raise

    @staticmethod
    def get_by_status(db: Session, status: str) -> List[Any]:
        """
        Fetch all user requests with given status

        Args:
            db: SQLAlchemy database session
            status: Status to filter by (pending, active, rejected)

        Returns:
            List of UserRequest objects matching status
        """
        try:
            from src.db.models import NewUserRequest

            requests = db.query(NewUserRequest).filter(
                NewUserRequest.status == status.lower()
            ).all()

            return requests
        except Exception as e:
            logger.error(f"Error fetching requests by status {status}: {str(e)}")
            raise

    @staticmethod
    def request_id_exists(db: Session, request_id: str) -> bool:
        """
        Check if requestId already exists

        Args:
            db: SQLAlchemy database session
            request_id: Request ID to check

        Returns:
            True if request exists, False otherwise
        """
        try:
            from src.db.models import NewUserRequest

            exists = db.query(
                db.query(NewUserRequest).filter(
                    NewUserRequest.requestId == request_id
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if request ID exists {request_id}: {str(e)}")
            raise

    @staticmethod
    def email_exists_in_pending(db: Session, email: str) -> bool:
        """
        Check if email already exists in pending or active requests

        Args:
            db: SQLAlchemy database session
            email: Email address to check

        Returns:
            True if email exists in pending/active, False otherwise
        """
        try:
            from src.db.models import NewUserRequest

            exists = db.query(
                db.query(NewUserRequest).filter(
                    func.lower(NewUserRequest.userId) == email.lower(),
                    NewUserRequest.status.in_(['pending', 'active'])
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if email exists in pending {email}: {str(e)}")
            raise

    @staticmethod
    def city_exists(db: Session, city_name: str) -> bool:
        """
        Check if city exists in state_city_pincode_master

        Args:
            db: SQLAlchemy database session
            city_name: City name to validate

        Returns:
            True if city exists, False otherwise
        """
        try:
            from src.db.models import StateCityPincodeMaster

            exists = db.query(
                db.query(StateCityPincodeMaster).filter(
                    func.lower(StateCityPincodeMaster.cityName) == city_name.lower()
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if city exists {city_name}: {str(e)}")
            raise

    @staticmethod
    def district_exists(db: Session, district_name: str) -> bool:
        """
        Check if district exists in state_city_pincode_master
        Note: Checking districtId instead as districtName may not be direct column

        Args:
            db: SQLAlchemy database session
            district_name: District name/id to validate

        Returns:
            True if district exists, False otherwise
        """
        try:
            from src.db.models import StateCityPincodeMaster

            # Check if any record has this district_name (implementation may vary)
            exists = db.query(
                db.query(StateCityPincodeMaster).filter(
                    func.lower(StateCityPincodeMaster.cityId) == district_name.lower()
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if district exists {district_name}: {str(e)}")
            raise

    @staticmethod
    def pincode_exists(db: Session, pincode: str) -> bool:
        """
        Check if pincode exists in state_city_pincode_master

        Args:
            db: SQLAlchemy database session
            pincode: PIN code to validate

        Returns:
            True if pincode exists, False otherwise
        """
        try:
            from src.db.models import StateCityPincodeMaster

            exists = db.query(
                db.query(StateCityPincodeMaster).filter(
                    StateCityPincodeMaster.pinCode == pincode
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if pincode exists {pincode}: {str(e)}")
            raise

    @staticmethod
    def state_exists(db: Session, state_name: str) -> bool:
        """
        Check if state exists in state_city_pincode_master

        Args:
            db: SQLAlchemy database session
            state_name: State name to validate

        Returns:
            True if state exists, False otherwise
        """
        try:
            from src.db.models import StateCityPincodeMaster

            exists = db.query(
                db.query(StateCityPincodeMaster).filter(
                    func.lower(StateCityPincodeMaster.stateName) == state_name.lower()
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if state exists {state_name}: {str(e)}")
            raise

    @staticmethod
    def role_exists(db: Session, role_name: str) -> bool:
        """
        Check if role exists in user_role_master

        Args:
            db: SQLAlchemy database session
            role_name: Role name to validate

        Returns:
            True if role exists, False otherwise
        """
        try:
            from src.db.models import UserRoleMaster

            exists = db.query(
                db.query(UserRoleMaster).filter(
                    func.lower(UserRoleMaster.roleName) == role_name.lower()
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if role exists {role_name}: {str(e)}")
            raise

    @staticmethod
    def create_user_request(db: Session, request_data: Dict[str, Any]) -> Any:
        """
        Create new user request with validations

        Args:
            db: SQLAlchemy database session
            request_data: Dictionary containing request fields

        Returns:
            Created NewUserRequest object

        Raises:
            ValueError: If validation fails
            Exception: For database errors
        """
        try:
            from src.db.models import NewUserRequest

            # Validate email is unique (not in pending/active)
            if UserRequestUtils.email_exists_in_pending(db, request_data['userId']):
                raise ValueError(f"Email already has a pending or active request: {request_data['userId']}")

            # Validate role exists
            if not UserRequestUtils.role_exists(db, request_data['currentRole']):
                raise ValueError(f"Role does not exist: {request_data['currentRole']}")

            # Validate location references if provided
            if request_data.get('city_name'):
                if not UserRequestUtils.city_exists(db, request_data['city_name']):
                    raise ValueError(f"City does not exist: {request_data['city_name']}")

            if request_data.get('pincode'):
                if not UserRequestUtils.pincode_exists(db, request_data['pincode']):
                    raise ValueError(f"Pincode does not exist: {request_data['pincode']}")

            if request_data.get('state_name'):
                if not UserRequestUtils.state_exists(db, request_data['state_name']):
                    raise ValueError(f"State does not exist: {request_data['state_name']}")

            # Generate requestId
            request_id = UserRequestUtils.get_next_request_id(db)

            # Create new request object
            new_request = NewUserRequest(
                requestId=request_id,
                userId=request_data['userId'].lower(),  # Normalize email to lowercase
                firstName=request_data['firstName'],
                lastName=request_data['lastName'],
                mobileNumber=request_data['mobileNumber'],
                organization=request_data.get('organization'),
                currentRole=request_data['currentRole'].upper(),
                status=request_data.get('status', 'pending').lower(),
                city_name=request_data.get('city_name'),
                district_name=request_data.get('district_name'),
                pincode=request_data.get('pincode'),
                state_name=request_data.get('state_name'),
                created_Date=datetime.utcnow(),
                updated_Date=datetime.utcnow()
            )

            # Add and commit
            db.add(new_request)
            db.commit()
            db.refresh(new_request)

            logger.info(f"Created user request with ID: {request_id}")
            return new_request

        except ValueError as e:
            db.rollback()
            logger.error(f"Validation error creating request: {str(e)}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user request: {str(e)}")
            raise

    @staticmethod
    def update_status(db: Session, request_id: str, new_status: str) -> Any:
        """
        Update request status to active or rejected

        Args:
            db: SQLAlchemy database session
            request_id: Request ID to update
            new_status: New status (active, rejected, or pending)

        Returns:
            Updated NewUserRequest object

        Raises:
            ValueError: If request not found or invalid status
            Exception: For database errors
        """
        try:
            from src.db.models import NewUserRequest

            # Validate status value
            allowed_statuses = {'pending', 'active', 'rejected'}
            if new_status.lower() not in allowed_statuses:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(allowed_statuses)}")

            # Get the request
            request = db.query(NewUserRequest).filter(
                NewUserRequest.requestId == request_id
            ).first()

            if not request:
                raise ValueError(f"Request not found: {request_id}")

            # Update status and timestamp
            request.status = new_status.lower()
            request.updated_Date = datetime.utcnow()

            db.commit()
            db.refresh(request)

            logger.info(f"Updated request {request_id} status to {new_status}")
            return request

        except ValueError as e:
            db.rollback()
            logger.error(f"Validation error updating status: {str(e)}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating request status: {str(e)}")
            raise


# Create singleton instance for module-level access
user_request_db = UserRequestUtils()
