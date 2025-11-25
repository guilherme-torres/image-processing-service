from fastapi import APIRouter, Depends, File, UploadFile
from celery.result import AsyncResult
from app.core.dependencies import get_image_service
from app.core.security import get_current_user
from app.schemas.image import ImageResponse
from app.schemas.transformations import TransformationsCreate
from app.schemas.user import UserResponse
from app.services.image import ImageService
from app.tasks.image_processing import transform_image_task


router = APIRouter(prefix="/images")

@router.post("/", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    image_service: ImageService = Depends(get_image_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await image_service.upload(file=file, user_id=current_user.id)


@router.get("/{id}", response_model=ImageResponse)
def get_image(
    id: int,
    image_service: ImageService = Depends(get_image_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return image_service.get_image_by_id(id, current_user.id)


@router.get("/", response_model=list[ImageResponse])
def list_images(
    limit: int = 100,
    skip: int = 0,
    image_service: ImageService = Depends(get_image_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return image_service.list_images(user_id=current_user.id, limit=limit, skip=skip)


@router.delete("/{id}", status_code=204)
def delete_image(
    id: int,
    image_service: ImageService = Depends(get_image_service),
    current_user: UserResponse = Depends(get_current_user),
):
    image_service.delete_image(id, current_user.id)


@router.post("/{id}/transform/")
def transform_image(
    id: int,
    transformations: TransformationsCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    task = transform_image_task.delay(id, current_user.id, transformations.model_dump(exclude_none=True, exclude_unset=True))
    return {"task_id": task.id}


@router.get("/tasks/{task_id}")
def transform_image_task_result(
    task_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return task_result.get()
    else:
        return {"status": task_result.status}
