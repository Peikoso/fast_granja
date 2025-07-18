from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_granja.models import (
    ChickenDeathReasonModel,
)
from fast_granja.router.annotated import T_Session
from fast_granja.schema.chicken_schema import (
    ChickenDeathReason,
    ChickenDeathReasonDTO,
)


router = APIRouter()


@router.post("/", response_model=ChickenDeathReason)
async def create_chicken_death_reason(
    chicken_death_reason: ChickenDeathReasonDTO, session: T_Session
):
    db_chicken_death_reason = await session.scalar(
        select(ChickenDeathReasonModel.reason).where(
            ChickenDeathReasonModel.reason == chicken_death_reason.reason
        )
    )

    if db_chicken_death_reason:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Reason already exists"
        )

    db_chicken_death_reason = ChickenDeathReasonModel(
        reason=chicken_death_reason.reason
    )

    session.add(db_chicken_death_reason)
    await session.commit()
    await session.refresh(db_chicken_death_reason)

    return db_chicken_death_reason


@router.get("/", response_model=list[ChickenDeathReason])
async def list_chicken_race(session: T_Session):
    return await session.scalars(select(ChickenDeathReasonModel))
