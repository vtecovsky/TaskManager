from src.modules.users.router import router as router_users
from src.modules.tasks.router import router as router_tasks
from src.modules.projects.router import router as router_projects
from src.modules.auth.router import router as router_auth

routers = [router_users, router_users, router_tasks, router_projects, router_auth]

__all__ = ["routers"]
