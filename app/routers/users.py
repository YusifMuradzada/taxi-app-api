from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.db.database import get_db
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def get_me(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    return db.query(User).filter(
        User.id == current_user_id
    ).first()