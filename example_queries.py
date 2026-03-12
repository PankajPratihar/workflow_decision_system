from sqlalchemy.orm import Session
from database import SessionLocal
from db_models import RequestDB, AuditLogDB, ProcessedRequestDB

def run_queries():
    db = SessionLocal()
    try:
        print("--- All Requests ---")
        requests = db.query(RequestDB).all()
        for r in requests:
            print(f"ID: {r.request_id}, Status: {r.status}, Created: {r.created_at}")

        print("\n--- Audit Logs for a specific request ---")
        if requests:
            first_req = requests[0]
            logs = db.query(AuditLogDB).filter(AuditLogDB.request_id_internal == first_req.id).all()
            for l in logs:
                print(f"[{l.timestamp}] {l.event}: {l.details}")

        print("\n--- Processed Request IDs ---")
        processed = db.query(ProcessedRequestDB).all()
        for p in processed:
            print(f"Request ID: {p.request_id}, Processed At: {p.processed_at}")

        print("\n--- Requests needing Manual Review ---")
        manual = db.query(RequestDB).filter(RequestDB.status == "manual_review").all()
        for m in manual:
            print(f"ID: {m.request_id}, Payload: {m.payload}")

    finally:
        db.close()

if __name__ == "__main__":
    run_queries()
