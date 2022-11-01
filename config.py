from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
