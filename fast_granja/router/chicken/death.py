from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select

from fast_granja.models import (
    ChickenDeathModel,
    ChickenDeathReasonModel,
    FlockModel,
)
from fast_granja.router.annotated import T_Session
from fast_granja.schema.chicken import (
    ChickenDeathDTO,
    ChickenDeath,
    ChickenDeathUpdate,
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

    if db_total_death is None:
        db_total_death = 0

    return {"total_chicken_death": db_total_death}


@router.put("/{chicken_death_id}", response_model=ChickenDeath)
async def update_chicken_death(
    chicken_death_id: int, chicken_death: ChickenDeathUpdate, session: T_Session
):
    db_chicken_death = await session.scalar(
        select(ChickenDeathModel).where(ChickenDeathModel.id == chicken_death_id)
    )

    if not db_chicken_death:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Chicken death not found."
        )

    db_flock = await session.scalar(
        select(FlockModel.id).where(FlockModel.id == chicken_death.flock_id)
    )

    if not db_flock:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flock not found.")

    db_death_reason = await session.scalar(
        select(ChickenDeathReasonModel.id).where(
            ChickenDeathReasonModel.id == chicken_death.reason_id
        )
    )

    if not db_death_reason:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Death reason not found."
        )

    db_chicken_death.amount = chicken_death.amount
    db_chicken_death.reason_id = chicken_death.reason_id
    db_chicken_death.day = chicken_death.day
    db_chicken_death.flock_id = chicken_death.flock_id

    await session.commit()
    await session.refresh(db_chicken_death)

    return db_chicken_death


@router.delete("/{chicken_death_id}")
async def delete_chicken_death(chicken_death_id: int, session: T_Session):
    db_chicken_death = await session.scalar(
        select(ChickenDeathModel).where(ChickenDeathModel.id == chicken_death_id)
    )

    if not db_chicken_death:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Chicken death not found."
        )

    await session.delete(db_chicken_death)
    await session.commit()

    return "Chicken death deleted"
