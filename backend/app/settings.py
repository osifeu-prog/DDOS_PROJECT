from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ============================
    #  CORE PROJECT CONFIG
    # ============================
    PROJECT_NAME: str = Field(
        default="SLH DDOS × BOT_FACTORY – Enterprise Backend",
        description="Project display name."
    )

    VERSION: str = Field(
        default="0.1.0",
        description="Backend version (overridden by Railway env if exists)."
    )

    ENVIRONMENT: str = Field(
        default="production",
        description="Environment name: local / staging / production."
    )

    PUBLIC_BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Base URL of this service."
    )

    DOCS_URL: str | None = Field(
        default=None,
        description="Public link to investor documentation (GitHub Pages)."
    )

    BOT_FACTORY_BASE_URL: str | None = Field(
        default=None,
        description="Internal link to BOT_FACTORY microservice."
    )

    # ============================
    #  BOT CONFIG
    # ============================
    BOT_TOKEN: str | None = None
    SECRET_KEY: str | None = None
    ADMIN_USER_ID: str | None = None

    WEBHOOK_URL: str | None = Field(
        default=None,
        description="Webhook endpoint for Telegram updates."
    )

    DEFAULT_LANGUAGE: str = "he"
    SUPPORTED_LANGUAGES: str = "he,en,ru,es"

    # ============================
    #  BLOCKCHAIN CONFIG
    # ============================
    COMMUNITY_WALLET_ADDRESS: str | None = None
    COMMUNITY_WALLET_PRIVATE_KEY: str | None = None

    SLH_TOKEN_ADDRESS: str | None = None
    SLH_TOKEN_DECIMALS: int = 15
    SLH_PRICE_NIS: float = 444.0

    BSC_RPC_URL: str = "https://bsc-dataseed.binance.org"
    BSC_SCAN_BASE: str = "https://bscscan.com"

    # ============================
    #  TELEGRAM LOG CHANNELS
    # ============================
    MAIN_COMMUNITY_CHAT_ID: str | None = None
    LOG_NEW_USERS_CHAT_ID: str | None = None
    LOG_TRANSACTIONS_CHAT_ID: str | None = None
    LOG_ERRORS_CHAT_ID: str | None = None
    REFERRAL_LOGS_CHAT_ID: str | None = None

    # ============================
    #  DATABASE
    # ============================
    DATABASE_URL: str | None = None

    # ============================
    #  LOAD .env IF EXISTS
    # ============================
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global instance used across the project
settings = Settings()
