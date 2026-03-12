from typing import Dict, Optional
from ..models.schemas import ProcessResponse

class StateManager:
    def __init__(self):
        # In-memory store: {request_id: ProcessResponse}
        self._store: Dict[str, ProcessResponse] = {}

    def get_request_state(self, request_id: str) -> Optional[ProcessResponse]:
        return self._store.get(request_id)

    def save_request_state(self, request_id: str, state: ProcessResponse):
        self._store[request_id] = state
