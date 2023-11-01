from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import PositiveInt

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    API_SERVER_PORT: PositiveInt
    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MIN_COLS: PositiveInt
    MAX_COLS: PositiveInt
    MAX_ROWS: PositiveInt

    model_config = SettingsConfigDict(env_file=find_dotenv(".env"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
