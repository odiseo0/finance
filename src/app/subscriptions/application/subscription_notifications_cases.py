from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.subscriptions.domain import (
    SubscriptionNotification,
    SubscriptionNotificationCreate,
    SubscriptionNotificationUpdate,
    dao_subscription_notifications,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_subscription_notification(
    db: AsyncSession, notification_id: int
) -> SubscriptionNotification:
    data = await dao_subscription_notifications.get(db, notification_id)
    return data


async def get_subscription_notifications(
    db: AsyncSession,
    subscription_id: int | None = None,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[SubscriptionNotification]:
    if subscription_id:
        filters = filters or {}
        filters["subscription_id"] = subscription_id

    data = await dao_subscription_notifications.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_subscription_notification(
    db: AsyncSession, obj_in: SubscriptionNotificationCreate
) -> SubscriptionNotification | None:
    result = await dao_subscription_notifications.create(db, obj_in=obj_in)
    return result


async def update_subscription_notification(
    db: AsyncSession,
    notification_id: int,
    obj_in: SubscriptionNotificationUpdate,
) -> SubscriptionNotification:
    result = await dao_subscription_notifications.update(
        db, db_obj_id=notification_id, obj_in=obj_in
    )
    return result


async def remove_subscription_notification(
    db: AsyncSession, notification_id: int
) -> None:
    notification = await dao_subscription_notifications.get(db, notification_id)
    await dao_subscription_notifications.delete(db, notification)

    return
