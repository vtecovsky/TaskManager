import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storages.models.__mixin__ import IdMixin
from src.storages.models.base import Base

if TYPE_CHECKING:
    from src.storages.models.tasks import Task
    from src.storages.models.projects import Project


class User(Base, IdMixin):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(unique=True)
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    birthday_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    tasks: Mapped[Optional[List["Task"]]] = relationship(back_populates="users")
    projects: Mapped[List["Project"]] = relationship("Project",
        secondary="projects_x_users", back_populates="users"
    )
