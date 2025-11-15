from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService


router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create(data)
