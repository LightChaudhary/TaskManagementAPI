from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.base import TaskRepositoryInterface

class TaskRepository(TaskRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all(self, status: str|None = None,
                priority:str| None=None,
                skip:int = 0,
                limit:int = 20,) -> list[Task]:
        query = self.db.query(Task)

        if status is not None:
            query = query.filter(Task.status == status)

        if priority is not None:
            query = query.filter(Task.priority == priority)

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

    