from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from fast_granja.models import ChickenRaceModel, FlockModel
from fast_granja.schema.flock_schema import (
    Flock,
    FlockCreate,
    FlockOverview,
    FlockPatch,
)

from fast_granja.router.annotated import T_Session


router = APIRouter()


@router.post("/", response_model=Flock)
async def create_flock(flock: FlockCreate, session: T_Session):
    db_flock = await session.scalar(
        select(FlockModel).where(FlockModel.flock_name == flock.flock_name)
    )

    if db_flock:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Flock already registered"
        )

    db_race = await session.scalar(
        select(ChickenRaceModel.id).where(ChickenRaceModel.id == flock.race_id)
    )

    if not db_race:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Chicken race not registered"
        )

    db_flock = FlockModel(
        price=flock.price,
        race_id=flock.race_id,
        amount=flock.amount,
        arrival_date=flock.arrival_date,
        supplier_name=flock.supplier_name,
        flock_name=flock.flock_name,
        isActive=True,
    )

    session.add(db_flock)
    await session.commit()
    await session.refresh(db_flock)

    return db_flock


@router.get("/", response_model=list[Flock])
async def list_flocks(session: T_Session):
    db_flocks = await session.scalars(select(FlockModel))

    return db_flocks


@router.patch("/{flock_id}", response_model=Flock)
async def patch_flock(flock_id: int, flock: FlockPatch, session: T_Session):
    db_flock = await session.scalar(select(FlockModel).where(FlockModel.id == flock_id))

    if not db_flock:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flock not found")

    for key, value in flock.model_dump(exclude_unset=True).items():
        if key == "race_id":
            db_chicken_race = await session.scalar(
                select(ChickenRaceModel.id).where(ChickenRaceModel.id == flock.race_id)
            )

            if not db_chicken_race:
                raise HTTPException(HTTPStatus.NOT_FOUND, detail="Race not found")

        setattr(db_flock, key, value)

    session.add(db_flock)
    await session.commit()
    await session.refresh(db_flock)

    return db_flock


@router.delete("/{flock_id}")
async def delete_flock(flock_id: int, session: T_Session):
    db_flock = await session.scalar(select(FlockModel).where(FlockModel.id == flock_id))

    if not db_flock:
        HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flock not found")

    await session.delete(db_flock)
    await session.commit()

    return "Flock deleted"


@router.get("/{flock_id}", response_model=FlockOverview)
async def get_flock_by_id(flock_id: int, session: T_Session):
    soma_total_eggs, soma_broken_eggs, soma_chicken_death = 0, 0, 0

    db_flock = await session.scalar(select(FlockModel).where(FlockModel.id == flock_id))

    if not db_flock:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flock not found")

    for daily_eggs in db_flock.daily_eggs:
        soma_total_eggs += daily_eggs.total_eggs
        soma_broken_eggs += daily_eggs.broken_eggs

    for chicken_death in db_flock.chicken_death:
        soma_chicken_death += chicken_death.amount

    flock_overview = FlockOverview(
        id=db_flock.id,
        price=db_flock.price,
        race_id=db_flock.race_id,
        amount=db_flock.amount,
        arrival_date=db_flock.arrival_date,
        supplier_name=db_flock.supplier_name,
        flock_name=db_flock.flock_name,
        isActive=db_flock.isActive,
        total_eggs=soma_total_eggs,
        total_broken_eggs=soma_broken_eggs,
        total_death_chicken=soma_chicken_death,
    )

    return flock_overview
