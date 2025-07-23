from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_granja.models import (
    ChickenRaceModel,
    FlockModel,
)
from fast_granja.router.annotated import T_Session
from fast_granja.schema.chicken_schema import (
    ChickenRace,
    ChickenRaceDTO,
)


router = APIRouter()


@router.post("/", response_model=ChickenRace)
async def create_chicken_race(chicken_race: ChickenRaceDTO, session: T_Session):
    db_chicken_race = await session.scalar(
        select(ChickenRaceModel.race).where(ChickenRaceModel.race == chicken_race.race)
    )

    if db_chicken_race:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Race already registered"
        )

    db_chicken_race = ChickenRaceModel(race=chicken_race.race)

    session.add(db_chicken_race)
    await session.commit()
    await session.refresh(db_chicken_race)

    return db_chicken_race


@router.get("/", response_model=list[ChickenRace])
async def list_chicken_race(session: T_Session):
    return await session.scalars(select(ChickenRaceModel))


@router.put("/{chicken_race_id}", response_model=ChickenRace)
async def chicken_race_update(
    chicken_race_id: int, chicken_race: ChickenRaceDTO, session: T_Session
):
    db_chicken_race = await session.scalar(
        select(ChickenRaceModel.race).where(ChickenRaceModel.race == chicken_race.race)
    )

    if db_chicken_race:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Race already registered"
        )

    db_chicken_race = await session.scalar(
        select(ChickenRaceModel).where(ChickenRaceModel.id == chicken_race_id)
    )

    if not db_chicken_race:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Race not found")

    db_chicken_race.race = chicken_race.race

    await session.commit()
    await session.refresh(db_chicken_race)

    return db_chicken_race


@router.delete("/{chicken_race_id}")
async def delete_chicken_race(chicken_race_id: int, session: T_Session):
    db_flock = await session.scalar(
        select(FlockModel.id).where(FlockModel.race_id == chicken_race_id)
    )

    if db_flock:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Can not delete a race linked to a flock",
        )

    db_chicken_race = await session.scalar(
        select(ChickenRaceModel).where(ChickenRaceModel.id == chicken_race_id)
    )

    if not db_chicken_race:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Race not found")

    await session.delete(db_chicken_race)
    await session.commit()

    return "Chicken race deleted"
