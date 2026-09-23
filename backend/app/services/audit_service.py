import json
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog
from app.core.logging import logger


class AuditService:
    @staticmethod
    async def record_event(
        db: AsyncSession,
        action: str,
        entity_type: str,
        entity_id: str,
        description: str,
        actor_id: Optional[str] = None,
        payload_before: Optional[Dict[str, Any]] = None,
        payload_after: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        audit_entry = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            actor_id=actor_id,
            payload_before=json.dumps(payload_before) if payload_before else None,
            payload_after=json.dumps(payload_after) if payload_after else None,
            ip_address=ip_address,
        )
        db.add(audit_entry)
        await db.flush()
        logger.info(f"Audit log recorded: {action} on {entity_type}:{entity_id}")
        return audit_entry
