from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert, Investigation, InvestigationNote
from app.schemas.investigation import InvestigationCreate, InvestigationDecision
from app.services.audit_service import AuditService
from app.core.logging import logger


class InvestigationService:
    @staticmethod
    async def create_investigation(
        db: AsyncSession,
        data: InvestigationCreate,
        actor_id: Optional[str] = None,
    ) -> Investigation:
        # Check if already exists for this alert
        existing = await db.execute(
            select(Investigation).where(Investigation.alert_id == data.alert_id)
        )
        existing_case = existing.scalars().first()
        if existing_case:
            return existing_case

        investigation = Investigation(
            alert_id=data.alert_id,
            assigned_analyst_id=actor_id,
            status="open",
            priority=data.priority,
        )
        db.add(investigation)
        await db.flush()

        if data.initial_notes:
            note = InvestigationNote(
                investigation_id=investigation.id,
                author_id=actor_id,
                note_type="analyst",
                content=data.initial_notes,
            )
            db.add(note)
            await db.flush()

        # Update alert status to investigating
        alert_q = await db.execute(select(Alert).where(Alert.id == data.alert_id))
        alert = alert_q.scalars().first()
        if alert:
            alert.status = "investigating"

        await AuditService.record_event(
            db=db,
            action="INVESTIGATION_OPENED",
            entity_type="investigation",
            entity_id=investigation.id,
            actor_id=actor_id,
            description=f"Investigation opened for alert {data.alert_id}",
            payload_after={"priority": data.priority},
        )
        return investigation

    @staticmethod
    async def submit_decision(
        db: AsyncSession,
        investigation_id: str,
        data: InvestigationDecision,
        actor_id: Optional[str] = None,
    ) -> Investigation:
        q = await db.execute(select(Investigation).where(Investigation.id == investigation_id))
        investigation = q.scalars().first()
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")

        old_status = investigation.status
        investigation.decision = data.decision
        investigation.decision_rationale = data.rationale
        investigation.decided_at = datetime.now(timezone.utc)

        # Update status based on decision
        if data.decision == "cleared":
            investigation.status = "cleared"
        elif data.decision == "confirmed_fraud":
            investigation.status = "confirmed_fraud"
        elif data.decision == "escalated":
            investigation.status = "escalated"
        else:
            investigation.status = "under_review"

        # Add decision note to timeline
        note = InvestigationNote(
            investigation_id=investigation.id,
            author_id=actor_id,
            note_type="analyst",
            content=f"Decision recorded: {data.decision.upper()}. Rationale: {data.rationale}",
        )
        db.add(note)

        # Also update associated alert
        alert_q = await db.execute(select(Alert).where(Alert.id == investigation.alert_id))
        alert = alert_q.scalars().first()
        if alert:
            alert.status = investigation.status

        await db.flush()

        await AuditService.record_event(
            db=db,
            action="INVESTIGATION_DECIDED",
            entity_type="investigation",
            entity_id=investigation.id,
            actor_id=actor_id,
            description=f"Decision {data.decision} recorded with rationale: {data.rationale[:50]}...",
            payload_before={"status": old_status},
            payload_after={"status": investigation.status, "decision": data.decision, "rationale": data.rationale},
        )
        return investigation
