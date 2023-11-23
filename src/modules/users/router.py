from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import USER_REPOSITORY_DEPENDENCY
from src.modules.auth.jwt import oauth2_scheme
from src.modules.users.schemas import CreateUser, ViewUserTask, ViewUserProject, ViewUserFull, ViewUserSimple

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ViewUserSimple, status_code=201)
async def create_user(user: CreateUser, user_repository: USER_REPOSITORY_DEPENDENCY) -> ViewUserSimple:
    return await user_repository.create(user)


@router.get("/simple/{username}")
async def read_user_simple(username: str, user_repository: USER_REPOSITORY_DEPENDENCY) -> ViewUserSimple | None:
    return await user_repository.read_simple(username)


@router.get("/tasks/{user_id}", response_model=ViewUserTask)
async def read_user_with_task(user_id: int, user_repository: USER_REPOSITORY_DEPENDENCY,
                              token: Annotated[str, Depends(oauth2_scheme)]) -> ViewUserTask:
    return await user_repository.read_with_task(user_id)


@router.get("/projects/{user_id}", response_model=ViewUserProject)
async def read_user_with_projects(user_id: int, user_repository: USER_REPOSITORY_DEPENDENCY) -> ViewUserProject:
    return await user_repository.read_with_project(user_id)


@router.get("/{user_id}", response_model=ViewUserFull)
async def read_user_full(user_id: int, user_repository: USER_REPOSITORY_DEPENDENCY) -> ViewUserFull:
    return await user_repository.read_full(user_id)


@router.get("/")
async def read_all_users(user_repository: USER_REPOSITORY_DEPENDENCY) -> list[ViewUserSimple]:
    return await user_repository.list_users()


@router.delete("/{user_id}", response_model=ViewUserSimple)
async def delete_user(user_id: int, user_repository: USER_REPOSITORY_DEPENDENCY,
                      ) -> ViewUserSimple:
    return await user_repository.delete(user_id)
