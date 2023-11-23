from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    name: str
    description: str
    status: str

    user_id: Optional[int] = None


class ViewTaskSimple(BaseModel):
    id: int
    name: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class ViewTaskUsers(BaseModel):
    id: int
    name: str
    description: str
    status: str

    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


ViewTaskUsers.model_rebuild()
CreateTask.model_rebuild()
