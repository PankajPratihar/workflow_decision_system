from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

class WorkflowOutcome(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    RETRY = "retry"
    MANUAL_REVIEW = "manual_review"

class WorkflowStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"

@dataclass
class AuditLog:
    stage: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    details: str = ""

@dataclass
class WorkflowRequest:
    request_id: str
    payload: Dict[str, Any]
    workflow_type: str = "default"

@dataclass
class WorkflowResult:
    request_id: str
    outcome: Optional[WorkflowOutcome] = None
    status: WorkflowStatus = WorkflowStatus.IN_PROGRESS
    audit_trail: List[AuditLog] = field(default_factory=list)
    error_message: Optional[str] = None
