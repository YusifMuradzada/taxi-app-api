from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.crud.user import create_user, get_user_by_email
from app.db.database import get_db
from app.schemas.user import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    return create_user(db, user_data)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(
        db,
        user_data.email,
    )

    if not user or not verify_password(
        user_data.password,
        user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }