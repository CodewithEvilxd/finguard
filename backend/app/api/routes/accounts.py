import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_db
from app.models.entity import Account
from app.models.transaction import Transaction
from app.models.ml import ModelPrediction
from app.schemas.account import AccountResponse, AccountRiskProfile
from app.schemas.common import PaginatedResponse
from app.schemas.transaction import TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=PaginatedResponse[AccountResponse])
async def list_accounts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by account number or holder name"),
    risk_tier: Optional[str] = Query(None, description="Filter by risk tier (standard, elevated, high_risk)"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Account)
    count_stmt = select(func.count(Account.id))

    if search:
        search_filter = (Account.account_number.ilike(f"%{search}%")) | (Account.account_holder.ilike(f"%{search}%"))
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    if risk_tier:
        stmt = stmt.where(Account.risk_tier == risk_tier)
        count_stmt = count_stmt.where(Account.risk_tier == risk_tier)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(desc(Account.created_at)).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    accounts = result.scalars().all()

    items = [
        AccountResponse(
            id=acc.id,
            account_number=acc.account_number,
            account_holder=acc.account_holder,
            balance=acc.balance,
            currency=acc.currency,
            risk_tier=acc.risk_tier,
            status=acc.status,
            created_at=acc.created_at,
        )
        for acc in accounts
    ]

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{id}", response_model=AccountResponse)
async def get_account(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Account).where((Account.id == id) | (Account.account_number == id))
    res = await db.execute(stmt)
    acc = res.scalars().first()
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account {id} not found")

    return AccountResponse(
        id=acc.id,
        account_number=acc.account_number,
        account_holder=acc.account_holder,
        balance=acc.balance,
        currency=acc.currency,
        risk_tier=acc.risk_tier,
        status=acc.status,
        created_at=acc.created_at,
    )


@router.get("/{id}/risk", response_model=AccountRiskProfile)
async def get_account_risk(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    profile = await TransactionService.get_account_risk_profile(db, id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account {id} not found")
    return AccountRiskProfile(**profile)


@router.get("/{id}/transactions", response_model=PaginatedResponse[TransactionResponse])
async def get_account_transactions(
    id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    acc_stmt = select(Account).where((Account.id == id) | (Account.account_number == id))
    acc_res = await db.execute(acc_stmt)
    acc = acc_res.scalars().first()
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account {id} not found")

    stmt = select(Transaction).where(Transaction.account_id == acc.id)
    count_stmt = select(func.count(Transaction.id)).where(Transaction.account_id == acc.id)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(desc(Transaction.timestamp)).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    items = []
    for tx in transactions:
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
                model_version=pred.model_version if pred else None,
                explanation_payload=pred.explanation_payload if pred else None,
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
