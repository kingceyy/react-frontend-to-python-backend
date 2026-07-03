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

    # Admins: liste de Telegram IDs separes par des virgules
    # Exemple: ADMIN_IDS=8467461906,123456789
    admin_ids_raw: str = os.getenv("ADMIN_IDS", "")

    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key")
    jwt_algorithm: str = "HS256"

    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "https://clubjm.vercel.app")

    # Environment
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    @property
    def admin_ids(self) -> set[int]:
        """Parse ADMIN_IDS env var into a set of Telegram IDs"""
        ids = set()
        for part in self.admin_ids_raw.split(","):
            part = part.strip()
            if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
                ids.add(int(part))
        return ids

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
