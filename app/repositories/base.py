from abc import ABC, abstractmethod

from app.models.task import Task


class TaskRepositoryInterface(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> list[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task: Task) -> None:
        pass