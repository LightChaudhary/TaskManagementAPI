from fastapi import APIRouter, status, HTTPException, Depends

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

from app.services.task import TaskService
from app.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service),) -> TaskOut:
    return service.create_task(task)

@router.get("", response_model=list[TaskOut])
def get_tasks(service: TaskService = Depends(get_task_service),) -> list[TaskOut]:
    return service.get_tasks()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, service: TaskService = Depends(get_task_service),) -> TaskOut:
    task = service.get_task(task_id)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, service: TaskService = Depends(get_task_service),) -> TaskOut:

    updated_task = service.update_task(task_id, task)

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service),) -> None:

    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )
