__all__ = ["AbstractProjectRepository", "ProjectRepository"]

from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.modules.projects.schemas import CreateProject, ViewProjectSimple, ViewProjectUsers
from src.storages.models.projects import Project, ProjectXUser
from src.storages.storage import AbstractSQLAlchemyStorage


class AbstractProjectRepository(ABC):

    # ----------------- CRUD ----------------- #
    @abstractmethod
    async def create(self, project: "CreateProject") -> "ViewProjectSimple":
        ...

    @abstractmethod
    async def simple_read(self, project_id: int) -> "ViewProjectSimple":
        ...

    @abstractmethod
    async def read_with_users(self, project_id: int) -> "ViewProjectUsers":
        ...

    @abstractmethod
    async def add_user(self, project_id: int, user_id: int) -> None:
        ...


class ProjectRepository(AbstractProjectRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def create(self, project: "CreateProject") -> "ViewProjectSimple":
        async with self._create_session() as session:
            q = insert(Project).values(**project.model_dump()).options(selectinload(Project.users)).returning(Project)
            new_project = await session.scalar(q)
            await session.commit()
            if new_project:
                return ViewProjectSimple.model_validate(new_project)

    async def simple_read(self, project_id: int) -> "ViewProjectSimple":
        async with self._create_session() as session:
            q = select(Project).where(Project.id == project_id).options(selectinload(Project.users))
            project = await session.scalar(q)
            if project:
                return ViewProjectSimple.model_validate(project)

    async def read_with_users(self, project_id: int) -> "ViewProjectUsers":
        async with self._create_session() as session:
            q = select(Project).where(Project.id == project_id).options(joinedload(Project.users))
            project = await session.scalar(q)
            if project:
                return ViewProjectUsers.model_validate(project)

    async def add_user(self, project_id: int, user_id: int) -> None:
        async with self._create_session() as session:
            q = insert(ProjectXUser).values(project_id=project_id, user_id=user_id)
            await session.execute(q)
            await session.commit()
