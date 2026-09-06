from fastapi import APIRouter, status, HTTPException

from app.models import task as task_model
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate) -> TaskOut:
    new_task = {
        "id": task_model.next_task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
    }

    task_model.tasks[task_model.next_task_id] = new_task
    task_model.next_task_id += 1

    return new_task

@router.get("", response_model=list[TaskOut])
def get_tasks() -> list[TaskOut]:
    return list(task_model.tasks.values())

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int) -> TaskOut:
    task = task_model.tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate) -> TaskOut:
    existing_task = task_model.tasks.get(task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    existing_task.update(
        {
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
        }
    )

    return existing_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_task(task_id: int) -> None:
    task = task_model.tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    del task_model.tasks[task_id]
