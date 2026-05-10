from sqlalchemy.orm import Session
from app.models.user import User
from app.security import get_password_hash


def init_admin(db: Session):
    admin_email = "admin@local"
    admin = db.query(User).filter(User.email == admin_email).first()
    if admin:
        return

    admin = User(
        email=admin_email,
        full_name="Администратор системы",
        hashed_password=get_password_hash("admin"),
        is_active=True,
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    print(">>> Создан админ: admin@local / admin")
