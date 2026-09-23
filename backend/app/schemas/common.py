from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Stable machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    request_id: Optional[str] = Field(None, description="Correlated request identifier")
    details: Optional[Dict[str, Any]] = Field(None, description="Optional field errors or diagnostics")


class StatusResponse(BaseModel):
    status: str = Field(default="ok", description="Status code")
    message: str = Field(default="Operation completed successfully", description="Status message")
    timestamp: str = Field(..., description="ISO formatted UTC timestamp")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T] = Field(..., description="Page items")
    total: int = Field(..., description="Total count matching filter")
    page: int = Field(default=1, description="Current page number (1-indexed)")
    page_size: int = Field(default=20, description="Items per page")
    total_pages: int = Field(..., description="Total available pages")
