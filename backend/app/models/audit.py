from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import generate_uuid, get_utc_now


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)  # TRANSACTION_INGEST, ALERT_STATUS_CHANGE, INVESTIGATION_DECISION, AI_QUERY
    entity_type = Column(String(50), nullable=False)  # transaction, alert, investigation, system
    entity_id = Column(String(36), nullable=False)
    description = Column(Text, nullable=False)
    payload_before = Column(Text, nullable=True)  # JSON
    payload_after = Column(Text, nullable=True)   # JSON
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)

    actor = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index("idx_audit_entity", "entity_type", "entity_id"),
        Index("idx_audit_created_at", "created_at"),
    )
