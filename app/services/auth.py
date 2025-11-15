from app.core.exceptions import InvalidCredentials
from app.core.security import generate_access_token, generate_refresh_token, verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import LoginCreate, LoginResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    
    def login(self, data: LoginCreate) -> LoginResponse:
        user = self.user_repo.find_by_username(data.username)
        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentials
        access_token = generate_access_token({"sub": user.id})
        refresh_token = generate_refresh_token({"sub": user.id})
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
