from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from database import SessionLocal
from jose import jwt
from pydantic import ValidationError
from schemas import User
from schemas import TokenPayload
import crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT",
    auto_error=False
)


async def get_current_user(token: str | None = Depends(reuseable_oauth), db: Session = Depends(get_db)) -> User:
    if (token == None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if (datetime.fromtimestamp(token_data.exp) < datetime.now()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = crud.get_user(db=db, username=token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user


async def get_optional_current_user(token: str | None = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    if token == None:
        return None
    return await get_current_user(token, db)
