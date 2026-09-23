from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AlertResponse(BaseModel):
    id: str
    transaction_id: str
    risk_score: float
    risk_level: str
    status: str
    trigger_reason: str
    factors_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    transaction_amount: Optional[float] = None
    transaction_currency: Optional[str] = None
    account_id: Optional[str] = None

    model_config = {"from_attributes": True}


class AlertUpdate(BaseModel):
    status: str = Field(..., description="Target status: new, investigating, confirmed_fraud, false_positive, dismissed")
    notes: Optional[str] = Field(None, description="Optional note for status transition")
