from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.storages.models.__mixin__ import IdMixin
from src.storages.models.base import Base

if TYPE_CHECKING:
    from src.storages.models.users import User


class Task(Base, IdMixin):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped[List["User"]] = relationship(back_populates="tasks")
