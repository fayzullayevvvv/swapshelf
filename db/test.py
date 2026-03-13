from db.base import Base
from db.session import engine
from db.models import *
from db.session import SessionLocal
from db.services.user import UserService


session = SessionLocal()
user_service = UserService(session)


def create_tables():
    Base.metadata.create_all(bind=engine)
