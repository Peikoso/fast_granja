import datetime
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import extract, select, func

from fast_granja.models import DailyEggsModel, FlockModel
from fast_granja.router.annotated import T_Session
from fast_granja.schema.eggs_schema import Eggs, EggsDTO, EggsMonth, EggsPatch


router = APIRouter()


@router.post("/", response_model=Eggs)
async def create_eggs(eggs: EggsDTO, flock_id: int, session: T_Session):
    db_flock = await session.scalar(
        select(FlockModel.id).where(FlockModel.id == flock_id)
    )

    if not db_flock:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flock not found")

    db_eggs = DailyEggsModel(
        total_eggs=eggs.total_eggs,
        broken_eggs=eggs.broken_eggs,
        day=eggs.day,
        flock_id=flock_id,
    )

    session.add(db_eggs)
    await session.commit()
    await session.refresh(db_eggs)

    return db_eggs


@router.get("/", response_model=list[Eggs])
async def list_eggs(
    session: T_Session,
    flock_id: int = Query(default=None, ge=1),
    day_period: int = Query(default=None, ge=1),
):
    conditions = []

    if day_period:
        date_period = datetime.date.today() - datetime.timedelta(days=day_period)
        conditions.append(DailyEggsModel.day >= date_period)

    if flock_id:
        conditions.append(DailyEggsModel.flock_id == flock_id)

    db_eggs = await session.scalars(
        select(DailyEggsModel).where(*conditions).order_by(DailyEggsModel.day.desc())
    )

    return db_eggs


@router.patch("/{eggs_id}", response_model=Eggs)
async def patch_eggs(eggs_id: int, eggs: EggsPatch, session: T_Session):
    db_eggs = await session.scalar(
        select(DailyEggsModel).where(DailyEggsModel.id == eggs_id)
    )

    if not db_eggs:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Daily eggs not found"
        )

    for key, value in eggs.model_dump(exclude_unset=True).items():
        setattr(db_eggs, key, value)

    session.add(db_eggs)
    await session.commit()
    await session.refresh(db_eggs)

    return db_eggs


@router.delete("/{eggs_id}")
async def delete_eggs(eggs_id: int, session: T_Session):
    db_eggs = await session.scalar(
        select(DailyEggsModel).where(DailyEggsModel.id == eggs_id)
    )

    if not db_eggs:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Daily eggs not found"
        )

    await session.delete(db_eggs)
    await session.commit()

    return "Daily eggs deleted"


@router.get("/report")
async def total_eggs_month(
    session: T_Session,
    month: int = Query(default=None, ge=1, le=12),
    year: int = Query(..., ge=2025, le=2100),
):
    conditions = [extract("YEAR", DailyEggsModel.day) == year]
    if month:
        conditions.append(extract("MONTH", DailyEggsModel.day) == month)

    db_eggs = await session.execute(
        select(
            func.sum(DailyEggsModel.total_eggs).label("total_eggs"),
            func.sum(DailyEggsModel.broken_eggs).label("broken_eggs"),
            DailyEggsModel.flock_id,
        )
        .where(*conditions)
        .group_by(DailyEggsModel.flock_id)
    )

    result = db_eggs.fetchall()

    result = [
        EggsMonth(
            total_eggs=egg_month.total_eggs,
            broken_eggs=egg_month.broken_eggs,
            flock_id=egg_month.flock_id,
        )
        for egg_month in result
    ]

    return result
