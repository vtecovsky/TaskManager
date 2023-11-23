import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class CreateProject(BaseModel):
    name: str
    goal: str
    start_date: datetime.datetime
    deadline: datetime.datetime


class ViewProjectSimple(BaseModel):
    id: int
    name: str
    goal: str
    start_date: datetime.datetime
    deadline: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ViewProjectUsers(BaseModel):
    name: str
    goal: str
    start_date: datetime.datetime
    deadline: datetime.datetime

    users: Optional[List["ViewUserSimple"]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


from src.modules.users.schemas import ViewUserSimple  # noqa E402

ViewProjectUsers.model_rebuild()
