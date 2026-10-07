from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.task import TaskRepository
from app.services.task import TaskService

def get_task_service(db:Session = Depends(get_db),) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)

