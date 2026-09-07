from fastapi import FastAPI
from app.api.tasks import router as task_router

from app.database import Base, engine
from app.models.task import Task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SWE Project")

@app.get("/")
def root()->dict:
    return {"message": "Hello!, Prakash"}

app.include_router(task_router)