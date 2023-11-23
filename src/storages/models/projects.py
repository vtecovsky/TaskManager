import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storages.models.__mixin__ import IdMixin
from src.storages.models.base import Base

if TYPE_CHECKING:
    from src.storages.models.users import User


class Project(Base, IdMixin):
    __tablename__ = "projects"
    name: Mapped[str] = mapped_column()
    goal: Mapped[str] = mapped_column()
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime)

    users: Mapped[List["User"]] = relationship("User",
        secondary="projects_x_users", back_populates="projects"
    )


class ProjectXUser(Base):
    __tablename__ = "projects_x_users"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
