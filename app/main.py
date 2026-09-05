from fastapi import FastAPI

from app.api.tasks import router as task_router

app = FastAPI(title="SWE Project")

@app.get("/")
def root()->dict:
    return {"message": "Hello!, Prakash"}

app.include_router(task_router)