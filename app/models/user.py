from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship

from app.schemas.user import UserBase


if TYPE_CHECKING:
    from .image import Image

class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)

    images: list["Image"] = Relationship(back_populates="user", cascade_delete=True)
