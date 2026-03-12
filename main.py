from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import WorkflowRequest, WorkflowResponse
from services import workflow_service
from database import engine, Base, get_db
import db_models

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQL-Backed Idempotent Workflow System")

@app.post("/process_request", response_model=WorkflowResponse)
async def process_request(request: WorkflowRequest, db: Session = Depends(get_db)):
    """
    Endpoint to process a workflow request with SQL-backed idempotency and retry logic.
    """
    try:
        result = await workflow_service.process_workflow(db, request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
