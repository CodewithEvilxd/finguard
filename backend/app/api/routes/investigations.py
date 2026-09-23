import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.dependencies.db import get_db
from app.models.alert import Alert, Investigation, InvestigationNote
from app.schemas.alert import AlertResponse
from app.schemas.common import PaginatedResponse
from app.schemas.investigation import (
    InvestigationCreate,
    InvestigationDecision,
    InvestigationNoteResponse,
    InvestigationResponse,
)
from app.services.investigation_service import InvestigationService

router = APIRouter(prefix="/investigations", tags=["investigations"])


@router.post("", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED)
async def create_investigation(
    payload: InvestigationCreate,
    db: AsyncSession = Depends(get_db),
):
    investigation = await InvestigationService.create_investigation(db, payload)

    stmt = (
        select(Investigation)
        .options(selectinload(Investigation.notes))
        .where(Investigation.id == investigation.id)
    )
    res = await db.execute(stmt)
    inv = res.scalars().first()

    return InvestigationResponse(
        id=inv.id,
        alert_id=inv.alert_id,
        assigned_analyst_id=inv.assigned_analyst_id,
        status=inv.status,
        priority=inv.priority,
        decision=inv.decision,
        decision_rationale=inv.decision_rationale,
        decided_at=inv.decided_at,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        notes=[InvestigationNoteResponse.from_orm(n) for n in inv.notes],
    )


@router.get("", response_model=PaginatedResponse[InvestigationResponse])
async def list_investigations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status: open, in_review, closed"),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high, urgent"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Investigation).options(selectinload(Investigation.notes))
    count_stmt = select(func.count(Investigation.id))

    if status:
        stmt = stmt.where(Investigation.status == status)
        count_stmt = count_stmt.where(Investigation.status == status)

    if priority:
        stmt = stmt.where(Investigation.priority == priority)
        count_stmt = count_stmt.where(Investigation.priority == priority)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(desc(Investigation.updated_at)).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    investigations = result.scalars().all()

    items = []
    for inv in investigations:
        alert_stmt = select(Alert).where(Alert.id == inv.alert_id)
        alert_res = await db.execute(alert_stmt)
        alert = alert_res.scalars().first()
        alert_resp = None
        if alert:
            alert_resp = AlertResponse(
                id=alert.id,
                transaction_id=alert.transaction_id,
                risk_score=alert.risk_score,
                risk_level=alert.risk_level,
                status=alert.status,
                trigger_reason=alert.trigger_reason,
                factors_summary=alert.factors_summary,
                created_at=alert.created_at,
                updated_at=alert.updated_at,
            )

        items.append(
            InvestigationResponse(
                id=inv.id,
                alert_id=inv.alert_id,
                assigned_analyst_id=inv.assigned_analyst_id,
                status=inv.status,
                priority=inv.priority,
                decision=inv.decision,
                decision_rationale=inv.decision_rationale,
                decided_at=inv.decided_at,
                created_at=inv.created_at,
                updated_at=inv.updated_at,
                alert=alert_resp,
                notes=[InvestigationNoteResponse.from_orm(n) for n in inv.notes],
            )
        )

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{id}", response_model=InvestigationResponse)
async def get_investigation(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Investigation)
        .options(selectinload(Investigation.notes))
        .where(Investigation.id == id)
    )
    res = await db.execute(stmt)
    inv = res.scalars().first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Investigation {id} not found")

    alert_stmt = select(Alert).where(Alert.id == inv.alert_id)
    alert_res = await db.execute(alert_stmt)
    alert = alert_res.scalars().first()
    alert_resp = None
    if alert:
        alert_resp = AlertResponse(
            id=alert.id,
            transaction_id=alert.transaction_id,
            risk_score=alert.risk_score,
            risk_level=alert.risk_level,
            status=alert.status,
            trigger_reason=alert.trigger_reason,
            factors_summary=alert.factors_summary,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
        )

    return InvestigationResponse(
        id=inv.id,
        alert_id=inv.alert_id,
        assigned_analyst_id=inv.assigned_analyst_id,
        status=inv.status,
        priority=inv.priority,
        decision=inv.decision,
        decision_rationale=inv.decision_rationale,
        decided_at=inv.decided_at,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        alert=alert_resp,
        notes=[InvestigationNoteResponse.from_orm(n) for n in inv.notes],
    )


@router.post("/{id}/decision", response_model=InvestigationResponse)
async def submit_investigation_decision(
    id: str,
    payload: InvestigationDecision,
    db: AsyncSession = Depends(get_db),
):
    try:
        inv = await InvestigationService.submit_decision(db, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    stmt = (
        select(Investigation)
        .options(selectinload(Investigation.notes))
        .where(Investigation.id == inv.id)
    )
    res = await db.execute(stmt)
    refreshed = res.scalars().first()

    alert_stmt = select(Alert).where(Alert.id == refreshed.alert_id)
    alert_res = await db.execute(alert_stmt)
    alert = alert_res.scalars().first()
    alert_resp = None
    if alert:
        alert_resp = AlertResponse(
            id=alert.id,
            transaction_id=alert.transaction_id,
            risk_score=alert.risk_score,
            risk_level=alert.risk_level,
            status=alert.status,
            trigger_reason=alert.trigger_reason,
            factors_summary=alert.factors_summary,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
        )

    return InvestigationResponse(
        id=refreshed.id,
        alert_id=refreshed.alert_id,
        assigned_analyst_id=refreshed.assigned_analyst_id,
        status=refreshed.status,
        priority=refreshed.priority,
        decision=refreshed.decision,
        decision_rationale=refreshed.decision_rationale,
        decided_at=refreshed.decided_at,
        created_at=refreshed.created_at,
        updated_at=refreshed.updated_at,
        alert=alert_resp,
        notes=[InvestigationNoteResponse.from_orm(n) for n in refreshed.notes],
    )
