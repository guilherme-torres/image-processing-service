from fastapi import APIRouter, Depends, File, UploadFile

from app.core.dependencies import get_image_service
from app.core.security import get_current_user
from app.schemas.image import ImageResponse
from app.schemas.user import UserResponse
from app.services.image import ImageService


router = APIRouter(prefix="/images")

@router.post("/", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    image_service: ImageService = Depends(get_image_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await image_service.upload(file=file, user_id=current_user.id)
