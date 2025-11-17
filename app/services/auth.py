from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.exceptions import ExpiredToken, InvalidCredentials, InvalidToken, MissingToken, UserNotFound
from app.core.security import generate_access_token, generate_refresh_token, verify_password, validate_refresh_token
from app.repositories.user import UserRepository
from app.schemas.auth import LoginCreate, LoginResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    
    def login(self, data: LoginCreate) -> LoginResponse:
        user = self.user_repo.find_by_username(data.username)
        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentials
        access_token = generate_access_token({"sub": str(user.id)})
        refresh_token = generate_refresh_token({"sub": str(user.id)})
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    

    def refresh_access_token(self, refresh_token: str) -> LoginResponse:
        try:
            if not refresh_token:
                raise MissingToken
            payload = validate_refresh_token(refresh_token)
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidToken
            user = self.user_repo.get(int(user_id))
            if not user:
                raise UserNotFound
            access_token = generate_access_token({"sub": str(user.id)})
            return LoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            )
        except ExpiredSignatureError:
            raise ExpiredToken
        except InvalidTokenError:
            raise InvalidToken
