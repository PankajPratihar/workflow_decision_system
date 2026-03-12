import logging
from typing import Tuple, Optional
from workflow_models import WorkflowRequest, WorkflowResult, WorkflowOutcome, WorkflowStatus, AuditLog

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowEngine")

class WorkflowEngine:
    """
    Modular Workflow Engine that executes stages sequentially.
    Stages: request_received -> validation -> rule_evaluation -> decision_stage
    """

    def __init__(self):
        self.stages = [
            self.stage_request_received,
            self.stage_validation,
            self.stage_rule_evaluation,
            self.stage_decision_stage
        ]

    async def run(self, request: WorkflowRequest) -> WorkflowResult:
        result = WorkflowResult(request_id=request.request_id)
        
        logger.info(f"Starting workflow for request: {request.request_id}")

        try:
            for stage_func in self.stages:
                stage_name = stage_func.__name__.replace("stage_", "")
                logger.info(f"Executing stage: {stage_name}")
                
                # Execute the stage
                success, details, outcome = await stage_func(request, result)
                
                # Record audit log
                result.audit_trail.append(AuditLog(stage=stage_name, details=details))
                
                if not success:
                    result.status = WorkflowStatus.FAILED
                    result.error_message = details
                    logger.error(f"Workflow failed at stage {stage_name}: {details}")
                    break
                
                if outcome:
                    result.outcome = outcome
                    # If an outcome is reached, we might stop or continue depending on logic
                    # For this engine, we continue to decision_stage if not already there
                    if stage_name == "decision_stage":
                        result.status = WorkflowStatus.SUCCESS
                        break

        except Exception as e:
            logger.exception("Unexpected error in workflow execution")
            result.status = WorkflowStatus.FAILED
            result.error_message = str(e)
            result.audit_trail.append(AuditLog(stage="system_error", details=str(e)))

        logger.info(f"Workflow finished for {request.request_id} with outcome: {result.outcome}")
        return result

    async def stage_request_received(self, request: WorkflowRequest, result: WorkflowResult) -> Tuple[bool, str, Optional[WorkflowOutcome]]:
        """Initial stage to acknowledge receipt."""
        return True, "Request successfully received and queued", None

    async def stage_validation(self, request: WorkflowRequest, result: WorkflowResult) -> Tuple[bool, str, Optional[WorkflowOutcome]]:
        """Validate the input payload."""
        payload = request.payload
        if not payload:
            return False, "Empty payload", None
        
        required_fields = ["amount", "user_id"]
        missing = [f for f in required_fields if f not in payload]
        
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}", None
            
        return True, "Payload validation passed", None

    async def stage_rule_evaluation(self, request: WorkflowRequest, result: WorkflowResult) -> Tuple[bool, str, Optional[WorkflowOutcome]]:
        """Evaluate business rules to determine preliminary outcome."""
        amount = request.payload.get("amount", 0)
        
        # Mock rule logic
        if amount < 0:
            return True, "Negative amount detected", WorkflowOutcome.REJECT
        elif amount > 10000:
            return True, "High value transaction", WorkflowOutcome.MANUAL_REVIEW
        elif amount == 404:
            return True, "Simulated system timeout", WorkflowOutcome.RETRY
        else:
            return True, "Standard transaction", WorkflowOutcome.APPROVE

    async def stage_decision_stage(self, request: WorkflowRequest, result: WorkflowResult) -> Tuple[bool, str, Optional[WorkflowOutcome]]:
        """Final stage to confirm and persist the decision."""
        if not result.outcome:
            return False, "No outcome determined in previous stages", None
            
        return True, f"Final decision confirmed: {result.outcome}", result.outcome
