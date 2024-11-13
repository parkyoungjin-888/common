from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from mongodb_module.beanie_control import BaseDocument


class User(BaseDocument):
    name: str
    age: int
    email: Optional[str | None] = None

    class Settings:
        name = 'user'

    class Config:
        extra = 'allow'


class ProjectUser(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    name: str
    age: int
