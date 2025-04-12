from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.news.domain.entities.newsletter_subscriptions import (
    NewsletterSubscription,
    NewsletterSubscriptionCreate,
    NewsletterSubscriptionUpdate,
)
from src.app.news.domain.repository.daos import dao_newsletter_subscriptions


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_newsletter_subscription(
    db: AsyncSession, subscription_id: int
) -> NewsletterSubscription:
    data = await dao_newsletter_subscriptions.get(db, subscription_id)
    return data


async def get_newsletter_subscriptions(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[NewsletterSubscription]:
    data = await dao_newsletter_subscriptions.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_newsletter_subscription(
    db: AsyncSession, obj_in: NewsletterSubscriptionCreate
) -> NewsletterSubscription | None:
    result = await dao_newsletter_subscriptions.create(db, obj_in=obj_in)
    return result


async def update_newsletter_subscription(
    db: AsyncSession,
    subscription_id: int,
    obj_in: NewsletterSubscriptionUpdate,
) -> NewsletterSubscription:
    result = await dao_newsletter_subscriptions.update(
        db, db_obj_id=subscription_id, obj_in=obj_in
    )
    return result


async def remove_newsletter_subscription(
    db: AsyncSession, subscription_id: int
) -> None:
    """Ensure we remove the newsletter subscription with its saved articles."""
    subscription = await dao_newsletter_subscriptions.get(db, subscription_id)
    await dao_newsletter_subscriptions.delete(db, subscription)

    return
