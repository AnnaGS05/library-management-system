from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, q: Optional[str] = None) -> List[Book]:
        query = self.db.query(Book)
        if q:
            ilike = f"%{q}%"
            query = query.filter(
                (Book.title.ilike(ilike)) |
                (Book.author.ilike(ilike))
            )
        return query.all()

    def get(self, book_id: int) -> Book | None:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def save(self, book: Book) -> Book:
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book):
        self.db.delete(book)
        self.db.commit()
