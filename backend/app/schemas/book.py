from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int | None = None
    description: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    available: bool | None = None


class BookRead(BookBase):
    id: int
    available: bool

    class Config:
        orm_mode = True
