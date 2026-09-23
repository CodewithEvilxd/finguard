import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_db
from app.models.alert import Alert
from app.models.transaction import Transaction
from app.schemas.alert import AlertResponse, AlertUpdate
from app.schemas.common import PaginatedResponse
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=PaginatedResponse[AlertResponse])
async def list_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    risk_level: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Alert, Transaction).join(Transaction, Alert.transaction_id == Transaction.id)
    count_stmt = select(func.count(Alert.id))

    if status_filter:
        stmt = stmt.where(Alert.status == status_filter)
        count_stmt = count_stmt.where(Alert.status == status_filter)
    if risk_level:
        stmt = stmt.where(Alert.risk_level == risk_level)
        count_stmt = count_stmt.where(Alert.risk_level == risk_level)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(desc(Alert.created_at)).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    rows = result.all()

    items = []
    for alert, tx in rows:
        items.append(
            AlertResponse(
                id=alert.id,
                transaction_id=tx.transaction_id,
                risk_score=alert.risk_score,
                risk_level=alert.risk_level,
                status=alert.status,
                trigger_reason=alert.trigger_reason,
                factors_summary=alert.factors_summary,
                created_at=alert.created_at,
                updated_at=alert.updated_at,
                transaction_amount=tx.amount,
                transaction_currency=tx.currency,
                account_id=tx.account_id,
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


@router.get("/{id}", response_model=AlertResponse)
async def get_alert(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Alert, Transaction)
        .join(Transaction, Alert.transaction_id == Transaction.id)
        .where(Alert.id == id)
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert {id} not found")

    alert, tx = row
    return AlertResponse(
        id=alert.id,
        transaction_id=tx.transaction_id,
        risk_score=alert.risk_score,
        risk_level=alert.risk_level,
        status=alert.status,
        trigger_reason=alert.trigger_reason,
        factors_summary=alert.factors_summary,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        transaction_amount=tx.amount,
        transaction_currency=tx.currency,
        account_id=tx.account_id,
    )


@router.patch("/{id}", response_model=AlertResponse)
async def update_alert(
    id: str,
    payload: AlertUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Alert).where(Alert.id == id)
    res = await db.execute(stmt)
    alert = res.scalars().first()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert {id} not found")

    updated = await AlertService.update_alert_status(db, alert, payload.status, note=payload.notes)

    tx_stmt = select(Transaction).where(Transaction.id == updated.transaction_id)
    tx_res = await db.execute(tx_stmt)
    tx = tx_res.scalars().first()

    return AlertResponse(
        id=updated.id,
        transaction_id=tx.transaction_id if tx else "unknown",
        risk_score=updated.risk_score,
        risk_level=updated.risk_level,
        status=updated.status,
        trigger_reason=updated.trigger_reason,
        factors_summary=updated.factors_summary,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
        transaction_amount=tx.amount if tx else None,
        transaction_currency=tx.currency if tx else None,
        account_id=tx.account_id if tx else None,
    )
