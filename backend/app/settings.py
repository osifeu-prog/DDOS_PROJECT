from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the DDOS × BOT_FACTORY Enterprise backend.

    All values can be overridden via environment variables on Railway.
    Only a very small core is required for the Enterprise API service.
    """

    # Basic metadata used by FastAPI for the OpenAPI schema and / endpoint
    PROJECT_NAME: str = "SLH DDOS × BOT_FACTORY Enterprise API"
    VERSION: str = "0.1.0"

    # External documentation site (GitHub Pages)
    DOCS_URL: str | None = None

    # Base URL of the BOT_FACTORY gateway / API that this project integrates with
    BOT_FACTORY_BASE_URL: str | None = None

    # Allow loading from a .env file locally and from plain env vars in Railway
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
