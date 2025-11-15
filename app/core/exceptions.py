from fastapi import HTTPException


class ApplicationException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = "Internal error."):
        super().__init__(status_code, detail)


class UserAlreadyExists(ApplicationException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists.")


class InvalidCredentials(ApplicationException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials.")
