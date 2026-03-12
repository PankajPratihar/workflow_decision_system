from fastapi import APIRouter, HTTPException
from ..models.schemas import ProcessRequest, ProcessResponse
from ..core.engine import WorkflowEngine
from ..services.state_manager import StateManager
from ..core.rules import RulesEngine
import os

router = APIRouter()

# Dependency Injection setup
state_manager = StateManager()
config_path = os.path.join(os.path.dirname(__file__), "..", "config", "workflow_config.json")
rules_engine = RulesEngine(config_path)
engine = WorkflowEngine(state_manager, rules_engine)

@router.post("/process_request", response_model=ProcessResponse)
async def process_request(request: ProcessRequest):
    try:
        return await engine.process(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
