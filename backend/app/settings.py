from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "SLH DDOS × BOT_FACTORY – Enterprise API"
    ENVIRONMENT: str = "production"

    PUBLIC_BASE_URL: AnyHttpUrl | None = None
    DOCS_URL: AnyHttpUrl | None = None

    BOT_FACTORY_BASE_URL: AnyHttpUrl | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
