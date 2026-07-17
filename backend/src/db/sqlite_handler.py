"""Sqlite handler module."""

from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from src.settings import settings


class SqliteHandler:
    """Sqlite handler class."""

    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(
            settings.db_settings.db_url,
            echo=settings.db_settings.DB_ECHO,
        )
        self.session_maker: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                class_=AsyncSession,
                autoflush=False,
            )
        )

    async def dispose(self) -> None:
        """Dispose of the connection pool."""
        await self.engine.dispose()


async def get_lite_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """Get dependency for session retrival for the app."""
    lite: SqliteHandler = request.app.state.db
    async with lite.session_maker() as session:
        yield session
