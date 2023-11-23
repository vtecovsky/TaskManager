__all__ = ["AbstractTaskRepository", "TaskRepository"]

from abc import ABC, abstractmethod

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.tasks.schemas import ViewTaskUsers, CreateTask
from src.storages.models.tasks import Task
from src.storages.storage import AbstractSQLAlchemyStorage


class AbstractTaskRepository(ABC):

    # ----------------- CRUD ----------------- #
    @abstractmethod
    async def create(self, task: "CreateTask") -> "ViewTaskUsers":
        ...

    @abstractmethod
    async def read(self, task_id: int) -> "ViewTaskUsers":
        ...

    @abstractmethod
    async def assign_task(self, task_id: int, assignee_id: int) -> "ViewTaskUsers":
        ...


class TaskRepository(AbstractTaskRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def create(self, task: "CreateTask") -> "ViewTaskUsers":
        async with self._create_session() as session:
            q = insert(Task).values(**task.model_dump()).returning(Task)
            new_task = await session.scalar(q)
            await session.commit()
            if new_task:
                return ViewTaskUsers.model_validate(new_task)

    async def read(self, task_id: int) -> "ViewTaskUsers":
        async with self._create_session() as session:
            q = select(Task).where(Task.id == task_id).options(selectinload(Task.users))
            task = await session.scalar(q)
            if task:
                return ViewTaskUsers.model_validate(task)

    async def assign_task(self, task_id: int, user_id: int) -> "ViewTaskUsers":
        async with self._create_session() as session:
            q = update(Task).where(Task.id == task_id).values(user_id=user_id).options(
                selectinload(Task.users)).returning(Task)
            updated_task = await session.scalar(q)
            await session.commit()
            return ViewTaskUsers.model_validate(updated_task)
