from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.api import auth, books, reservations
from app.init_data import init_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

origins = ["http://localhost:5173", "http://frontend:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reservations.router)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        init_admin(db)
    finally:
        db.close()
