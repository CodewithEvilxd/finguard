from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transaction_id = Column(String(36), ForeignKey("transactions.id"), index=True, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)  # medium, high, critical
    status = Column(String(30), default="new", nullable=False)  # new, investigating, confirmed_fraud, false_positive, dismissed
    trigger_reason = Column(String(255), nullable=False)
    factors_summary = Column(Text, nullable=True)  # JSON summary of top contributors

    transaction = relationship("Transaction", back_populates="alerts")
    investigation = relationship("Investigation", back_populates="alert", uselist=False)

    __table_args__ = (
        Index("idx_alerts_status_risk_created", "status", "risk_level", "created_at"),
    )


class Investigation(Base, TimestampMixin):
    __tablename__ = "investigations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    alert_id = Column(String(36), ForeignKey("alerts.id"), unique=True, index=True, nullable=False)
    assigned_analyst_id = Column(String(36), ForeignKey("users.id"), nullable=True)

    status = Column(String(30), default="open", nullable=False)  # open, under_review, confirmed_fraud, cleared, escalated
    priority = Column(String(20), default="high", nullable=False)  # low, medium, high, urgent
    decision = Column(String(50), nullable=True)  # cleared, confirmed_fraud, escalated, monitor
    decision_rationale = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)

    alert = relationship("Alert", back_populates="investigation")
    assigned_analyst = relationship("User", back_populates="investigations")
    notes = relationship("InvestigationNote", back_populates="investigation", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_investigations_status_updated", "status", "updated_at"),
    )


class InvestigationNote(Base, TimestampMixin):
    __tablename__ = "investigation_notes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    note_type = Column(String(30), default="analyst", nullable=False)  # analyst, ai_assistant, system
    content = Column(Text, nullable=False)
    metadata_payload = Column(Text, nullable=True)  # JSON citations/evidence

    investigation = relationship("Investigation", back_populates="notes")
