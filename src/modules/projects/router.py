from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import PROJECT_REPOSITORY_DEPENDENCY
from src.modules.auth.jwt import oauth2_scheme
from src.modules.projects.schemas import CreateProject, ViewProjectSimple, ViewProjectUsers

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ViewProjectSimple, status_code=201)
async def create_project(project: CreateProject,
                         project_repository: PROJECT_REPOSITORY_DEPENDENCY) -> ViewProjectSimple:
    return await project_repository.create(project)


@router.get("/{project_id}", response_model=ViewProjectSimple)
async def simple_read_project(project_id: int, project_repository: PROJECT_REPOSITORY_DEPENDENCY) -> ViewProjectSimple:
    return await project_repository.simple_read(project_id)


@router.get("/users/{project_id}", response_model=ViewProjectUsers)
async def read_with_users(project_id: int, project_repository: PROJECT_REPOSITORY_DEPENDENCY) -> ViewProjectUsers:
    return await project_repository.read_with_users(project_id)


@router.post("/add_user/{user_id}")
async def add_user_to_project(project_id: int, user_id: int,
                              project_repository: PROJECT_REPOSITORY_DEPENDENCY,
                              token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    return await project_repository.add_user(project_id, user_id)
