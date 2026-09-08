import pytest

from app.database import SessionLocal
from app.models.task import Task


@pytest.fixture(autouse=True)
def reset_tasks():
    db = SessionLocal()

    db.query(Task).delete()

    task1 = Task(
        title="learn rest",
        description="understand http methods and status codes.",
        status="todo",
        priority="high",
    )

    task2 = Task(
        title="learn git branches",
        description="practice feature branches and merging",
        status="todo",
        priority="medium",
    )

    db.add_all([task1, task2])
    db.commit()

    yield

    db.close()
