from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=30)
    password_hash: str = Field(max_length=255)
