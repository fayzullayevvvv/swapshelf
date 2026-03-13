from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from db.base import Base


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    books: Mapped["Book"] = relationship("Book", back_populates="genre")