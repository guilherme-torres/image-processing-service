from sqlmodel import Session
from app.core.celery import celery_app
from app.core.database import engine
from app.repositories.image import ImageRepository
from app.services.image import ImageService


@celery_app.task
def transform_image_task(image_id: int, user_id: int, transformations_dict: dict) -> dict:
    with Session(engine) as session:
        try:
            image_repo = ImageRepository(session)
            image_service = ImageService(image_repo)
            result = image_service.transform(image_id, user_id=user_id, transformations_dict=transformations_dict)
            return result.model_dump()
        except Exception as e:
            return {"status": "error", "message": str(e)}
