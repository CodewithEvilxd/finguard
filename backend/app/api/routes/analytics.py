from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_db
from app.models.transaction import Transaction
from app.models.alert import Alert, Investigation
from app.schemas.analytics import OverviewMetrics, RiskTrendPoint, RiskTrendResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=OverviewMetrics)
async def get_overview_metrics(db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(hours=24)

    # Total transactions last 24h
    tx_count_stmt = select(func.count(Transaction.id)).where(Transaction.timestamp >= yesterday)
    tx_res = await db.execute(tx_count_stmt)
    total_tx = tx_res.scalar() or 0

    # Active alerts
    alert_active_stmt = select(func.count(Alert.id)).where(Alert.status.in_(["new", "investigating"]))
    alert_res = await db.execute(alert_active_stmt)
    active_alerts = alert_res.scalar() or 0

    # Risk level counts
    high_stmt = select(func.count(Alert.id)).where(Alert.risk_level == "high", Alert.status != "dismissed")
    high_res = await db.execute(high_stmt)
    high_alerts = high_res.scalar() or 0

    crit_stmt = select(func.count(Alert.id)).where(Alert.risk_level == "critical", Alert.status != "dismissed")
    crit_res = await db.execute(crit_stmt)
    crit_alerts = crit_res.scalar() or 0

    # Pending investigations
    inv_stmt = select(func.count(Investigation.id)).where(Investigation.status.in_(["open", "under_review"]))
    inv_res = await db.execute(inv_stmt)
    pending_inv = inv_res.scalar() or 0

    # Resolved today
    resolved_stmt = select(func.count(Investigation.id)).where(
        Investigation.status.in_(["cleared", "confirmed_fraud", "escalated"]),
        Investigation.updated_at >= yesterday,
    )
    resolved_res = await db.execute(resolved_stmt)
    resolved_today = resolved_res.scalar() or 0

    return OverviewMetrics(
        total_transactions_24h=total_tx,
        active_alerts_count=active_alerts,
        high_risk_count=high_alerts,
        critical_risk_count=crit_alerts,
        pending_investigations=pending_inv,
        resolved_today=resolved_today,
        mean_resolution_hours=2.4,
    )


@router.get("/risk-trend", response_model=RiskTrendResponse)
async def get_risk_trend(
    period: str = Query("7d", pattern="^(24h|7d|30d)$"),
    db: AsyncSession = Depends(get_db),
):
    days = 7 if period == "7d" else (1 if period == "24h" else 30)
    now = datetime.now(timezone.utc)
    points = []

    # Aggregate in daily buckets
    for i in range(days - 1, -1, -1):
        bucket_date = now - timedelta(days=i)
        label = bucket_date.strftime("%b %d")
        # In a real environment, query daily group by; here compute per day interval
        day_start = bucket_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        stmt = (
            select(Alert.risk_level, func.count(Alert.id))
            .where(Alert.created_at >= day_start, Alert.created_at < day_end)
            .group_by(Alert.risk_level)
        )
        res = await db.execute(stmt)
        counts = dict(res.all())

        points.append(
            RiskTrendPoint(
                timestamp_label=label,
                low_count=counts.get("low", 0),
                medium_count=counts.get("medium", 0),
                high_count=counts.get("high", 0),
                critical_count=counts.get("critical", 0),
            )
        )

    return RiskTrendResponse(period=period, trend_points=points)


@router.get("/retraining-status")
async def get_model_retraining_status():
    """Returns the 12-hour automated model retraining status from the ML service."""
    from app.services.ml_client import ml_client

    return await ml_client.get_training_status()


@router.post("/trigger-retrain")
async def trigger_model_retrain():
    """Triggers an immediate model retraining run on the ML service."""
    from app.services.ml_client import ml_client

    return await ml_client.trigger_retraining()
