from typing import Optional
from beanie import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, root_validator


class User(BaseModel):
    name: str
    age: int
    email: Optional[str | None] = None

    class Config:
        extra = 'allow'

    @root_validator(pre=True)
    def type_based_conversion(cls, values):
        for field_name, value in values.items():
            if field_name not in cls.__annotations__:
                continue
            field_type = cls.__annotations__.get(field_name)
            if field_type == str and not isinstance(value, str):
                values[field_name] = str(value)
            if field_type == int and isinstance(value, str) and value.isdigit():
                values[field_name] = int(value)
            elif field_type == int and isinstance(value, float):
                values[field_name] = int(value)
            elif field_type == float and isinstance(value, str):
                try:
                    values[field_name] = float(value)
                except ValueError:
                    raise ValueError(f'Field {field_name} expects a float value, got {value}')
        return values


class ProjectUser(BaseModel):
    id: ObjectId = Field(alias='_id')
    name: str
    age: int
