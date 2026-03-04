"""
SQLAlchemy ORM models for database tables
Phase 2: Database Layer - ORM Models
Date: 2026-03-03

Models:
- UserMaster: ORM model for user_master table
- UserRoleMaster: ORM model for user_role_master table
- StateCityPincodeMaster: ORM model for state_city_pincode_master table
- NewUserRequest: ORM model for new_user_request table
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index, UniqueConstraint, CheckConstraint, func
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class UserMaster(Base):
    """
    SQLAlchemy ORM model for user_master table

    Attributes:
        userId: Primary key, unique user identifier (auto-incremented)
        firstName: User first name (required, max 50 chars)
        lastName: User last name (required, max 50 chars)
        currentRole: Reference to user_role_master.rolename (required)
        emailId: Email address (required, unique, max 255 chars)
        mobileNumber: Mobile number (required, unique, 10 digits: 1000000000-9999999999)
        organisation: Organization name (optional, max 255 chars)
        address1: Primary address (optional, max 255 chars)
        address2: Secondary address (optional, max 255 chars)
        stateId: State identifier (optional, varchar reference, max 10 chars)
        stateName: State name (optional, max 100 chars)
        districtId: District identifier (optional, varchar reference, max 10 chars)
        cityId: City identifier (optional, varchar reference, max 10 chars)
        cityName: City name (optional, max 100 chars)
        pinCode: PIN code (optional, varchar reference, max 10 chars)
        commentLog: Most recent change comment (optional, max 255 chars)
        status: User status (required, default: 'active', max 50 chars)
        createdDate: Record creation timestamp (auto-set, immutable)
        updatedDate: Last update timestamp (auto-updated)
    """

    __tablename__ = "user_master"

    # Primary Key
    userId = Column(String(100), primary_key=True, nullable=False, index=True, unique=True)

    # Required Fields
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    currentRole = Column(String(50), ForeignKey('user_role_master.rolename', ondelete='RESTRICT'), nullable=False)
    emailId = Column(String(255), nullable=False, unique=True, index=True)
    mobileNumber = Column(Integer, nullable=False, unique=True, index=True)

    # Optional Fields
    organisation = Column(String(255), nullable=True)
    address1 = Column(String(255), nullable=True)
    address2 = Column(String(255), nullable=True)
    stateId = Column(String(10), nullable=True)  # Reference without FK (reference table lacks unique constraint)
    stateName = Column(String(100), nullable=True)
    districtId = Column(String(10), nullable=True)  # Reference without FK
    cityId = Column(String(10), nullable=True)  # Reference without FK
    cityName = Column(String(100), nullable=True)
    pinCode = Column(String(10), nullable=True)  # Reference without FK
    commentLog = Column(String(255), nullable=True)

    # Status Field
    status = Column(String(50), nullable=False, default='active', index=True)

    # Timestamp Fields
    createdDate = Column(DateTime, nullable=False, default=func.current_timestamp(), index=True)
    updatedDate = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Constraints
    __table_args__ = (
        # Unique constraint on email+mobile combination
        UniqueConstraint('emailId', 'mobileNumber', name='uk_user_master_email_mobile'),

        # Check constraint for status values
        CheckConstraint("status IN ('active', 'pending', 'deceased', 'inactive')", name='ck_user_master_status'),

        # Indexes for query optimization
        Index('idx_user_master_email', 'emailId'),
        Index('idx_user_master_mobile', 'mobileNumber'),
        Index('idx_user_master_role', 'currentRole'),
        Index('idx_user_master_status', 'status'),
        Index('idx_user_master_created', 'createdDate'),
        Index('idx_user_master_updated', 'updatedDate'),
        Index('idx_user_master_city', 'cityId'),
        Index('idx_user_master_state', 'stateId'),
    )

    def __repr__(self) -> str:
        """String representation of UserMaster object"""
        return f"<UserMaster(userId={self.userId}, firstName={self.firstName}, lastName={self.lastName}, emailId={self.emailId})>"


class UserRoleMaster(Base):
    """
    SQLAlchemy ORM model for user_role_master table

    Attributes:
        roleId: Primary key, auto-incremented role identifier
        roleName: Role name (required, unique, max 50 chars)
        status: Role status (default: 'Active', max 20 chars)
        comments: Optional comments (max 250 chars)
        createdDate: Record creation date (auto-set)
        updatedDate: Last update date (auto-updated)
    """

    __tablename__ = "user_role_master"

    # Primary Key
    roleId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # Required Fields
    roleName = Column(String(50), nullable=False, unique=True, index=True)

    # Optional Fields
    status = Column(String(20), nullable=False, default='Active')
    comments = Column(String(250), nullable=True)

    # Timestamp Fields
    createdDate = Column(DateTime, nullable=False, default=func.current_date())
    updatedDate = Column(DateTime, nullable=False, default=func.current_date(), onupdate=func.current_date())

    def __repr__(self) -> str:
        """String representation of UserRoleMaster object"""
        return f"<UserRoleMaster(roleId={self.roleId}, roleName={self.roleName}, status={self.status})>"


class StateCityPincodeMaster(Base):
    """
    SQLAlchemy ORM model for state_city_pincode_master table

    Attributes:
        id: Primary key, auto-incremented identifier
        stateId: State identifier (required, varchar, max 10 chars)
        stateName: State name (required, max 100 chars)
        cityId: City identifier (required, varchar, max 10 chars)
        cityName: City name (required, max 100 chars)
        pinCode: PIN code (required, max 10 chars)
        countryName: Country name (default: 'India', max 100 chars)
        status: Record status (default: 'Active', max 50 chars)
        createdDate: Record creation timestamp (auto-set)
        updatedDate: Last update timestamp (auto-updated)
    """

    __tablename__ = "state_city_pincode_master"

    # Primary Key
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # Required Fields
    stateId = Column(String(10), nullable=False, index=True)
    stateName = Column(String(100), nullable=False, index=True)
    cityId = Column(String(10), nullable=False, index=True)
    cityName = Column(String(100), nullable=False, index=True)
    pinCode = Column(String(10), nullable=False, index=True)

    # Optional Fields
    countryName = Column(String(100), nullable=False, default='India')
    status = Column(String(50), nullable=False, default='Active')

    # Timestamp Fields
    createdDate = Column(DateTime, nullable=False, default=func.current_timestamp())
    updatedDate = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Constraints
    __table_args__ = (
        UniqueConstraint('stateId', 'cityId', 'pinCode', name='uk_state_city_pincode'),
        Index('idx_state_id', 'stateId'),
        Index('idx_city_id', 'cityId'),
        Index('idx_pin_code', 'pinCode'),
        Index('idx_country', 'countryName'),
        Index('idx_location_status', 'status'),
    )

    def __repr__(self) -> str:
        """String representation of StateCityPincodeMaster object"""
        return f"<StateCityPincodeMaster(id={self.id}, stateName={self.stateName}, cityName={self.cityName}, pinCode={self.pinCode})>"


class NewUserRequest(Base):
    """
    SQLAlchemy ORM model for new_user_request table

    Attributes:
        requestId: Primary key, auto-generated request identifier (max 100 chars)
        userId: Email address, unique identifier (max 255 chars)
        firstName: User first name (required, max 100 chars)
        lastName: User last name (required, max 100 chars)
        mobileNumber: Mobile number (required, 10 digits: 1000000000-9999999999)
        organization: Organization name (optional, max 255 chars)
        currentRole: Role name (required, max 50 chars)
        status: Request status (default: 'pending', max 50 chars)
        city_name: City name reference (optional, max 100 chars)
        district_name: District name reference (optional, max 100 chars)
        pincode: PIN code reference (optional, max 10 chars)
        state_name: State name reference (optional, max 100 chars)
        created_Date: Record creation timestamp (auto-set, immutable)
        updated_Date: Last update timestamp (auto-updated)
    """

    __tablename__ = "new_user_request"

    # Primary Key
    requestId = Column(String(100), primary_key=True, nullable=False, unique=True, index=True)

    # Required Fields
    userId = Column(String(255), nullable=False, unique=True, index=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    mobileNumber = Column(Integer, nullable=False, index=True)
    currentRole = Column(String(50), nullable=False, index=True)

    # Optional Fields
    organization = Column(String(255), nullable=True)
    city_name = Column(String(100), nullable=True)
    district_name = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    state_name = Column(String(100), nullable=True)

    # Status Field
    status = Column(String(50), nullable=False, default='pending', index=True)

    # Timestamp Fields
    created_Date = Column(DateTime, nullable=False, default=func.current_timestamp(), index=True)
    updated_Date = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp(), index=True)

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'active', 'rejected')", name='ck_new_user_request_status'),
        CheckConstraint("userId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'", name='ck_new_user_request_email'),
        CheckConstraint("mobileNumber >= 1000000000 AND mobileNumber <= 9999999999", name='ck_new_user_request_mobile'),
        Index('idx_request_email', 'userId'),
        Index('idx_request_mobile', 'mobileNumber'),
        Index('idx_request_status', 'status'),
        Index('idx_request_role', 'currentRole'),
        Index('idx_request_created', 'created_Date'),
        Index('idx_request_updated', 'updated_Date'),
    )

    def __repr__(self) -> str:
        """String representation of NewUserRequest object"""
        return f"<NewUserRequest(requestId={self.requestId}, userId={self.userId}, status={self.status})>"
