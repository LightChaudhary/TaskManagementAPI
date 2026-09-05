from pydantic import BaseModel
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDUIM = "medium"
    HIGH = "high"

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False
    priority: Priority = Priority.MEDUIM

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool
    priority: Priority

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: Priority
