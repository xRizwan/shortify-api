from pydantic import BaseModel
import datetime


class URLBase(BaseModel):
    long: str


class URLCreate(URLBase):
    pass


class URL(URLBase):
    id: int
    short: str
    date: datetime.datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    urls: list[URL] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
