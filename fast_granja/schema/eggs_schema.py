from datetime import date
from pydantic import BaseModel, Field


class EggsDTO(BaseModel):
    total_eggs: int = Field(..., ge=0)
    broken_eggs: int = Field(..., ge=0)
    day: date


class Eggs(EggsDTO):
    id: int
    flock_id: int


class EggsPatch(BaseModel):
    total_eggs: int = Field(default=None, ge=0)
    broken_eggs: int = Field(default=None, ge=0)
    day: date = Field(default=None)


class EggsMonth(BaseModel):
    total_eggs: int
    broken_eggs: int
    flock_id: int
