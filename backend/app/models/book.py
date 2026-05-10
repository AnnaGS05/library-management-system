from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    available = Column(Boolean, default=True)
