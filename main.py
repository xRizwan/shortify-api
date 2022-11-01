from genericpath import exists
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from database import engine
from sqlalchemy.orm import Session
from deps import get_current_user, get_db, get_optional_current_user
import crud
import models
import schemas
import utils

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get('/api/shortify', response_model=list[schemas.URL])
def get_urls(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    return crud.get_urls(db=db)


@app.post("/api/shortify", response_model=schemas.URL)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    return crud.create_url(db=db, url=url)


@app.get('/api/users', response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)


@app.post('/api/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = crud.get_user(db, username=user.username)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    hashed_password = utils.get_hashed_password(user.password)
    db_user = crud.create_user(
        db, username=user.username, hashed_password=hashed_password
    )
    return db_user


@app.post('/login')
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


@app.get("/{short_url}")
def redirect(short_url, db: Session = Depends(get_db)):
    db_url = crud.get_url(db=db, short_url=short_url)
    if (db_url):
        if ("http" in db_url.long):
            return RedirectResponse(url=db_url.long, headers={})
        else:
            return RedirectResponse(url=f"https://{db_url.long}")
    raise HTTPException(status_code=404, detail="Does not exist")
