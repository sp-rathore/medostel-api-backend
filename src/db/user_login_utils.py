"""
Database utility functions for User_Login module
Date: March 3, 2026
Purpose: CRUD operations and validation for user_login table
"""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from src.utils.password_utils import PasswordManager
import logging

# Configure logging
logger = logging.getLogger(__name__)


class UserLoginManager:
    """
    Manages user login database operations.
    Provides CRUD operations with built-in validation and error handling.
    """

    @staticmethod
    def email_exists_in_user_master(email_id: str, db_connection) -> bool:
        """
        Check if email exists in user_master table.

        Args:
            email_id: Email address to check
            db_connection: Database connection object

        Returns:
            True if email exists, False otherwise
        """
        try:
            query = "SELECT COUNT(*) FROM user_master WHERE emailId = %s"
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id,))
                result = cursor.fetchone()
                return result[0] > 0
        except Exception as e:
            logger.error(f"Error checking email in user_master: {str(e)}")
            return False

    @staticmethod
    def mobile_matches_email(
        email_id: str,
        mobile_number: str,
        db_connection
    ) -> bool:
        """
        Verify that mobile number matches email in user_master.

        Args:
            email_id: Email address
            mobile_number: Mobile number to verify
            db_connection: Database connection object

        Returns:
            True if mobile matches email, False otherwise
        """
        try:
            query = "SELECT mobileNumber FROM user_master WHERE emailId = %s"
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id,))
                result = cursor.fetchone()

                if not result:
                    logger.warning(f"Email {email_id} not found in user_master")
                    return False

                stored_mobile = str(int(result[0]))  # Convert to int then back to string
                provided_mobile = mobile_number.strip()

                match = stored_mobile == provided_mobile
                if not match:
                    logger.warning(
                        f"Mobile mismatch for {email_id}: "
                        f"stored={stored_mobile}, provided={provided_mobile}"
                    )
                return match
        except Exception as e:
            logger.error(f"Error verifying mobile for email: {str(e)}")
            return False

    @staticmethod
    def user_status_is_active(email_id: str, db_connection) -> bool:
        """
        Check if user's status in user_master is 'active'.

        Args:
            email_id: Email address
            db_connection: Database connection object

        Returns:
            True if status is 'active', False otherwise
        """
        try:
            query = "SELECT status FROM user_master WHERE emailId = %s"
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id,))
                result = cursor.fetchone()

                if not result:
                    logger.warning(f"Email {email_id} not found in user_master")
                    return False

                status = result[0].lower() if result[0] else ""
                return status == 'active'
        except Exception as e:
            logger.error(f"Error checking user status: {str(e)}")
            return False

    @staticmethod
    def login_exists_for_email(email_id: str, db_connection) -> bool:
        """
        Check if login credentials already exist for email.

        Args:
            email_id: Email address
            db_connection: Database connection object

        Returns:
            True if login exists, False otherwise
        """
        try:
            query = "SELECT COUNT(*) FROM user_login WHERE email_id = %s"
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id,))
                result = cursor.fetchone()
                return result[0] > 0
        except Exception as e:
            logger.error(f"Error checking if login exists: {str(e)}")
            return False

    @staticmethod
    def get_user_login_by_email(email_id: str, db_connection) -> Optional[Dict[str, Any]]:
        """
        Retrieve user login record by email.

        Args:
            email_id: Email address
            db_connection: Database connection object

        Returns:
            Dictionary with login record, or None if not found
        """
        try:
            query = """
                SELECT email_id, password, mobile_number, is_active,
                       last_login, created_date, updated_date
                FROM user_login
                WHERE email_id = %s
            """
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id,))
                result = cursor.fetchone()

                if not result:
                    logger.info(f"No login record found for email: {email_id}")
                    return None

                return {
                    'email_id': result[0],
                    'password': result[1],
                    'mobile_number': str(int(result[2])),
                    'is_active': result[3],
                    'last_login': result[4],
                    'created_date': result[5],
                    'updated_date': result[6]
                }
        except Exception as e:
            logger.error(f"Error retrieving login record: {str(e)}")
            return None

    @staticmethod
    def get_user_login_by_mobile(mobile_number: str, db_connection) -> Optional[Dict[str, Any]]:
        """
        Retrieve user login record by mobile number.

        Args:
            mobile_number: Mobile number to search
            db_connection: Database connection object

        Returns:
            Dictionary with login record, or None if not found
        """
        try:
            query = """
                SELECT email_id, password, mobile_number, is_active,
                       last_login, created_date, updated_date
                FROM user_login
                WHERE mobile_number = %s
            """
            with db_connection.cursor() as cursor:
                cursor.execute(query, (int(mobile_number),))
                result = cursor.fetchone()

                if not result:
                    logger.info(f"No login record found for mobile: {mobile_number}")
                    return None

                return {
                    'email_id': result[0],
                    'password': result[1],
                    'mobile_number': str(int(result[2])),
                    'is_active': result[3],
                    'last_login': result[4],
                    'created_date': result[5],
                    'updated_date': result[6]
                }
        except Exception as e:
            logger.error(f"Error retrieving login by mobile: {str(e)}")
            return None

    @staticmethod
    def create_user_login(
        email_id: str,
        mobile_number: str,
        password: Optional[str],
        db_connection
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Create new user login record.

        Args:
            email_id: Email address (PK)
            mobile_number: Mobile number
            password: Password (optional, uses default if None)
            db_connection: Database connection object

        Returns:
            Tuple of (success, data_dict, message)
        """
        try:
            # Validate email exists in user_master
            if not UserLoginManager.email_exists_in_user_master(email_id, db_connection):
                return False, {}, "Email not registered in user_master"

            # Validate mobile matches email
            if not UserLoginManager.mobile_matches_email(email_id, mobile_number, db_connection):
                return False, {}, "Mobile number doesn't match registered mobile for this email"

            # Validate user status is active
            if not UserLoginManager.user_status_is_active(email_id, db_connection):
                return False, {}, "User account is not active in user_master"

            # Check if login already exists
            if UserLoginManager.login_exists_for_email(email_id, db_connection):
                return False, {}, "Login credentials already exist for this email"

            # Use provided password or default
            password_to_hash = password if password else PasswordManager.DEFAULT_PASSWORD
            hashed_password = PasswordManager.hash_password(password_to_hash)

            # Determine is_active value
            is_active = 'Y'  # Assumed to be active since user_master status is active

            # Insert new record
            query = """
                INSERT INTO user_login
                (email_id, password, mobile_number, is_active, created_date, updated_date)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING email_id, password, mobile_number, is_active,
                          last_login, created_date, updated_date
            """
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id, hashed_password, int(mobile_number), is_active))
                result = cursor.fetchone()
                db_connection.commit()

                logger.info(f"Created login record for email: {email_id}")

                return True, {
                    'email_id': result[0],
                    'password': hashed_password,  # Return hashed
                    'mobile_number': str(int(result[2])),
                    'is_active': result[3],
                    'last_login': result[4],
                    'created_date': result[5],
                    'updated_date': result[6]
                }, "User login created successfully"

        except Exception as e:
            db_connection.rollback()
            logger.error(f"Error creating user login: {str(e)}")
            return False, {}, f"Error creating login record: {str(e)}"

    @staticmethod
    def update_password(
        email_id: str,
        new_password: str,
        db_connection
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Update user password.

        Args:
            email_id: Email address
            new_password: New password to set
            db_connection: Database connection object

        Returns:
            Tuple of (success, data_dict, message)
        """
        try:
            # Check login exists
            login = UserLoginManager.get_user_login_by_email(email_id, db_connection)
            if not login:
                return False, {}, "User login record not found"

            # Hash new password
            hashed_password = PasswordManager.hash_password(new_password)

            # Update password and updated_date (NOT last_login)
            query = """
                UPDATE user_login
                SET password = %s, updated_date = CURRENT_TIMESTAMP
                WHERE email_id = %s
                RETURNING email_id, password, mobile_number, is_active,
                          last_login, created_date, updated_date
            """
            with db_connection.cursor() as cursor:
                cursor.execute(query, (hashed_password, email_id))
                result = cursor.fetchone()
                db_connection.commit()

                logger.info(f"Updated password for email: {email_id}")

                return True, {
                    'email_id': result[0],
                    'mobile_number': str(int(result[2])),
                    'is_active': result[3],
                    'last_login': result[4],
                    'created_date': result[5],
                    'updated_date': result[6]
                }, "Password updated successfully"

        except Exception as e:
            db_connection.rollback()
            logger.error(f"Error updating password: {str(e)}")
            return False, {}, f"Error updating password: {str(e)}"

    @staticmethod
    def update_is_active(
        email_id: str,
        is_active: str,
        db_connection
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Update user active status.

        Args:
            email_id: Email address
            is_active: Status value ('Y' or 'N')
            db_connection: Database connection object

        Returns:
            Tuple of (success, data_dict, message)
        """
        try:
            # Validate status
            if is_active.upper() not in ['Y', 'N']:
                return False, {}, "is_active must be Y or N"

            # Check login exists
            login = UserLoginManager.get_user_login_by_email(email_id, db_connection)
            if not login:
                return False, {}, "User login record not found"

            # Update status
            query = """
                UPDATE user_login
                SET is_active = %s, updated_date = CURRENT_TIMESTAMP
                WHERE email_id = %s
                RETURNING email_id, password, mobile_number, is_active,
                          last_login, created_date, updated_date
            """
            with db_connection.cursor() as cursor:
                cursor.execute(query, (is_active.upper(), email_id))
                result = cursor.fetchone()
                db_connection.commit()

                logger.info(f"Updated status for email {email_id}: {is_active}")

                return True, {
                    'email_id': result[0],
                    'mobile_number': str(int(result[2])),
                    'is_active': result[3],
                    'last_login': result[4],
                    'created_date': result[5],
                    'updated_date': result[6]
                }, "User status updated successfully"

        except Exception as e:
            db_connection.rollback()
            logger.error(f"Error updating status: {str(e)}")
            return False, {}, f"Error updating status: {str(e)}"

    @staticmethod
    def update_last_login(
        email_id: str,
        db_connection
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Update last login timestamp (called on successful authentication).

        Args:
            email_id: Email address
            db_connection: Database connection object

        Returns:
            Tuple of (success, data_dict, message)
        """
        try:
            # Check login exists
            login = UserLoginManager.get_user_login_by_email(email_id, db_connection)
            if not login:
                return False, {}, "User login record not found"

            # Update last_login only
            query = """
                UPDATE user_login
                SET last_login = CURRENT_TIMESTAMP
                WHERE email_id = %s
                RETURNING email_id, password, mobile_number, is_active,
                          last_login, created_date, updated_date
            """
            with db_connection.cursor() as cursor:
                cursor.execute(query, (email_id,))
                result = cursor.fetchone()
                db_connection.commit()

                logger.info(f"Updated last_login for email: {email_id}")

                return True, {
                    'email_id': result[0],
                    'mobile_number': str(int(result[2])),
                    'is_active': result[3],
                    'last_login': result[4],
                    'created_date': result[5],
                    'updated_date': result[6]
                }, "Last login updated"

        except Exception as e:
            db_connection.rollback()
            logger.error(f"Error updating last_login: {str(e)}")
            return False, {}, f"Error updating last_login: {str(e)}"


# Convenience functions (wrappers)

def email_exists_in_user_master(email_id: str, db_connection) -> bool:
    """Check if email exists in user_master"""
    return UserLoginManager.email_exists_in_user_master(email_id, db_connection)


def mobile_matches_email(email_id: str, mobile_number: str, db_connection) -> bool:
    """Verify mobile matches email in user_master"""
    return UserLoginManager.mobile_matches_email(email_id, mobile_number, db_connection)


def user_status_is_active(email_id: str, db_connection) -> bool:
    """Check if user status is active"""
    return UserLoginManager.user_status_is_active(email_id, db_connection)


def login_exists_for_email(email_id: str, db_connection) -> bool:
    """Check if login exists"""
    return UserLoginManager.login_exists_for_email(email_id, db_connection)


def get_user_login_by_email(email_id: str, db_connection) -> Optional[Dict[str, Any]]:
    """Get login by email"""
    return UserLoginManager.get_user_login_by_email(email_id, db_connection)


def get_user_login_by_mobile(mobile_number: str, db_connection) -> Optional[Dict[str, Any]]:
    """Get login by mobile"""
    return UserLoginManager.get_user_login_by_mobile(mobile_number, db_connection)


def create_user_login(
    email_id: str,
    mobile_number: str,
    password: Optional[str],
    db_connection
) -> Tuple[bool, Dict[str, Any], str]:
    """Create new login"""
    return UserLoginManager.create_user_login(email_id, mobile_number, password, db_connection)


def update_password(
    email_id: str,
    new_password: str,
    db_connection
) -> Tuple[bool, Dict[str, Any], str]:
    """Update password"""
    return UserLoginManager.update_password(email_id, new_password, db_connection)


def update_is_active(
    email_id: str,
    is_active: str,
    db_connection
) -> Tuple[bool, Dict[str, Any], str]:
    """Update is_active status"""
    return UserLoginManager.update_is_active(email_id, is_active, db_connection)


def update_last_login(
    email_id: str,
    db_connection
) -> Tuple[bool, Dict[str, Any], str]:
    """Update last login timestamp"""
    return UserLoginManager.update_last_login(email_id, db_connection)
