from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.subscriptions.domain import (
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    dao_subscriptions,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_subscription(db: AsyncSession, subscription_id: int) -> Subscription:
    data = await dao_subscriptions.get(db, subscription_id)
    return data


async def get_subscriptions(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[Subscription]:
    data = await dao_subscriptions.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_subscription(
    db: AsyncSession, obj_in: SubscriptionCreate
) -> Subscription | None:
    result = await dao_subscriptions.create(db, obj_in=obj_in)
    return result


async def update_subscription(
    db: AsyncSession,
    subscription_id: int,
    obj_in: SubscriptionUpdate,
) -> Subscription:
    result = await dao_subscriptions.update(
        db, db_obj_id=subscription_id, obj_in=obj_in
    )
    return result


async def remove_subscription(db: AsyncSession, subscription_id: int) -> None:
    """Ensure we remove the subscription with its payments."""
    subscription = await dao_subscriptions.get(db, subscription_id)
    await dao_subscriptions.delete(db, subscription)

    return
