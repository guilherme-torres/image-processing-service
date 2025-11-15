from app.core.exceptions import UserAlreadyExists
from app.core.security import get_password_hash
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    
    def create(self, data: UserCreate) -> UserResponse:
        user_exists = self.user_repo.find_by_username(data.username)
        if user_exists:
            raise UserAlreadyExists
        user = self.user_repo.create({
            "username": data.username,
            "password_hash": get_password_hash(data.password),
        })
        return UserResponse(id=user.id, username=user.username)
