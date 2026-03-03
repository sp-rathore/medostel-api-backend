"""
Application constants - Error codes, status values, and roles
"""


class ErrorCodes:
    """Error codes for API responses"""
    AUTH_001 = "Invalid credentials"
    AUTH_002 = "Token expired"
    AUTH_003 = "Insufficient permissions"
    USER_001 = "User not found"
    USER_002 = "Email already exists"
    USER_003 = "Invalid input data"
    DB_001 = "Database connection error"
    FILE_001 = "Invalid file type"
    FILE_002 = "File size exceeds limit"
    ROLE_001 = "Role not found"
    ROLE_002 = "Role already exists"
    LOCATION_001 = "Location not found"
    REPORT_001 = "Report not found"
    REQUEST_001 = "Registration request not found"
    VALIDATION_001 = "Validation error"


class Roles:
    """User roles in the system"""
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    PATIENT = "Patient"


class StatusCodes:
    """Status values for database records"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    CLOSED = "Closed"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    ERROR = "Error"


class TableNames:
    """Database table names"""
    USER_ROLE_MASTER = "user_role_master"
    STATE_CITY_PINCODE_MASTER = "state_city_pincode_master"
    USER_MASTER = "user_master"
    USER_LOGIN = "user_login"
    NEW_USER_REQUEST = "new_user_request"
    REPORT_HISTORY = "report_history"


class HTTPStatus:
    """HTTP status codes"""
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
