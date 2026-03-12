from datetime import datetime
from ..models.schemas import AuditLogEntry

class AuditLogger:
    def __init__(self):
        self.logs = []

    def log(self, stage: str, details: str):
        entry = AuditLogEntry(
            timestamp=datetime.utcnow().isoformat(),
            stage=stage,
            details=details
        )
        self.logs.append(entry)
        print(f"[{entry.timestamp}] {stage}: {details}")

    def get_logs(self):
        return self.logs
