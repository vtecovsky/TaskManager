from fastapi import FastAPI

from src.api.dependencies import Dependencies
from src.api.routers import routers
from src.config import settings
from src.modules.projects.repository import ProjectRepository
from src.modules.tasks.repository import TaskRepository
from src.modules.users.repository import UserRepository
from src.storages.storage import SQLAlchemyStorage

app = FastAPI()


async def setup_repositories():
    # ------------------- Repositories Dependencies -------------------
    storage = SQLAlchemyStorage.from_url(settings.DB_URL)
    user_repository = UserRepository(storage)
    task_repository = TaskRepository(storage)
    project_repository = ProjectRepository(storage)
    Dependencies.set_storage(storage)
    Dependencies.set_user_repository(user_repository)
    Dependencies.set_task_repository(task_repository)
    Dependencies.set_project_repository(project_repository)

    await storage.create_all()


@app.on_event("startup")
async def startup_event():
    await setup_repositories()


for router in routers:
    app.include_router(router)
