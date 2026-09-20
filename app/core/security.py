from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()

security = HTTPBearer()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception


def require_role(required_role: str):

    def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):

        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            user_id = payload.get("sub")
            role = payload.get("role")

            if user_id is None:
                raise credentials_exception

            if role != required_role:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission",
                )

            return int(user_id)

        except (JWTError, ValueError):
            raise credentials_exception

    return role_checker