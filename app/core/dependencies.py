from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.user import UserService


def get_user_repo(session: Session = Depends(get_session)):
    return UserRepository(session)


def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)):
    return AuthService(user_repo)
