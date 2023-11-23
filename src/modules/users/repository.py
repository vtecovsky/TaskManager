__all__ = ["AbstractUserRepository", "UserRepository"]

from abc import ABC, abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.modules.auth.hashing import Hasher
from src.modules.users.schemas import ViewUserTask, CreateUser, ViewUserProject, ViewUserFull, ViewUserSimple, UserInDB
from src.storages.models.users import User
from src.storages.storage import AbstractSQLAlchemyStorage


class AbstractUserRepository(ABC):

    # ----------------- CRUD ----------------- #
    @abstractmethod
    async def create(self, user: "CreateUser") -> "ViewUserSimple":
        ...

    @abstractmethod
    async def read_simple(self, username: str) -> ViewUserSimple | None:
        ...

    @abstractmethod
    async def read_by_username_for_auth(self, username: str) -> UserInDB | None:
        ...

    @abstractmethod
    async def read_with_task(self, user_id: int) -> "ViewUserTask":
        ...

    @abstractmethod
    async def read_with_project(self, user_id: int) -> "ViewUserProject":
        ...

    @abstractmethod
    async def read_full(self, user_id: int) -> "ViewUserFull":
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> "ViewUserSimple":
        ...

    @abstractmethod
    async def list_users(self) -> list["ViewUserSimple"]:
        ...


class UserRepository(AbstractUserRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def create(self, user: "CreateUser") -> "ViewUserSimple":
        async with self._create_session() as session:
            hashed_password = Hasher.get_password_hash(user.password)
            q = insert(User).values(username=user.username, firstname=user.firstname, lastname=user.lastname,
                                    birthday_date=user.birthday_date, hashed_password=hashed_password).options(
                selectinload(User.tasks)).returning(
                User)
            new_user = await session.scalar(q)
            await session.commit()
            if new_user:
                return ViewUserSimple.model_validate(new_user)

    async def read_simple(self, username: str) -> ViewUserSimple | None:
        async with self._create_session() as session:
            q = select(User).where(User.username == username)
            user = await session.scalar(q)
            if user:
                return ViewUserSimple.model_validate(user)

    async def list_users(self) -> list["ViewUserSimple"]:
        async with self._create_session() as session:
            q = select(User)
            users = await session.scalars(q)
            if users:
                return [ViewUserSimple.model_validate(user) for user in users]

    async def read_by_username_for_auth(self, username: str) -> UserInDB | None:
        async with self._create_session() as session:
            q = select(User).where(User.username == username)
            user = await session.scalar(q)
            if user:
                return UserInDB.model_validate(user)

    async def read_with_task(self, user_id: int) -> "ViewUserTask":
        async with self._create_session() as session:
            q = select(User).where(User.id == user_id).options(selectinload(User.tasks))
            user = await session.scalar(q)
            if user:
                return ViewUserTask.model_validate(user)

    async def read_with_project(self, user_id: int) -> "ViewUserProject":
        async with self._create_session() as session:
            q = select(User).where(User.id == user_id).options(
                selectinload(User.projects))
            user = await session.scalar(q)
            if user:
                return ViewUserProject.model_validate(user)

    async def read_full(self, user_id: int) -> "ViewUserFull":
        async with self._create_session() as session:
            q = select(User).where(User.id == user_id).options(
                joinedload(User.projects)).options(joinedload(User.tasks))
            user = await session.scalar(q)
            if user:
                return ViewUserFull.model_validate(user)

    async def delete(self, user_id: int) -> "ViewUserSimple":
        async with self._create_session() as session:
            q = delete(User).where(User.id == user_id).returning(User)
            user = await session.scalar(q)
            await session.commit()
            if user:
                return ViewUserSimple.model_validate(user)
