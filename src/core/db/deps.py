from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from .session import async_session_factory


async def get_db() -> AsyncIterator[AsyncSession]:
    """Dependency that yields an `AsyncSession` for accessing the database."""
    async with async_session_factory() as db:
        try:
            yield db
        except Exception:
            raise
        finally:
            await db.close()


@asynccontextmanager
async def session() -> AsyncIterator[AsyncSession]:
    """Use this in case you can't use dependency injection."""
    async with async_session_factory() as db:
        yield db
