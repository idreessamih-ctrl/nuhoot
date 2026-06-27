"""Application settings via pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All app configuration. Load from .env or environment variables."""

    # Database
    database_url: str = "postgresql://nuhoot:changeme@localhost:5432/nuhoot"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI (GLM 5.2 via umans.ai)
    umans_api_key: str = ""
    ai_model: str = "umans-glm-5.2"
    ai_base_url: str = "https://api.code.umans.ai/v1"

    # WhatsApp Cloud API
    whatsapp_phone_number_id: str = ""
    whatsapp_access_token: str = ""
    whatsapp_business_account_id: str = ""
    whatsapp_webhook_verify_token: str = ""

    # Google Maps Scraper
    gosom_binary_path: str = "/usr/local/bin/gosom"
    scraper_max_results: int = 200
    scraper_delay_seconds: int = 2

    # App
    app_env: str = "development"
    app_secret_key: str = "change-this-in-production"
    app_timezone: str = "Asia/Riyadh"
    app_language: str = "ar"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
