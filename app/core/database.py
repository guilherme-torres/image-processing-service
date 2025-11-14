from sqlmodel import create_engine, Session
from app.core.config import Config


engine = create_engine(Config().POSTGRES_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
