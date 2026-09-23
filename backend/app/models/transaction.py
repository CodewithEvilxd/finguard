from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid, get_utc_now


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transaction_id = Column(String(64), unique=True, index=True, nullable=False)
    account_id = Column(String(36), ForeignKey("accounts.id"), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    transaction_type = Column(String(50), nullable=False)  # wire, purchase, transfer, withdrawal
    timestamp = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    channel = Column(String(50), default="web", nullable=False)  # web, mobile, atm, api, pos

    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id"), nullable=True)
    vendor_id = Column(String(36), ForeignKey("vendors.id"), nullable=True)
    device_id = Column(String(36), ForeignKey("devices.id"), nullable=True)
    location_id = Column(String(36), ForeignKey("locations.id"), nullable=True)

    status = Column(String(20), default="completed", nullable=False)  # completed, flagged, under_review, rejected
    ingestion_id = Column(String(64), nullable=True)
    raw_payload = Column(Text, nullable=True)

    # Relationships
    account = relationship("Account", back_populates="transactions")
    beneficiary = relationship("Beneficiary", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")
    device = relationship("Device", back_populates="transactions")
    location = relationship("Location", back_populates="transactions")

    prediction = relationship("ModelPrediction", back_populates="transaction", uselist=False)
    alerts = relationship("Alert", back_populates="transaction")

    __table_args__ = (
        Index("idx_transactions_account_timestamp", "account_id", "timestamp"),
        Index("idx_transactions_created_at", "created_at"),
    )
