from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import TASK_REPOSITORY_DEPENDENCY
from src.modules.auth.jwt import oauth2_scheme
from src.modules.tasks.schemas import CreateTask, ViewTaskUsers

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=ViewTaskUsers, status_code=201)
async def create_task(task: CreateTask, task_repository: TASK_REPOSITORY_DEPENDENCY) -> ViewTaskUsers:
    return await task_repository.create(task)


@router.get("/{task_id}", response_model=ViewTaskUsers)
async def read_task(task_id: int, task_repository: TASK_REPOSITORY_DEPENDENCY) -> ViewTaskUsers:
    return await task_repository.read(task_id)


@router.post("/assign/{task_id}", response_model=ViewTaskUsers, )
async def assign_task(task_id: int, assignee_id: int, task_repository: TASK_REPOSITORY_DEPENDENCY,
                      token: Annotated[str, Depends(oauth2_scheme)]) -> ViewTaskUsers:
    return await task_repository.assign_task(task_id, assignee_id)
