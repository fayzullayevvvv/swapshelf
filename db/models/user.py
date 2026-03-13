from datetime import datetime

from sqlalchemy import BigInteger, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from db.base import Base
from db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    books: Mapped["Book"] = relationship("Book", back_populates="added_user")
    swap_requests: Mapped["SwapRequest"] = relationship("SwapRequest", back_populates="requester")

    def __repr__(self):
        return f"User(id={self.id}, full_name={self.full_name})"
