from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserDTO(BaseModel):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=4)
    email: EmailStr


class User(UserDTO):
    id: int


class UserPatch(BaseModel):
    username: Optional[str] = Field(default=None, min_length=4)
    password: Optional[str] = Field(default=None, min_length=8)
    full_name: Optional[str] = Field(default=None, min_length=4)
    email: Optional[EmailStr] = None
