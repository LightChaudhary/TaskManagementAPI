from fastapi import APIRouter, status, Depends, Query
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate, TaskStatus, Priority

from app.services.task import TaskService
from app.dependencies import get_task_service, get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    return service.create_task(task, current_user.id)

@router.get("", response_model=list[TaskOut])
def get_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority_filter: Priority | None = Query(default=None, alias="priority"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> list[TaskOut]:
    return service.get_tasks(
        owner_id=current_user.id,
        status=status_filter,
        priority=priority_filter,
        skip=skip,
        limit=limit,
    )

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    return service.get_task(task_id, current_user.id)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    return service.update_task(
        task_id,
        task,
        current_user.id,
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.delete_task(task_id, current_user.id)
