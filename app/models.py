from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
