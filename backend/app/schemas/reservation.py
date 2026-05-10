from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    book_id: int


class ReservationRead(BaseModel):
    id: int
    book_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
