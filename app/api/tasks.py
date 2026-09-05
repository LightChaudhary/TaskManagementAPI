from fastapi import APIRouter, status, HTTPException

from app.models.task import tasks, next_task_id
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate) -> TaskOut:
    global next_task_id

    new_task={
        "id": next_task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
    }

    tasks[next_task_id] = new_task
    next_task_id += 1

    return new_task

@router.get("", response_model=list[TaskOut])
def get_tasks() -> list[TaskOut]:
    return list(tasks.values())

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int) -> TaskOut:
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    return task

