from db.base import Base
from db.session import engine

from db.models.user import User
from db.models.book import Book
from db.models.genres import Genre
from db.models.swap_request import SwapRequest

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")