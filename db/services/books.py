from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from models import Book, Genre, User, BookStatus


class BookService:
    def __init__(self, session: Session) -> Book:
        self.session = session

        def create_book(
            self,
            title: str,
            author: str,
            genre_id: int | None = None,
            status: str = "New",
            type: str = "Borrow",
            rating: int = 0,
            added_by: int | None = None,
        ) -> Book:
            if genre_id:
                genre = self.session.query(Genre).get(genre_id)
            if genre is None:
                raise ValueError("Genre not found")

            if added_by:
                user = self.session.query(User).get(added_by)
                if user is None:
                    raise ValueError("User not found")

            if status not in ("New", "Good", "Fair", "Worn"):
                raise ValueError("Invalid status")

            if type not in ("Borrow", "Permanent", "Both"):
                raise ValueError("Invalid type")

            book = Book(
                title=title,
                author=author,
                genre_id=genre_id,
                status=status,
                type=type,
                rating=rating,
                added_by=added_by,
            )

            self.session.add(book)
            self.session.commit()
            self.session.refresh(book)

            return book

        def get_my_books(self, telegram_id: int) -> list[Book]:
            stmt = select(Book).where(Book.added_by == telegram_id)
            result = self.session.execute(stmt)
            return result.scalars().all()

        def get_book(self, book_id: int) -> Book | None:
            stmt = select(Book).where(Book.id == book_id)
            result = self.session.execute(stmt)
            return result.scalar_one_or_none()

        def save_channel_message_id(self, book_id: int, message_id: int) -> None:
            book = self.session.query(Book).get(book_id)
            if book:
                book.channel_message_id = message_id
                self.session.commit()
