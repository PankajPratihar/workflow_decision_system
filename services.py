import asyncio
import random
from datetime import datetime
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from db_models import RequestDB, AuditLogDB, ProcessedRequestDB
from models import WorkflowRequest, WorkflowResponse, WorkflowStatus, AuditLog

class WorkflowService:
    async def process_workflow(self, db: Session, request: WorkflowRequest) -> WorkflowResponse:
        # 1. Idempotency Check (Database lookup in processed_requests)
        processed = db.query(ProcessedRequestDB).filter(ProcessedRequestDB.request_id == request.request_id).first()
        
        if processed:
            # If processed, find the original request
            db_request = db.query(RequestDB).filter(RequestDB.request_id == request.request_id).first()
            if db_request:
                self._log_event_db(db, db_request.id, "IDEMPOTENCY_HIT", "Duplicate request detected in processed_requests. Returning cached result.")
                return self._map_to_response(db_request)

        # 2. Initialize Database Record
        db_request = RequestDB(
            request_id=request.request_id,
            status=WorkflowStatus.PENDING.value,
            payload=request.payload
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        
        self._log_event_db(db, db_request.id, "WORKFLOW_STARTED", "Starting processing for request.")

        # 3. Execute External Call with Retry Logic
        success = await self._execute_with_retry(db, db_request)

        if success:
            db_request.status = WorkflowStatus.APPROVED.value
            db_request.result = {"message": "External processing successful"}
            self._log_event_db(db, db_request.id, "WORKFLOW_COMPLETED", "Request approved after successful external call.")
        else:
            # 4. Fallback to Manual Review if all retries fail
            db_request.status = WorkflowStatus.MANUAL_REVIEW.value
            db_request.result = {"message": "External call failed after multiple attempts. Routed to human review."}
            self._log_event_db(db, db_request.id, "FALLBACK_TRIGGERED", "Max retries reached. Routing to manual review.")

        # 5. Mark as processed
        processed_entry = ProcessedRequestDB(request_id=request.request_id)
        db.add(processed_entry)
        
        db.commit()
        db.refresh(db_request)
        return self._map_to_response(db_request)

    async def _execute_with_retry(self, db: Session, db_request: RequestDB, max_retries: int = 3) -> bool:
        """Simulates an external call with retry logic."""
        for attempt in range(1, max_retries + 1):
            self._log_event_db(db, db_request.id, "EXTERNAL_CALL_ATTEMPT", f"Attempt {attempt} of {max_retries}")
            
            try:
                # Simulate external call
                if await self._call_external_dependency():
                    self._log_event_db(db, db_request.id, "EXTERNAL_CALL_SUCCESS", "External dependency responded successfully.")
                    return True
                else:
                    raise Exception("External service returned error status.")
            
            except Exception as e:
                self._log_event_db(db, db_request.id, "EXTERNAL_CALL_FAILURE", f"Attempt {attempt} failed: {str(e)}")
                if attempt < max_retries:
                    wait_time = attempt * 1 
                    self._log_event_db(db, db_request.id, "RETRY_WAIT", f"Waiting {wait_time}s before next attempt.")
                    await asyncio.sleep(wait_time)
        
        return False

    async def _call_external_dependency(self) -> bool:
        """Simulates an external API call."""
        await asyncio.sleep(0.5)
        return random.random() > 0.7

    def _log_event_db(self, db: Session, db_request_id: int, event: str, details: str):
        audit_log = AuditLogDB(
            request_id_internal=db_request_id,
            event=event,
            details=details
        )
        db.add(audit_log)
        db.commit()

    def _map_to_response(self, db_request: RequestDB) -> WorkflowResponse:
        return WorkflowResponse(
            request_id=db_request.request_id,
            status=WorkflowStatus(db_request.status),
            result=db_request.result,
            audit_trail=[
                AuditLog(
                    timestamp=log.timestamp.isoformat(),
                    event=log.event,
                    details=log.details
                ) for log in db_request.audit_logs
            ]
        )

# Singleton instance
workflow_service = WorkflowService()
