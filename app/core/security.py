from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Dict
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
    InvalidTokenError,
)
from pwdlib import PasswordHash
from app.core.config import settings
from app.core.dependencies import get_user_repo
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse


password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def generate_token(payload: Dict[str, Any], secret: str, algorithm: str) -> str:
    return jwt.encode(payload, secret, algorithm)


def validate_token(token: str, secret: str, algorithm: str):
    try:
        return jwt.decode(token, secret, algorithms=[algorithm])
    except ExpiredSignatureError:
        raise
    except InvalidSignatureError:
        raise
    except DecodeError:
        raise
    except InvalidTokenError:
        raise


def generate_access_token(payload: Dict[str, Any]) -> str:
    expiration_time = datetime.now(tz=timezone.utc) + timedelta(
        seconds=settings.JWT_ACCESS_EXPIRATION_SECONDS
    )
    return generate_token(
        {**payload, "exp": expiration_time},
        secret=settings.JWT_ACCESS_SECRET,
        algorithm=settings.JWT_ACCESS_ALGORITHM,
    )


def generate_refresh_token(payload: Dict[str, Any]) -> str:
    expiration_time = datetime.now(tz=timezone.utc) + timedelta(
        seconds=settings.JWT_REFRESH_EXPIRATION_SECONDS
    )
    return generate_token(
        {**payload, "exp": expiration_time},
        secret=settings.JWT_REFRESH_SECRET,
        algorithm=settings.JWT_REFRESH_ALGORITHM,
    )


def validate_access_token(token: str):
    return validate_token(
        token,
        secret=settings.JWT_ACCESS_SECRET,
        algorithm=settings.JWT_ACCESS_ALGORITHM,
    )


def validate_refresh_token(token: str):
    return validate_token(
        token,
        secret=settings.JWT_REFRESH_SECRET,
        algorithm=settings.JWT_REFRESH_ALGORITHM,
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = validate_access_token(token)
        user_id = int(payload.get("sub"))
        user = user_repo.get(user_id)
        if not user:
            raise credentials_exception
        return UserResponse(id=user.id, username=user.username)
    except InvalidTokenError:
        raise credentials_exception
