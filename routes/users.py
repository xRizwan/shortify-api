from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies import get_db
import db.schemas as schemas
import db.crud as crud
import utils

router = APIRouter()


@router.post('/api/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = crud.get_user(db, username=user.username)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists."
        )

    hashed_password = utils.get_hashed_password(user.password)
    db_user = crud.create_user(
        db, username=user.username,
        hashed_password=hashed_password
    )
    return db_user


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user(db=db, username=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {
        "access_token": utils.create_access_token(user.username),
        "refresh_token": utils.create_refresh_token(user.username),
    }
