from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., description="Unique client idempotency/business identifier")
    account_id: str = Field(..., description="Account identifier")
    amount: float = Field(..., gt=0, description="Positive transaction amount")
    currency: str = Field(default="USD", min_length=3, max_length=3, description="ISO-4217 currency code")
    transaction_type: str = Field(..., description="Transaction type: wire, transfer, purchase, withdrawal")
    channel: str = Field(default="web", description="Channel: web, mobile, atm, api, pos")
    timestamp: Optional[datetime] = Field(default=None, description="Transaction timestamp in UTC")

    beneficiary_name: Optional[str] = Field(None, description="Optional beneficiary name")
    beneficiary_account: Optional[str] = Field(None, description="Optional beneficiary account number")
    vendor_name: Optional[str] = Field(None, description="Optional vendor name")
    device_fingerprint: Optional[str] = Field(None, description="Optional device fingerprint")
    ip_address: Optional[str] = Field(None, description="Optional client IP address")
    country: Optional[str] = Field(default="US", min_length=2, max_length=2, description="2-letter country code")


class TransactionResponse(BaseModel):
    id: str
    transaction_id: str
    account_id: str
    amount: float
    currency: str
    transaction_type: str
    channel: str
    status: str
    timestamp: datetime
    created_at: datetime

    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    fraud_probability: Optional[float] = None
    anomaly_score: Optional[float] = None
    rule_score: Optional[float] = None
    model_version: Optional[str] = None
    explanation_payload: Optional[str] = None
    investigation_id: Optional[str] = None
    investigation_status: Optional[str] = None

    model_config = {"from_attributes": True}


class BatchTransactionCreate(BaseModel):
    transactions: List[TransactionCreate] = Field(..., max_length=1000, description="List of transactions to ingest")


class BatchTransactionResponse(BaseModel):
    total_received: int
    created: int
    skipped_duplicates: int
    flagged_alerts: int
    items: List[TransactionResponse]
