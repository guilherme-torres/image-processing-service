from typing import Any, Optional
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship

from app.models.user import User
from app.schemas.image import ImageBase


class Image(ImageBase, table=True):
    __tablename__ = "images"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    image_metadata: dict[str, Any] = Field(sa_column=Column(JSONB))

    user: User = Relationship(back_populates="images")
