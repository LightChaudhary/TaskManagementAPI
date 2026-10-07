from fastapi import FastAPI
from app.api.tasks import router as task_router
from app.api.auth import router as auth_router

app = FastAPI(title="SWE Project")

@app.get("/")
def root()->dict:
    return {"message": "Hello!, Prakash"}

app.include_router(task_router)
app.include_router(auth_router)