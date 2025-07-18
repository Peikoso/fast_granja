from datetime import date
from pydantic import BaseModel, Field


class FlockCreate(BaseModel):
    price: int = Field(..., ge=0)
    race_id: int = Field(..., ge=0)
    amount: int = Field(..., ge=0)
    arrival_date: date
    supplier_name: str = Field(..., min_length=3)
    flock_name: str = Field(..., min_length=1)


class Flock(FlockCreate):
    isActive: bool
    id: int


class FlockPatch(BaseModel):
    price: int = Field(default=None, ge=0)
    race_id: int = Field(default=None, ge=0)
    amount: int = Field(default=None, ge=0)
    arrival_date: date = Field(default=None)
    supplier_name: str = Field(default=None, min_length=3)
    flock_name: str = Field(default=None, min_length=1)
    isActive: bool = Field(default=None)


class FlockOverview(Flock):
    total_eggs: int
    total_broken_eggs: int
    total_death_chicken: int
