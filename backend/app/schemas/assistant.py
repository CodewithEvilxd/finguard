from typing import List, Optional
from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    document_title: str = Field(..., description="Title of the retrieved reference document")
    document_category: str = Field(..., description="Category: policy, regulation, standard_operating_procedure")
    section_title: Optional[str] = Field(None, description="Section or article heading")
    relevance_score: float = Field(..., description="Cosine similarity relevance score")
    excerpt: str = Field(..., description="Extracted textual evidence snippet")


class AssistantQuery(BaseModel):
    query: str = Field(..., min_length=3, description="Analyst query question")
    transaction_id: Optional[str] = Field(None, description="Optional associated transaction identifier")
    alert_id: Optional[str] = Field(None, description="Optional associated alert identifier")


class AssistantResponse(BaseModel):
    query_id: str
    response_text: str = Field(..., description="Grounded AI response")
    sources: List[SourceReference] = Field(default=[], description="Retrieved citations from approved knowledge base")
    limitations: Optional[str] = Field(None, description="Explicit statement of any missing facts or constraints")
    disclaimer: str = Field(
        default="AI-generated assistance grounded in approved documents. Final decision must be verified by an analyst.",
        description="Standard fintech compliance disclaimer",
    )
