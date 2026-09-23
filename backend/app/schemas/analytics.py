from typing import List
from pydantic import BaseModel, Field


class OverviewMetrics(BaseModel):
    total_transactions_24h: int = Field(default=0, description="Total transactions in the last 24h")
    active_alerts_count: int = Field(default=0, description="Currently unresolved alerts")
    high_risk_count: int = Field(default=0, description="High risk alerts")
    critical_risk_count: int = Field(default=0, description="Critical risk alerts requiring immediate action")
    pending_investigations: int = Field(default=0, description="Open investigations")
    resolved_today: int = Field(default=0, description="Investigations resolved today")
    mean_resolution_hours: float = Field(default=0.0, description="Average time to resolution")


class RiskTrendPoint(BaseModel):
    timestamp_label: str = Field(..., description="Hourly or daily bucket label")
    low_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    high_count: int = Field(default=0)
    critical_count: int = Field(default=0)


class RiskTrendResponse(BaseModel):
    period: str = Field(default="7d", description="Time window for trends: 24h, 7d, 30d")
    trend_points: List[RiskTrendPoint] = Field(default=[], description="Series of trend points")
