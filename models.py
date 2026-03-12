from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
from enum import Enum
from datetime import datetime

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"
    FAILED = "failed"

class WorkflowRequest(BaseModel):
    request_id: str = Field(..., description="Unique ID for idempotency")
    payload: Dict[str, Any]

class AuditLog(BaseModel):
    timestamp: str
    event: str
    details: str

class WorkflowResponse(BaseModel):
    request_id: str
    status: WorkflowStatus
    result: Optional[Dict[str, Any]] = None
    audit_trail: List[AuditLog] = []
