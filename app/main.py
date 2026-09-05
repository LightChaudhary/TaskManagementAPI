from fastapi import FastAPI, status, HTTPException
from app.models import Task, TaskCreate

app = FastAPI(title="SWE project")

tasks = [
    {
        "id": 1,
        "title": "learn rest",
        "description" : "understand http methods and status codes.",
        "completed": False,
    },
    {
        "id" : 2,
        "title": "learn git branches",
        "description": "practice feature branches and merging",
        "completed": False,
    },
]

@app.get("/")
def root() -> dict:
    return {"message" : "Hello!, Prakash"}

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_tasks(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="task not found!",
    )

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED,)
def create_task(task: TaskCreate):
    new_task = {
        "id" : len(tasks) + 1,
        "title" : task.title,
        "description" : task.description,
        "completed" : task.completed,
    }
    tasks.append(new_task)

    return new_task