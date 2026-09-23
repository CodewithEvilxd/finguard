import json
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert, Investigation
from app.models.transaction import Transaction
from app.services.audit_service import AuditService
from app.core.logging import logger


class AlertService:
    @staticmethod
    async def create_alert_if_needed(
        db: AsyncSession,
        transaction: Transaction,
        risk_score: float,
        risk_level: str,
        factors_summary: Optional[str] = None,
    ) -> Optional[Alert]:
        # Only create alerts for high or critical risk thresholds
        if risk_level not in {"high", "critical", "medium"}:
            return None

        # Check if an alert already exists for this transaction (idempotency)
        existing_alert = await db.execute(
            select(Alert).where(Alert.transaction_id == transaction.id)
        )
        if existing_alert.scalars().first():
            return existing_alert.scalars().first()

        reason = f"Automated risk trigger: {risk_level.upper()} score ({risk_score:.1f})"
        new_alert = Alert(
            transaction_id=transaction.id,
            risk_score=risk_score,
            risk_level=risk_level,
            status="new",
            trigger_reason=reason,
            factors_summary=factors_summary,
        )
        db.add(new_alert)
        await db.flush()

        # Update transaction status
        transaction.status = "flagged"

        # Record audit log
        await AuditService.record_event(
            db=db,
            action="ALERT_GENERATED",
            entity_type="alert",
            entity_id=new_alert.id,
            description=f"Alert generated for transaction {transaction.transaction_id} with score {risk_score:.1f}",
            payload_after={"risk_score": risk_score, "risk_level": risk_level, "alert_id": new_alert.id},
        )
        logger.info(f"Alert {new_alert.id} generated for transaction {transaction.transaction_id}")
        return new_alert

    @staticmethod
    async def update_alert_status(
        db: AsyncSession,
        alert: Alert,
        new_status: str,
        actor_id: Optional[str] = None,
        note: Optional[str] = None,
    ) -> Alert:
        old_status = alert.status
        alert.status = new_status
        await db.flush()

        await AuditService.record_event(
            db=db,
            action="ALERT_STATUS_UPDATE",
            entity_type="alert",
            entity_id=alert.id,
            actor_id=actor_id,
            description=f"Alert status updated from {old_status} to {new_status}. Note: {note or 'none'}",
            payload_before={"status": old_status},
            payload_after={"status": new_status, "note": note},
        )
        return alert
