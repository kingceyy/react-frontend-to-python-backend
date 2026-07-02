import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/clubjm"
    )

    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_webhook_secret: str = os.getenv("TELEGRAM_WEBHOOK_SECRET", "secret")
    telegram_channel_id: int = int(os.getenv("TELEGRAM_CHANNEL_ID", "-1002632653839"))

    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key")
    jwt_algorithm: str = "HS256"

    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "https://clubjm.vercel.app")

    # Environment
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"


settings = Settings()
