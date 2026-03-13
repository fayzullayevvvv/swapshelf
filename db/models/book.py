from datetime import datetime

from sqlalchemy import (
    DateTime,
    BigInteger,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base
from db.mixins import TimestampMixin


class BookStatus:
    NEW = 'New'
    GOOD = 'Good'
    FAIR = 'Fair'
    WORN = 'Worn'

class BookType:
    BORROW = 'Borrow'
    PERMANENT = 'Permanent'
    BOTH = 'Both'

class Book(Base, TimestampMixin):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)

    genre_id: Mapped[int | None] = mapped_column(
        ForeignKey("genres.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text(f"'{BookStatus.NEW}'")
    )

    book_type: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text(f"'{BookType.BORROW}'")
    )

    rating: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    added_by: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('New', 'Good', 'Fair', 'Worn')", name="check_book_status"
        ),
        CheckConstraint(
            "book_type IN ('Borrow', 'Permanent', 'Both')", name="check_book_type"
        ),
    )

    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    added_user: Mapped["User"] = relationship("User", back_populates="books")
    swap_requests: Mapped["SwapRequest"] = relationship("SwapRequest", back_populates="book")