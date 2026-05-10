from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.security import get_current_user
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_service(db: Session = Depends(get_db)) -> ReservationService:
    return ReservationService(db)


@router.post("/", response_model=ReservationRead)
def create_reservation(
    reservation_in: ReservationCreate,
    service: ReservationService = Depends(get_reservation_service),
    current_user=Depends(get_current_user),
):
    try:
        return service.create_reservation(current_user.id, reservation_in)
    except ValueError as e:
        code = str(e)
        if code == "BOOK_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Book not found")
        if code == "BOOK_NOT_AVAILABLE":
            raise HTTPException(status_code=400, detail="Book is not available")
        raise


@router.get("/me", response_model=list[ReservationRead])
def my_reservations(
    service: ReservationService = Depends(get_reservation_service),
    current_user=Depends(get_current_user),
):
    return service.list_user_reservations(current_user.id)
