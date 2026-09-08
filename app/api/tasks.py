from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.task import Task
from app.database import get_db
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskOut:
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)) -> list[TaskOut]:
    tasks = db.query(Task).all()

    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db),) -> TaskOut:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)) -> TaskOut:
    existing_task = db.get(Task, task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status.value
    existing_task.priority = task.priority.value

    db.commit()
    db.refresh(existing_task)

    return existing_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    db.delete(task)
    db.commit()
