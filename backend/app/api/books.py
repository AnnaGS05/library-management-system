from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.security import get_current_admin
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)


@router.get("/", response_model=list[BookRead])
def list_books(
    q: str | None = Query(default=None),
    service: BookService = Depends(get_book_service),
):
    return service.list_books(q=q)


@router.get("/{book_id}", response_model=BookRead)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    try:
        return service.get_book(book_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.post("/", response_model=BookRead)
def create_book(
    book_in: BookCreate,
    service: BookService = Depends(get_book_service),
    _: str = Depends(get_current_admin),
):
    return service.create_book(book_in)


@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    service: BookService = Depends(get_book_service),
    _: str = Depends(get_current_admin),
):
    try:
        return service.update_book(book_id, book_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
    _: str = Depends(get_current_admin),
):
    try:
        service.delete_book(book_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
