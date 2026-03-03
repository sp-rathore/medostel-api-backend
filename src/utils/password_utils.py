"""
Password hashing and verification utilities for User_Login module
Date: March 3, 2026
Purpose: Secure password storage using bcrypt with consistent hashing
"""

import bcrypt
import secrets
from typing import Tuple


class PasswordManager:
    """
    Manages password hashing and verification using bcrypt.
    Implements industry-standard password security practices.
    """

    # Bcrypt cost factor (rounds): 12 is recommended for security vs performance
    # Higher = more secure but slower (good for ~100ms hashing time)
    BCRYPT_COST = 12

    # Default password used when not provided during user login creation
    DEFAULT_PASSWORD = "Medostel@AI2026"

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hash a plain-text password using bcrypt.

        Args:
            plain_password: The password to hash (must be at least 8 characters)

        Returns:
            bcrypt hashed password (60 characters)

        Raises:
            ValueError: If password is less than 8 characters
            Exception: If hashing fails

        Example:
            >>> hashed = PasswordManager.hash_password("MyPassword123")
            >>> len(hashed)
            60
        """
        if not plain_password or len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt(rounds=PasswordManager.BCRYPT_COST)
            hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            raise Exception(f"Error hashing password: {str(e)}")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain-text password against a bcrypt hash.

        Args:
            plain_password: The plain-text password to verify
            hashed_password: The bcrypt hashed password from database

        Returns:
            True if password matches, False otherwise

        Example:
            >>> hashed = PasswordManager.hash_password("MyPassword123")
            >>> PasswordManager.verify_password("MyPassword123", hashed)
            True
            >>> PasswordManager.verify_password("WrongPassword", hashed)
            False
        """
        try:
            # Verify password against hash
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            # Return False on any error (invalid hash format, etc.)
            return False

    @staticmethod
    def get_default_password() -> str:
        """
        Get the default password used for new user logins.

        Returns:
            Default password string: 'Medostel@AI2026'

        Note:
            This should be communicated to the user through a separate secure channel.
            Users should be required to change it on first login.
        """
        return PasswordManager.DEFAULT_PASSWORD

    @staticmethod
    def get_hashed_default_password() -> str:
        """
        Get the bcrypt hash of the default password.

        Returns:
            Bcrypt hashed default password

        Example:
            >>> hashed_default = PasswordManager.get_hashed_default_password()
            >>> PasswordManager.verify_password(PasswordManager.DEFAULT_PASSWORD, hashed_default)
            True
        """
        return PasswordManager.hash_password(PasswordManager.DEFAULT_PASSWORD)

    @staticmethod
    def generate_temporary_password(length: int = 16) -> str:
        """
        Generate a random temporary password.

        Args:
            length: Length of temporary password (default: 16 characters)

        Returns:
            Random password string containing letters, digits, and special chars

        Example:
            >>> temp_pwd = PasswordManager.generate_temporary_password()
            >>> len(temp_pwd)
            16
        """
        # Use secrets module for cryptographically secure randomness
        # Generate random bytes and convert to hex string
        random_bytes = secrets.token_bytes(length)
        # Convert to base62 (alphanumeric + special chars)
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        result = ""
        for byte in random_bytes:
            result += chars[byte % len(chars)]
        return result[:length]

    @staticmethod
    def password_meets_requirements(password: str) -> Tuple[bool, str]:
        """
        Validate if password meets security requirements.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, message)
            - is_valid: True if meets all requirements
            - message: Reason if invalid, empty string if valid

        Requirements:
            - Minimum 8 characters
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character (!@#$%^&*)

        Example:
            >>> is_valid, msg = PasswordManager.password_meets_requirements("weak")
            >>> is_valid
            False
        """
        if not password:
            return False, "Password cannot be empty"

        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if not has_upper:
            return False, "Password must contain at least one uppercase letter"
        if not has_lower:
            return False, "Password must contain at least one lowercase letter"
        if not has_digit:
            return False, "Password must contain at least one digit"
        if not has_special:
            return False, "Password must contain at least one special character"

        return True, ""


def hash_password(password: str) -> str:
    """
    Convenience function to hash a password.
    Wrapper around PasswordManager.hash_password()

    Args:
        password: Plain-text password to hash

    Returns:
        Bcrypt hashed password
    """
    return PasswordManager.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Convenience function to verify a password.
    Wrapper around PasswordManager.verify_password()

    Args:
        plain_password: Plain-text password
        hashed_password: Bcrypt hash to compare against

    Returns:
        True if password matches, False otherwise
    """
    return PasswordManager.verify_password(plain_password, hashed_password)


def get_default_password() -> str:
    """
    Get the default password.
    Wrapper around PasswordManager.get_default_password()

    Returns:
        Default password: 'Medostel@AI2026'
    """
    return PasswordManager.get_default_password()
