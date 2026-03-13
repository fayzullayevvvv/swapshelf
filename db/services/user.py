from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from db.models import User


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, telegram_id, full_name, phone_number) -> User:
        existing_user = self.get_user_by_telegram_id(telegram_id=telegram_id)

        if existing_user:
            return existing_user
        
        user = User(
            telegram_id=telegram_id, 
            full_name=full_name, 
            phone_number=phone_number
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user

    def get_user(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.scalar(stmt)

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()
    