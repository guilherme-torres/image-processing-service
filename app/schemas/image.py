from typing import Any, Optional
from sqlmodel import Field, SQLModel


class ImageBase(SQLModel):
    url: str = Field(max_length=255)
    image_metadata: dict[str, Any]


class ImageResponse(ImageBase):
    id: int


class ImageCreate(ImageBase):
    pass


class ImageUpdate(SQLModel):
    url: Optional[str] = Field(default=None, max_length=255)
