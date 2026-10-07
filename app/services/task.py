from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatus, Priority

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_data: TaskCreate) -> Task:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status.value,
            priority=task_data.priority.value,
        )

        return self.repository.create(task)

    def get_tasks(
        self,
        status: TaskStatus | None = None,
        priority: Priority | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Task]:
        return self.repository.get_all(
            status=status.value if status else None,
            priority=priority.value if priority else None,
            skip=skip,
            limit=limit,
        )

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def update_task(self, task_id: int, task_data: TaskUpdate,) -> Task | None:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return None

        task.title = task_data.title
        task.description = task_data.description
        task.status = task_data.status.value
        task.priority = task_data.priority.value

        return self.repository.update(task)

    def delete_task(self, task_id: int) -> bool:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return False

        self.repository.delete(task)
        return True

    