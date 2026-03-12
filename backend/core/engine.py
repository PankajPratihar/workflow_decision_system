from ..models.schemas import ProcessRequest, ProcessResponse, WorkflowStatus, WorkflowAction
from ..services.state_manager import StateManager
from ..services.audit_logger import AuditLogger
from .rules import RulesEngine

class WorkflowEngine:
    def __init__(self, state_manager: StateManager, rules_engine: RulesEngine):
        self.state_manager = state_manager
        self.rules_engine = rules_engine

    async def process(self, request: ProcessRequest) -> ProcessResponse:
        # 1. Idempotency Check
        existing = self.state_manager.get_request_state(request.request_id)
        if existing:
            return existing

        # 2. Initialize
        logger = AuditLogger()
        logger.log("START", f"Processing workflow {request.workflow_id}")
        
        response = ProcessResponse(
            request_id=request.request_id,
            status=WorkflowStatus.PROCESSING,
            audit_trail=logger.get_logs()
        )
        self.state_manager.save_request_state(request.request_id, response)

        try:
            # 3. Evaluate Rules
            action, reason = self.rules_engine.evaluate(request.workflow_id, request.payload)
            logger.log("DECISION", f"Action: {action}, Reason: {reason}")

            # 4. Handle Action (Simplified)
            if action == WorkflowAction.RETRY:
                logger.log("RETRY", "Simulating external dependency retry...")
            
            # 5. Finalize
            response.status = WorkflowStatus.COMPLETED
            response.action = action
            response.reason = reason
            response.audit_trail = logger.get_logs()
            
            logger.log("END", "Workflow completed")
            
        except Exception as e:
            logger.log("ERROR", str(e))
            response.status = WorkflowStatus.FAILED
            response.reason = str(e)
            response.audit_trail = logger.get_logs()

        self.state_manager.save_request_state(request.request_id, response)
        return response
