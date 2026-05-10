from typing import List
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.reservation import Reservation
from app.repositories.book_repository import BookRepository
from app.schemas.reservation import ReservationCreate


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.books = BookRepository(db)

    def create_reservation(self, user_id: int, data: ReservationCreate):
        book = self.books.get(data.book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        if not book.available:
            raise ValueError("BOOK_NOT_AVAILABLE")

        reservation = Reservation(
            user_id=user_id,
            book_id=data.book_id,
        )
        book.available = False
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def list_user_reservations(self, user_id: int) -> List[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.user_id == user_id)
            .order_by(Reservation.created_at.desc())
            .all()
        )
