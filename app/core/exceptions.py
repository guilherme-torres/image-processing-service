from fastapi import HTTPException


class ApplicationException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = "Internal error."):
        super().__init__(status_code, detail)


class UserAlreadyExists(ApplicationException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists.")


class UserNotFound(ApplicationException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found.")


class InvalidCredentials(ApplicationException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials.")


class InvalidToken(ApplicationException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid token.")


class ExpiredToken(ApplicationException):
    def __init__(self):
        super().__init__(status_code=401, detail="Token has expired.")


class MissingToken(ApplicationException):
    def __init__(self):
        super().__init__(status_code=401, detail="Missing authentication token.")
