import pytest

from app.models import task as task_model


@pytest.fixture(autouse=True)
def reset_tasks():
    task_model.tasks.clear()

    task_model.tasks.update(
        {
            1:{
                "id": 1,
                "title": "learn rest",
                "description": "understand http methods and status codes.",
                "status": "todo",
                "priority": "high",
            },
            2:{
                "id": 2,
                "title": "learn git branches",
                "description": "practice feature branches and merging",
                "status": "todo",
                "priority": "medium",
            },
        }
    )

    task_model.next_task_id = 3
