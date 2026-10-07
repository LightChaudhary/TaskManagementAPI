from fastapi import HTTPException

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatus, Priority

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_data: TaskCreate, owner_id: int,) -> Task:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status.value,
            priority=task_data.priority.value,
            owner_id=owner_id,
        )

        return self.repository.create(task)

    def get_tasks(
        self,
        owner_id: int,
        status: TaskStatus | None = None,
        priority: Priority | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Task]:
        return self.repository.get_all(
            owner_id=owner_id,
            status=status.value if status else None,
            priority=priority.value if priority else None,
            skip=skip,
            limit=limit,
        )

    def get_task(self, task_id: int, owner_id: int) -> Task:
        task = self.repository.get_by_id(task_id, owner_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="task not found!",
            )

        return task

    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: int,
    ) -> Task:
        task = self.repository.get_by_id(task_id, owner_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="task not found!",
            )

        task.title = task_data.title
        task.description = task_data.description
        task.status = task_data.status.value
        task.priority = task_data.priority.value

        return self.repository.update(task)

    def delete_task(
        self,
        task_id: int,
        owner_id: int,
    ) -> None:
        task = self.repository.get_by_id(task_id, owner_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="task not found!",
            )

        self.repository.delete(task)

    