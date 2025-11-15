from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=30)


class UserCreate(UserBase):
    password: str = Field(max_length=255)


class UserResponse(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=30)
    password: Optional[str] = Field(default=None, max_length=255)

