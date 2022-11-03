from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_optional_current_user, get_current_user
from db import schemas, crud
from validators import url as url_validator
from typing import Union

router = APIRouter()

@router.get("/api/shortify", summary="Returns all the urls shortened by the user", response_model=list[schemas.URL])
def get_users_urls(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    return crud.get_urls(db, user=user)

@router.post("/api/shortify", summary="Shortens urls", response_model=schemas.URL)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db), user: Union[schemas.User, None] = Depends(get_optional_current_user)):
    if not url_validator(url.long):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL provided.")
    return crud.create_url(db=db, url=url, user=user)

@router.get("/{short_url}", summary="Redirects to the shortened url")
def redirect(short_url, db: Session = Depends(get_db)):
    db_url = crud.get_url(db=db, short_url=short_url)
    if (db_url):
        return RedirectResponse(db_url.long)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Does not exist"
    )
