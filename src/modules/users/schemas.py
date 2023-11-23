import datetime
from typing import Optional, List

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

import re

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    birthday_date: datetime.datetime
    password: str = Field(example="password")

    @field_validator("firstname")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Firstname should contains only letters"
            )
        return value

    @field_validator("lastname")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Lastname should contains only letters"
            )
        return value


class UserInDB(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    birthday_date: datetime.datetime

    created_at: datetime.datetime
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class ViewUserSimple(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    birthday_date: datetime.datetime

    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ViewUserTask(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    birthday_date: datetime.datetime

    tasks: Optional[List["ViewTaskSimple"]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ViewUserProject(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    birthday_date: datetime.datetime

    projects: Optional[List["ViewProjectSimple"]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ViewUserFull(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    birthday_date: datetime.datetime

    tasks: Optional[List["ViewTaskSimple"]] = Field(default_factory=list)
    projects: Optional[List["ViewProjectSimple"]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


from src.modules.tasks.schemas import ViewTaskSimple  # noqa E402
from src.modules.projects.schemas import ViewProjectSimple  # noqa E402

ViewUserTask.model_rebuild()
ViewUserProject.model_rebuild()
ViewUserFull.model_rebuild()
