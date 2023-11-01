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
    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: str
    #: str: Postgresql database name.
    POSTGRES_DB: str

    TEST_HOST: str
    TEST_DB: str

    model_config = SettingsConfigDict(env_file=find_dotenv(".env"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
