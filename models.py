from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    short = Column(String)
    long = Column(String)
    date = Column(DateTime, default=datetime.now())

    user = Column(ForeignKey('users.id'), nullable=True, default=None)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    urls = relationship("URL", backref="user_urls")
