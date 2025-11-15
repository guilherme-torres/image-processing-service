from sqlmodel import select
from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)


    def find_by_username(self, username: str) -> bool:
        user = self.session.exec(select(User).where(User.username == username)).first()
        return True if user is not None else False
