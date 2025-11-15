from fastapi import HTTPException


class ApplicationException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = "Erro interno na aplicação."):
        super().__init__(status_code, detail)


class UserAlreadyExists(ApplicationException):
    def __init__(self):
        super().__init__(status_code=409, detail="Este usuário já existe.")