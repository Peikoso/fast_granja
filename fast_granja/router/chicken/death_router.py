from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select

from fast_granja.models import (
    ChickenDeathModel,
    ChickenDeathReasonModel,
    FlockModel,
)
from fast_granja.router.annotated import T_Session
from fast_granja.schema.chicken_schema import (
    ChickenDeathDTO,
    ChickenDeath,
    TotalChickenDeath,
)


router = APIRouter()


@router.post("/", response_model=ChickenDeath)
async def chicken_death_create(
    chicken_deaths: ChickenDeathDTO, flock_id: int, session: T_Session
):
    db_flock = await session.scalar(
        select(FlockModel.id).where(FlockModel.id == flock_id)
    )

    if not db_flock:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flock not found")

    db_chicken_death_reason = await session.scalar(
        select(ChickenDeathReasonModel.id).where(
            ChickenDeathReasonModel.id == chicken_deaths.reason_id
        )
    )

    if not db_chicken_death_reason:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Reason not found")

    db_chicken_death = ChickenDeathModel(
        amount=chicken_deaths.amount,
        reason_id=chicken_deaths.reason_id,
        day=chicken_deaths.day,
        flock_id=flock_id,
    )

    session.add(db_chicken_death)
    await session.commit()
    await session.refresh(db_chicken_death)

    return db_chicken_death


@router.get("/", response_model=list[ChickenDeath])
async def get_chicken_deaths(
    session: T_Session,
    flock_id: int = Query(default=None, ge=1),
    day_period: int = Query(default=None, ge=1),
):
    if flock_id:
        return await session.scalars(
            select(ChickenDeathModel)
            .where(ChickenDeathModel.flock_id == flock_id)
            .order_by(ChickenDeathModel.day.desc())
        )

    return await session.scalars(
        select(ChickenDeathModel).order_by(ChickenDeathModel.day.desc())
    )


@router.get("/report", response_model=TotalChickenDeath)
async def get_chicken_death_report(session: T_Session):
    db_total_death = await session.scalar(
        select(func.sum(ChickenDeathModel.amount).label("total_chicken_death"))
    )

    return {"total_chicken_death": db_total_death}


@router.patch("/{chicken_death_id}", response_model=ChickenDeath)
async def patch_chicken_death(): ...


@router.delete("/{chicken_death_id}")
async def delete_chicken_death(): ...
