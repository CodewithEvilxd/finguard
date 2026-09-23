from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.alert import AlertResponse


class InvestigationNoteResponse(BaseModel):
    id: str
    author_id: Optional[str] = None
    note_type: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class InvestigationCreate(BaseModel):
    alert_id: str = Field(..., description="ID of the alert to open an investigation for")
    priority: str = Field(default="high", description="Priority: low, medium, high, urgent")
    initial_notes: Optional[str] = Field(None, description="Initial observation notes")


class InvestigationDecision(BaseModel):
    decision: str = Field(..., description="Analyst decision: cleared, confirmed_fraud, escalated, monitor")
    rationale: str = Field(..., min_length=10, description="Audit-trailed justification for decision")


class InvestigationResponse(BaseModel):
    id: str
    alert_id: str
    assigned_analyst_id: Optional[str] = None
    status: str
    priority: str
    decision: Optional[str] = None
    decision_rationale: Optional[str] = None
    decided_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    alert: Optional[AlertResponse] = None
    notes: List[InvestigationNoteResponse] = []

    model_config = {"from_attributes": True}
