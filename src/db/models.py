"""
SQLAlchemy ORM models for database tables
Phase 2: Database Layer - ORM Models
Date: 2026-03-03

Models:
- UserMaster: ORM model for user_master table
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
