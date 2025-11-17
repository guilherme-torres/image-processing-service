from sqlmodel import SQLModel


class LoginCreate(SQLModel):
    username: str
    password: str


class LoginResponse(SQLModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(SQLModel):
    refresh_token: str
