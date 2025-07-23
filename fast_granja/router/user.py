from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from fast_granja.models import UserModel
from fast_granja.schema.user import User, UserDTO, UserPatch

from fast_granja.router.annotated import T_Admin, T_Session
from fast_granja.security import get_password_hash


router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user: UserDTO, session: T_Session):
    db_user = await session.scalar(
        select(UserModel).where(
            (UserModel.username == user.username) | (UserModel.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )

    db_user = UserModel(
        username=user.username,
        password=get_password_hash(user.password),
        full_name=user.full_name,
        email=user.email,
        isAdmin=False,
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get("/", response_model=list[User])
async def list_users(session: T_Session):
    db_funcionaries = await session.scalars(select(UserModel).where(~UserModel.isAdmin))

    return db_funcionaries


@router.patch("/{user_id}")
async def patch_user(user_id: int, user: UserPatch, session: T_Session):
    db_user = await session.scalar(
        select(UserModel).where(
            ((UserModel.username == user.username) | (UserModel.email == user.email))
            & (UserModel.id != user_id)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )

    db_user = await session.scalar(select(UserModel).where(UserModel.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")

    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password":
            value = get_password_hash(value)
        setattr(db_user, key, value)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: T_Session):
    db_user = await session.scalar(select(UserModel).where(UserModel.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    await session.delete(db_user)
    await session.commit()

    return "User deleted"
