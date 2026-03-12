from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict
from enum import Enum

class WorkflowAction(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    RETRY = "retry"
    MANUAL_REVIEW = "manual_review"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProcessRequest(BaseModel):
    request_id: str = Field(..., description="Unique ID for idempotency")
    workflow_id: str
    payload: Dict[str, Any]

class AuditLogEntry(BaseModel):
    timestamp: str
    stage: str
    details: str

class ProcessResponse(BaseModel):
    request_id: str
    status: WorkflowStatus
    action: Optional[WorkflowAction] = None
    reason: Optional[str] = None
    audit_trail: List[AuditLogEntry] = []
