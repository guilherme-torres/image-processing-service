from typing import Optional
from pydantic import BaseModel, PositiveInt, NonNegativeInt

class Resize(BaseModel):
    width: PositiveInt
    height: PositiveInt


class Crop(BaseModel):
    width: PositiveInt
    height: PositiveInt
    x: NonNegativeInt
    y: NonNegativeInt


class Filters(BaseModel):
    grayscale: Optional[bool] = None
    sepia: Optional[bool] = None


class Transformations(BaseModel):
    resize: Optional[Resize] = None
    crop: Optional[Crop] = None
    rotate: Optional[float] = None
    image_format: Optional[str] = None
    filters: Optional[Filters] = None


class TransformationsCreate(BaseModel):
    transformations: Transformations
