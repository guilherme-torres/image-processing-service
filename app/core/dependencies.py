from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session
from app.repositories.image import ImageRepository
from app.repositories.user import UserRepository


def get_user_repo(session: Session = Depends(get_session)):
    return UserRepository(session)


def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    from app.services.user import UserService

    return UserService(user_repo)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)):
    from app.services.auth import AuthService

    return AuthService(user_repo)


def get_image_repo(session: Session = Depends(get_session)):
    return ImageRepository(session)


def get_image_service(image_repo: ImageRepository = Depends(get_image_repo)):
    from app.services.image import ImageService

    return ImageService(image_repo)
