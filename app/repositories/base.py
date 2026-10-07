from abc import ABC, abstractmethod

from app.models.task import Task


class TaskRepositoryInterface(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_all(
        self,
        status: str | None = None,
        priority: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Task]:
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