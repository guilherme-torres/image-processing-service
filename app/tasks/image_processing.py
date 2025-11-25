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
            result_dict = image_service.transform(image_id, user_id=user_id, transformations_dict=transformations_dict)
            success = {"status": "success", "data": result_dict.model_dump()}
            return success
        except Exception as e:
            error = {"status": "error", "message": str(e)}
            return error
