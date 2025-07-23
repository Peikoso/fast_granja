from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_granja.models import (
    ChickenDeathModel,
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
async def list_chicken_death_reason(session: T_Session):
    return await session.scalars(select(ChickenDeathReasonModel))


@router.put("/{death_reason_id}")
async def update_chicken_death_reason(death_reason_id: int, chicken_death_reason: ChickenDeathReasonDTO, session: T_Session):
    db_chicken_death_reason = await session.scalar(
        select(ChickenDeathReasonModel.reason).where(
            ChickenDeathReasonModel.reason == chicken_death_reason.reason
        )
    )

    if db_chicken_death_reason:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Reason already exists"
    )

    db_chicken_death_reason = await session.scalar(
        select(ChickenDeathReasonModel).where(ChickenDeathReasonModel.id==death_reason_id)
    )

    if not db_chicken_death_reason:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Reason not found"
        )
    
    db_chicken_death_reason.reason=chicken_death_reason.reason

    await session.commit()
    await session.refresh(db_chicken_death_reason)

    return db_chicken_death_reason


@router.delete("/{death_reason_id}")
async def delete_chicken_death_reason(death_reason_id: int, session: T_Session):
    db_chicken_death_reason = await session.scalar(
        select(ChickenDeathReasonModel).where(ChickenDeathReasonModel.id == death_reason_id)
    )

    if not db_chicken_death_reason:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Reason not found")
    
    db_chicken_death = await session.scalar(
        select(ChickenDeathModel).where(ChickenDeathModel.reason_id == death_reason_id)
    )

    if db_chicken_death:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Cannot delete reason with associated chicken deaths"
        )

    await session.delete(db_chicken_death_reason)
    await session.commit()

    return "Reason deleted"