from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fast_granja.database import get_session


T_Session = Annotated[AsyncSession, Depends(get_session)]
