from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.news.domain.entities.news_sources import (
    NewsSource,
    NewsSourceCreate,
    NewsSourceUpdate,
)
from src.app.news.domain.repository.daos import dao_news_sources


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_news_source(db: AsyncSession, news_source_id: int) -> NewsSource:
    data = await dao_news_sources.get(db, news_source_id)
    return data


async def get_news_sources(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[NewsSource]:
    data = await dao_news_sources.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_news_source(
    db: AsyncSession, obj_in: NewsSourceCreate
) -> NewsSource | None:
    result = await dao_news_sources.create(db, obj_in=obj_in)
    return result


async def update_news_source(
    db: AsyncSession,
    news_source_id: int,
    obj_in: NewsSourceUpdate,
) -> NewsSource:
    result = await dao_news_sources.update(db, db_obj_id=news_source_id, obj_in=obj_in)
    return result


async def remove_news_source(db: AsyncSession, news_source_id: int) -> None:
    """Ensure we remove the news source with its subscriptions."""
    news_source = await dao_news_sources.get(db, news_source_id)
    await dao_news_sources.delete(db, news_source)

    return
