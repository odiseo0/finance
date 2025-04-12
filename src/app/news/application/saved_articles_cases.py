from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.news.domain.entities.saved_articles import (
    SavedArticle,
    SavedArticleCreate,
    SavedArticleUpdate,
)
from src.app.news.domain.repository.daos import dao_saved_articles


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_saved_article(db: AsyncSession, article_id: int) -> SavedArticle:
    data = await dao_saved_articles.get(db, article_id)
    return data


async def get_saved_articles(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[SavedArticle]:
    data = await dao_saved_articles.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_saved_article(
    db: AsyncSession, obj_in: SavedArticleCreate
) -> SavedArticle | None:
    result = await dao_saved_articles.create(db, obj_in=obj_in)
    return result


async def update_saved_article(
    db: AsyncSession,
    article_id: int,
    obj_in: SavedArticleUpdate,
) -> SavedArticle:
    result = await dao_saved_articles.update(db, db_obj_id=article_id, obj_in=obj_in)
    return result


async def remove_saved_article(db: AsyncSession, article_id: int) -> None:
    """Remove a saved article."""
    article = await dao_saved_articles.get(db, article_id)
    await dao_saved_articles.delete(db, article)

    return
