from http import HTTPStatus
from fast_granja.schema.user import Token
from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from fast_granja.models import UserModel
from fast_granja.router.annotated import T_OAuth2Form, T_Session
from fast_granja.security import create_access_token, verify_password


router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: T_OAuth2Form, session: T_Session):
    user = await session.scalar(
        select(UserModel).where(UserModel.username == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
