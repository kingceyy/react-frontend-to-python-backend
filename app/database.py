import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.config import settings
from app.models import Base

logger = logging.getLogger(__name__)

# Convert postgresql:// to postgresql+asyncpg://
database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Migration: telegram_id must be BIGINT (Telegram IDs exceed int32)
    async with engine.begin() as conn:
        await conn.execute(
            text("ALTER TABLE users ALTER COLUMN telegram_id TYPE BIGINT")
        )
    logger.info("Database tables created")


async def get_session() -> AsyncSession:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session
