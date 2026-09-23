from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    account_number = Column(String(50), unique=True, index=True, nullable=False)
    account_holder = Column(String(255), nullable=False)
    account_type = Column(String(50), default="checking", nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    risk_tier = Column(String(20), default="low", nullable=False)
    status = Column(String(20), default="active", nullable=False)

    transactions = relationship("Transaction", back_populates="account")


class Vendor(Base, TimestampMixin):
    __tablename__ = "vendors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    is_trusted = Column(Boolean, default=True, nullable=False)

    transactions = relationship("Transaction", back_populates="vendor")


class Beneficiary(Base, TimestampMixin):
    __tablename__ = "beneficiaries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    account_identifier = Column(String(100), index=True, nullable=False)
    routing_code = Column(String(50), nullable=True)
    bank_name = Column(String(255), nullable=True)
    country = Column(String(2), default="US", nullable=False)

    transactions = relationship("Transaction", back_populates="beneficiary")


class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fingerprint = Column(String(255), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    is_known = Column(Boolean, default=True, nullable=False)

    transactions = relationship("Transaction", back_populates="device")


class Location(Base, TimestampMixin):
    __tablename__ = "locations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    country = Column(String(2), nullable=False)
    city = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    transactions = relationship("Transaction", back_populates="location")
