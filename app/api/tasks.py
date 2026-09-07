from fastapi import APIRouter, status, HTTPException

from app.models.task import Task
from app.database import SessionLocal
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate) -> TaskOut:
    db = SessionLocal()

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()

    return new_task

@router.get("", response_model=list[TaskOut])
def get_tasks() -> list[TaskOut]:
    db = SessionLocal()

    tasks = db.query(Task).all()

    db.close()

    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int) -> TaskOut:
    db = SessionLocal()

    task = db.get(Task, task_id)

    if task is None:
        db.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    db.close()

    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate) -> TaskOut:
    db = SessionLocal()

    existing_task = db.get(Task, task_id)

    if existing_task is None:
        db.close()

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
    db.close()


    return existing_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_task(task_id: int) -> None:
    db = SessionLocal()

    task = db.get(Task, task_id)

    if task is None:
        db.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found!",
        )

    db.delete(task)
    db.commit()
    db.close()
