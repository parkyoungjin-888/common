from pydantic import BaseModel, Field


class Rawdata(BaseModel):
    timestamp: int = Field(examples=[1717657200])
    io_id: str = Field(examples=['io_id'])
    value: float = Field(examples=[100.1])
