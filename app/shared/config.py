from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    ENV: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
