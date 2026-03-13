from datetime import datetime

from sqlalchemy import ForeignKey, String, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from db.base import Base


class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")

    requested_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    responded_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('Pending', 'Accepted', 'Rejected')",
            name="check_swap_request_status",
        ),
    )

    book: Mapped["Book"] = relationship("Book", back_populates="swap_requests")
    requester: Mapped["User"] = relationship("User", back_populates="swap_requests")