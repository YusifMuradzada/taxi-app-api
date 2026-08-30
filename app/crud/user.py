
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(
    db: Session,
    email: str,
):
    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
    db: Session,
    user_data: UserCreate,
):
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user