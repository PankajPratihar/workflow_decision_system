import json
from typing import Any, Dict, Optional
from ..models.schemas import WorkflowAction

class RulesEngine:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def evaluate(self, workflow_id: str, payload: Dict[str, Any]) -> tuple[WorkflowAction, Optional[str]]:
        workflow = next((w for w in self.config['workflows'] if w['id'] == workflow_id), None)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        for rule in workflow['rules']:
            if self._check_condition(rule['condition'], payload):
                return WorkflowAction(rule['action']), rule.get('reason')
        
        return WorkflowAction.MANUAL_REVIEW, "No matching rules"

    def _check_condition(self, condition: str, payload: Dict[str, Any]) -> bool:
        try:
            # Using eval for simple conditions. In production, use a safe expression parser.
            return eval(condition, {"__builtins__": None}, payload)
        except Exception:
            return False
