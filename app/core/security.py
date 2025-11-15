from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
    InvalidTokenError,
)
from pwdlib import PasswordHash
from app.core.config import settings


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


def validade_refresh_token(token: str):
    return validate_token(
        token,
        secret=settings.JWT_REFRESH_SECRET,
        algorithm=settings.JWT_REFRESH_ALGORITHM,
    )
