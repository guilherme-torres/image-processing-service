from fastapi import APIRouter, Depends

from app.core.dependencies import get_auth_service
from app.schemas.auth import LoginCreate, LoginResponse, RefreshTokenRequest
from app.services.auth import AuthService


router = APIRouter(prefix="/auth")

@router.post("/login/", response_model=LoginResponse, status_code=200)
def login(
    data: LoginCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(data)


@router.post("/token/refresh/", response_model=LoginResponse, status_code=200)
def refresh_access_token(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.refresh_access_token(data.refresh_token)
