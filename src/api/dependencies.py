from typing import Annotated

from fastapi import Depends

from src.modules.projects.repository import AbstractProjectRepository
from src.modules.tasks.repository import AbstractTaskRepository
from src.modules.users.repository import AbstractUserRepository
from src.storages.storage import AbstractSQLAlchemyStorage


class Dependencies:
    _storage: "AbstractSQLAlchemyStorage"
    _user_repository: "AbstractUserRepository"
    _task_repository: "AbstractTaskRepository"
    _project_repository: "AbstractProjectRepository"

    @classmethod
    def get_storage(cls) -> "AbstractSQLAlchemyStorage":
        return cls._storage

    @classmethod
    def set_storage(cls, storage: "AbstractSQLAlchemyStorage"):
        cls._storage = storage

    @classmethod
    def get_user_repository(cls) -> "AbstractUserRepository":
        return cls._user_repository

    @classmethod
    def set_user_repository(cls, user_repository: "AbstractUserRepository"):
        cls._user_repository = user_repository

    @classmethod
    def get_task_repository(cls) -> "AbstractTaskRepository":
        return cls._task_repository

    @classmethod
    def set_task_repository(cls, task_repository: "AbstractTaskRepository"):
        cls._task_repository = task_repository

    @classmethod
    def get_project_repository(cls) -> "AbstractProjectRepository":
        return cls._project_repository

    @classmethod
    def set_project_repository(cls, project_repository: "AbstractProjectRepository"):
        cls._project_repository = project_repository


STORAGE_DEPENDENCY = Annotated[AbstractSQLAlchemyStorage, Depends(Dependencies.get_storage)]
USER_REPOSITORY_DEPENDENCY = Annotated[
    AbstractUserRepository, Depends(Dependencies.get_user_repository)
]
TASK_REPOSITORY_DEPENDENCY = Annotated[
    AbstractTaskRepository, Depends(Dependencies.get_task_repository)
]
PROJECT_REPOSITORY_DEPENDENCY = Annotated[
    AbstractProjectRepository, Depends(Dependencies.get_project_repository)
]
