import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_db
from app.models.transaction import Transaction
from app.models.ml import ModelPrediction
from app.models.alert import Alert, Investigation
from app.schemas.common import PaginatedResponse
from app.schemas.transaction import (
    BatchTransactionCreate,
    BatchTransactionResponse,
    TransactionCreate,
    TransactionResponse,
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def ingest_transaction(
    payload: TransactionCreate,
    db: AsyncSession = Depends(get_db),
):
    transaction, created = await TransactionService.ingest_transaction(db, payload)

    # Fetch associated prediction if available
    pred_stmt = select(ModelPrediction).where(ModelPrediction.transaction_id == transaction.id)
    pred_res = await db.execute(pred_stmt)
    pred = pred_res.scalars().first()

    # Fetch alert / investigation linkage
    alert_stmt = select(Alert).where(Alert.transaction_id == transaction.id)
    alert_res = await db.execute(alert_stmt)
    alert = alert_res.scalars().first()

    inv_id = None
    inv_status = None
    if alert:
        inv_stmt = select(Investigation).where(Investigation.alert_id == alert.id)
        inv_res = await db.execute(inv_stmt)
        inv = inv_res.scalars().first()
        if inv:
            inv_id = inv.id
            inv_status = inv.status

    return TransactionResponse(
        id=transaction.id,
        transaction_id=transaction.transaction_id,
        account_id=transaction.account_id,
        amount=transaction.amount,
        currency=transaction.currency,
        transaction_type=transaction.transaction_type,
        channel=transaction.channel,
        status=transaction.status,
        timestamp=transaction.timestamp,
        created_at=transaction.created_at,
        risk_score=pred.final_risk_score if pred else None,
        risk_level=pred.risk_level if pred else None,
        fraud_probability=pred.fraud_probability if pred else None,
        anomaly_score=pred.anomaly_score if pred else None,
        rule_score=pred.rule_score if pred else None,
        model_version=pred.model_version_name if pred and pred.model_version_name else ("finguard-xgboost-v1.0.0" if pred else None),
        explanation_payload=pred.explanation_payload if pred else None,
        investigation_id=inv_id,
        investigation_status=inv_status,
    )


@router.post("/batch", response_model=BatchTransactionResponse, status_code=status.HTTP_201_CREATED)
async def ingest_batch_transactions(
    payload: BatchTransactionCreate,
    db: AsyncSession = Depends(get_db),
):
    batch_res = await TransactionService.ingest_batch(db, payload.transactions)
    items = []

    for tx in batch_res["transactions"]:
        pred_stmt = select(ModelPrediction).where(ModelPrediction.transaction_id == tx.id)
        pred_res = await db.execute(pred_stmt)
        pred = pred_res.scalars().first()

        items.append(
            TransactionResponse(
                id=tx.id,
                transaction_id=tx.transaction_id,
                account_id=tx.account_id,
                amount=tx.amount,
                currency=tx.currency,
                transaction_type=tx.transaction_type,
                channel=tx.channel,
                status=tx.status,
                timestamp=tx.timestamp,
                created_at=tx.created_at,
                risk_score=pred.final_risk_score if pred else None,
                risk_level=pred.risk_level if pred else None,
                fraud_probability=pred.fraud_probability if pred else None,
                anomaly_score=pred.anomaly_score if pred else None,
                rule_score=pred.rule_score if pred else None,
                model_version=pred.model_version_name if pred and pred.model_version_name else ("finguard-xgboost-v1.0.0" if pred else None),
                explanation_payload=pred.explanation_payload if pred else None,
            )
        )

    return BatchTransactionResponse(
        total_received=batch_res["total_received"],
        created=batch_res["created"],
        skipped_duplicates=batch_res["skipped_duplicates"],
        flagged_alerts=batch_res["flagged_alerts"],
        items=items,
    )


@router.get("", response_model=PaginatedResponse[TransactionResponse])
async def list_transactions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status (completed, flagged, blocked)"),
    search: Optional[str] = Query(None, description="Search by transaction ID or account ID"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level (low, medium, high, critical)"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum transaction amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum transaction amount"),
    sort_by: str = Query("timestamp", description="Sort by field: timestamp, amount"),
    sort_order: str = Query("desc", description="Sort order: asc, desc"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Transaction)
    count_stmt = select(func.count(Transaction.id))

    # Apply filters
    if status:
        stmt = stmt.where(Transaction.status == status)
        count_stmt = count_stmt.where(Transaction.status == status)

    if search:
        search_filter = or_(
            Transaction.transaction_id.ilike(f"%{search}%"),
            Transaction.account_id.ilike(f"%{search}%"),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    if min_amount is not None:
        stmt = stmt.where(Transaction.amount >= min_amount)
        count_stmt = count_stmt.where(Transaction.amount >= min_amount)

    if max_amount is not None:
        stmt = stmt.where(Transaction.amount <= max_amount)
        count_stmt = count_stmt.where(Transaction.amount <= max_amount)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar() or 0

    # Sorting
    sort_col = Transaction.timestamp
    if sort_by == "amount":
        sort_col = Transaction.amount

    if sort_order.lower() == "asc":
        stmt = stmt.order_by(asc(sort_col))
    else:
        stmt = stmt.order_by(desc(sort_col))

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    items = []
    for tx in transactions:
        pred_stmt = select(ModelPrediction).where(ModelPrediction.transaction_id == tx.id)
        pred_res = await db.execute(pred_stmt)
        pred = pred_res.scalars().first()

        # Filter by risk level if requested
        if risk_level and (not pred or pred.risk_level != risk_level.lower()):
            continue

        alert_stmt = select(Alert).where(Alert.transaction_id == tx.id)
        alert_res = await db.execute(alert_stmt)
        alert = alert_res.scalars().first()

        inv_id = None
        inv_status = None
        if alert:
            inv_stmt = select(Investigation).where(Investigation.alert_id == alert.id)
            inv_res = await db.execute(inv_stmt)
            inv = inv_res.scalars().first()
            if inv:
                inv_id = inv.id
                inv_status = inv.status

        items.append(
            TransactionResponse(
                id=tx.id,
                transaction_id=tx.transaction_id,
                account_id=tx.account_id,
                amount=tx.amount,
                currency=tx.currency,
                transaction_type=tx.transaction_type,
                channel=tx.channel,
                status=tx.status,
                timestamp=tx.timestamp,
                created_at=tx.created_at,
                risk_score=pred.final_risk_score if pred else None,
                risk_level=pred.risk_level if pred else None,
                fraud_probability=pred.fraud_probability if pred else None,
                anomaly_score=pred.anomaly_score if pred else None,
                rule_score=pred.rule_score if pred else None,
                model_version=pred.model_version_name if pred and pred.model_version_name else ("finguard-xgboost-v1.0.0" if pred else None),
                explanation_payload=pred.explanation_payload if pred else None,
                investigation_id=inv_id,
                investigation_status=inv_status,
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


@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Transaction).where((Transaction.id == id) | (Transaction.transaction_id == id))
    res = await db.execute(stmt)
    tx = res.scalars().first()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction {id} not found")

    pred_stmt = select(ModelPrediction).where(ModelPrediction.transaction_id == tx.id)
    pred_res = await db.execute(pred_stmt)
    pred = pred_res.scalars().first()

    alert_stmt = select(Alert).where(Alert.transaction_id == tx.id)
    alert_res = await db.execute(alert_stmt)
    alert = alert_res.scalars().first()

    inv_id = None
    inv_status = None
    if alert:
        inv_stmt = select(Investigation).where(Investigation.alert_id == alert.id)
        inv_res = await db.execute(inv_stmt)
        inv = inv_res.scalars().first()
        if inv:
            inv_id = inv.id
            inv_status = inv.status

    return TransactionResponse(
        id=tx.id,
        transaction_id=tx.transaction_id,
        account_id=tx.account_id,
        amount=tx.amount,
        currency=tx.currency,
        transaction_type=tx.transaction_type,
        channel=tx.channel,
        status=tx.status,
        timestamp=tx.timestamp,
        created_at=tx.created_at,
        risk_score=pred.final_risk_score if pred else None,
        risk_level=pred.risk_level if pred else None,
        fraud_probability=pred.fraud_probability if pred else None,
        anomaly_score=pred.anomaly_score if pred else None,
        rule_score=pred.rule_score if pred else None,
        model_version=pred.model_version_name if pred and pred.model_version_name else ("finguard-xgboost-v1.0.0" if pred else None),
        explanation_payload=pred.explanation_payload if pred else None,
        investigation_id=inv_id,
        investigation_status=inv_status,
    )
