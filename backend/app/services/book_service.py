from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, db: Session):
        self.repo = BookRepository(db)

    def list_books(self, q: Optional[str] = None) -> List[Book]:
        return self.repo.list(q=q)

    def get_book(self, book_id: int):
        book = self.repo.get(book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        return book

    def create_book(self, data: BookCreate) -> Book:
        book = Book(**data.dict())
        return self.repo.create(book)

    def update_book(self, book_id: int, data: BookUpdate):
        book = self.get_book(book_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(book, field, value)
        return self.repo.save(book)

    def delete_book(self, book_id: int):
        book = self.get_book(book_id)
        self.repo.delete(book)
