from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AccountResponse(BaseModel):
    id: str
    account_number: str
    account_holder: str
    balance: float
    currency: str
    risk_tier: str
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AccountRiskProfile(BaseModel):
    account_id: str
    account_internal_id: str
    holder_name: str
    balance: float
    currency: str
    risk_tier: str
    total_transactions: int
    total_spend: float
    average_transaction_amount: float
    max_transaction_amount: float
    average_risk_score: float
    peak_risk_score: float
    high_risk_transactions_count: int
    total_alerts_count: int
    created_at: Optional[str] = None
