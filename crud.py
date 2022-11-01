from datetime import datetime
from genericpath import exists
from sqlalchemy.orm import Session
import models
import schemas
import shortuuid


def get_urls(db: Session):
    return db.query(models.URL).all()


def get_url(db: Session, short_url: str) -> schemas.URL | None:
    return db.query(models.URL).filter(models.URL.short == short_url).first()


def create_url(db: Session, url: schemas.URLCreate):
    short_url = shortuuid.uuid()
    exists = get_url(db=db, short_url=short_url)

    if (exists):
        return create_url(db=db, url=url)

    db_url = models.URL(short=short_url, long=url.long, date=datetime.now())
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
