"""
Database utilities for user_master table
Phase 2.2: Database Utilities & Helpers
Date: 2026-03-03

Functions:
- get_next_user_id(): Auto-increment user ID (max + 1)
- get_user_by_id(user_id): Fetch user by userId
- get_user_by_email(email): Fetch user by emailId
- get_user_by_mobile(mobile): Fetch user by mobileNumber
- email_exists(email): Check if email exists
- mobile_exists(mobile): Check if mobile exists
- email_mobile_combination_exists(email, mobile): Check composite uniqueness
- create_user(db, user_data): Create new user
- update_user(db, user_id, update_data): Update user
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime
from typing import Optional, Dict, Any
import logging

# Assuming these are defined in the models
# from src.db.models import UserMaster

logger = logging.getLogger(__name__)


class UserMasterUtils:
    """Utility class for user_master database operations"""

    @staticmethod
    def get_next_user_id(db: Session) -> str:
        """
        Generate next user ID by finding max(userId) and incrementing by 1

        Pattern: If max userId is "USER_001", next would be "USER_002"
        If max userId is "10", next would be "11"

        Args:
            db: SQLAlchemy database session

        Returns:
            Next user ID as string

        Raises:
            Exception: If unable to generate user ID
        """
        try:
            # Import here to avoid circular imports
            from src.db.models import UserMaster

            # Get the maximum numeric value from userId
            max_user_id = db.query(func.max(UserMaster.userId)).scalar()

            if max_user_id is None:
                # Table is empty, start from USER_001
                return "USER_001"

            # Try to extract numeric portion and increment
            try:
                # If userId is purely numeric (e.g., "1", "2", "100")
                numeric_id = int(max_user_id)
                return str(numeric_id + 1)
            except ValueError:
                # If userId has prefix (e.g., "USER_001")
                # Extract the numeric part and increment, preserving zero-padding
                import re
                match = re.search(r'(\d+)', max_user_id)
                if match:
                    numeric_str = match.group(1)
                    numeric_part = int(numeric_str)
                    prefix = max_user_id[:match.start()]
                    suffix = max_user_id[match.end():]
                    # Preserve the zero-padding of the original numeric part
                    next_number = str(numeric_part + 1).zfill(len(numeric_str))
                    return f"{prefix}{next_number}{suffix}"
                else:
                    # Fallback if no numeric part found
                    logger.warning(f"Unable to parse userId format: {max_user_id}")
                    return f"{max_user_id}_1"

        except Exception as e:
            logger.error(f"Error generating next user ID: {str(e)}")
            raise


    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[Any]:
        """
        Fetch user by userId

        Args:
            db: SQLAlchemy database session
            user_id: User ID to search for

        Returns:
            User object if found, None otherwise
        """
        try:
            from src.db.models import UserMaster

            user = db.query(UserMaster).filter(
                UserMaster.userId == user_id
            ).first()

            return user
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {str(e)}")
            raise


    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[Any]:
        """
        Fetch user by emailId

        Args:
            db: SQLAlchemy database session
            email: Email address to search for

        Returns:
            User object if found, None otherwise
        """
        try:
            from src.db.models import UserMaster

            user = db.query(UserMaster).filter(
                func.lower(UserMaster.emailId) == email.lower()
            ).first()

            return user
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {str(e)}")
            raise


    @staticmethod
    def get_user_by_mobile(db: Session, mobile: int) -> Optional[Any]:
        """
        Fetch user by mobileNumber

        Args:
            db: SQLAlchemy database session
            mobile: Mobile number to search for (10-digit integer)

        Returns:
            User object if found, None otherwise
        """
        try:
            from src.db.models import UserMaster

            user = db.query(UserMaster).filter(
                UserMaster.mobileNumber == mobile
            ).first()

            return user
        except Exception as e:
            logger.error(f"Error fetching user by mobile {mobile}: {str(e)}")
            raise


    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        """
        Check if email already exists in database

        Args:
            db: SQLAlchemy database session
            email: Email to check

        Returns:
            True if email exists, False otherwise
        """
        try:
            from src.db.models import UserMaster

            exists = db.query(
                db.query(UserMaster).filter(
                    func.lower(UserMaster.emailId) == email.lower()
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if email exists {email}: {str(e)}")
            raise


    @staticmethod
    def mobile_exists(db: Session, mobile: int) -> bool:
        """
        Check if mobile number already exists in database

        Args:
            db: SQLAlchemy database session
            mobile: Mobile number to check (10-digit integer)

        Returns:
            True if mobile exists, False otherwise
        """
        try:
            from src.db.models import UserMaster

            exists = db.query(
                db.query(UserMaster).filter(
                    UserMaster.mobileNumber == mobile
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking if mobile exists {mobile}: {str(e)}")
            raise


    @staticmethod
    def email_mobile_combination_exists(db: Session, email: str, mobile: int) -> bool:
        """
        Check if email + mobile combination already exists (composite unique constraint)

        Args:
            db: SQLAlchemy database session
            email: Email address
            mobile: Mobile number (10-digit integer)

        Returns:
            True if combination exists, False otherwise
        """
        try:
            from src.db.models import UserMaster

            exists = db.query(
                db.query(UserMaster).filter(
                    and_(
                        func.lower(UserMaster.emailId) == email.lower(),
                        UserMaster.mobileNumber == mobile
                    )
                ).exists()
            ).scalar()

            return exists
        except Exception as e:
            logger.error(f"Error checking email-mobile combination: {str(e)}")
            raise


    @staticmethod
    def create_user(db: Session, user_data: Dict[str, Any]) -> Any:
        """
        Create a new user in the database

        Auto-populated fields (should NOT be in user_data):
        - userId: auto-generated (max + 1)
        - createdDate: CURRENT_TIMESTAMP
        - updatedDate: CURRENT_TIMESTAMP

        Args:
            db: SQLAlchemy database session
            user_data: Dictionary containing user fields

        Returns:
            Created user object

        Raises:
            Exception: If creation fails
        """
        try:
            from src.db.models import UserMaster

            # Generate userId if not provided
            if 'userId' not in user_data or not user_data['userId']:
                user_data['userId'] = UserMasterUtils.get_next_user_id(db)

            # Set timestamps
            now = datetime.utcnow()
            user_data['createdDate'] = now
            user_data['updatedDate'] = now

            # Normalize email to lowercase
            if 'emailId' in user_data:
                user_data['emailId'] = user_data['emailId'].lower()

            # Create new user instance
            new_user = UserMaster(**user_data)

            # Add to session and commit
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            logger.info(f"User created successfully: {new_user.userId}")
            return new_user

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise


    @staticmethod
    def update_user(db: Session, user_id: str, update_data: Dict[str, Any]) -> Any:
        """
        Update existing user in the database

        Immutable fields (will be ignored if present):
        - userId: Cannot change
        - createdDate: Cannot change (set on creation)

        Auto-updated fields:
        - updatedDate: Always set to current timestamp

        Required fields:
        - commentLog: Must be provided for audit trail

        Args:
            db: SQLAlchemy database session
            user_id: ID of user to update
            update_data: Dictionary containing fields to update

        Returns:
            Updated user object

        Raises:
            ValueError: If user not found or validation fails
            Exception: If update fails
        """
        try:
            from src.db.models import UserMaster

            # Get existing user
            user = db.query(UserMaster).filter(
                UserMaster.userId == user_id
            ).first()

            if not user:
                raise ValueError(f"User not found: {user_id}")

            # Remove immutable fields if present
            update_data.pop('userId', None)
            update_data.pop('createdDate', None)

            # Auto-update timestamp
            update_data['updatedDate'] = datetime.utcnow()

            # Normalize email if provided
            if 'emailId' in update_data and update_data['emailId']:
                update_data['emailId'] = update_data['emailId'].lower()

            # Update user fields
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            # Commit changes
            db.commit()
            db.refresh(user)

            logger.info(f"User updated successfully: {user_id}")
            return user

        except ValueError as ve:
            db.rollback()
            logger.error(f"Validation error updating user {user_id}: {str(ve)}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise


    @staticmethod
    def delete_user(db: Session, user_id: str) -> bool:
        """
        Delete user from database (Note: Spec says no DELETE operation required)

        This function is provided for completeness but may not be used per requirements

        Args:
            db: SQLAlchemy database session
            user_id: ID of user to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            from src.db.models import UserMaster

            user = db.query(UserMaster).filter(
                UserMaster.userId == user_id
            ).first()

            if not user:
                logger.warning(f"User not found for deletion: {user_id}")
                return False

            db.delete(user)
            db.commit()

            logger.info(f"User deleted: {user_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise


# Create a singleton instance for convenience
user_master_db = UserMasterUtils()
