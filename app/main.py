from fastapi import FastAPI, status, HTTPException
from app.models import Task, TaskCreate, TaskUpdate

app = FastAPI(title="SWE project")

tasks = [
    {
        "id": 1,
        "title": "learn rest",
        "description": "understand http methods and status codes.",
        "completed": False,
        "priority": "high",
    },
    {
        "id" : 2,
        "title": "learn git branches",
        "description": "practice feature branches and merging",
        "completed": False,
        "priority": "medium",
    },
]

@app.get("/")
def root() -> dict:
    return {"message" : "Hello!, Prakash"}

@app.get("/tasks", response_model=list[Task])
def get_tasks() -> list[Task]:
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="task not found!",
    )

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    new_task = {
        "id" : len(tasks) + 1,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority,
    }
    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate) -> Task:
    for existing_task in tasks:
        if existing_task["id"] == task_id:
            existing_task["title"] = task.title
            existing_task["description"] = task.description
            existing_task["completed"] = task.completed
            existing_task["priority"] = task.priority

            return existing_task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="task not found!",
    )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="task not found!",
    )