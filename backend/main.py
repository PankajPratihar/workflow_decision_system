from fastapi import FastAPI
from .api.routes import router

app = FastAPI(title="Workflow Decision Platform")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
