from datetime import date
from pydantic import BaseModel, Field


class ChickenDeathDTO(BaseModel):
    amount: int = Field(..., ge=0)
    reason_id: int = Field(..., ge=0)
    day: date

class ChickenDeath(ChickenDeathDTO):
    flock_id: int
    id: int

class ChickenDeathUpdate(ChickenDeathDTO):
    flock_id: int 


class TotalChickenDeath(BaseModel):
    total_chicken_death: int


class ChickenDeathReasonDTO(BaseModel):
    reason: str = Field(..., min_length=3)


class ChickenDeathReason(ChickenDeathReasonDTO):
    id: int


class ChickenRaceDTO(BaseModel):
    race: str = Field(..., min_length=3)


class ChickenRace(ChickenRaceDTO):
    id: int
