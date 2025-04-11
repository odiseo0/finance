from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.subscriptions.domain import (
    SubscriptionPayment,
    SubscriptionPaymentCreate,
    SubscriptionPaymentUpdate,
    dao_subscription_payments,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_subscription_payment(
    db: AsyncSession, payment_id: int
) -> SubscriptionPayment:
    data = await dao_subscription_payments.get(db, payment_id)
    return data


async def get_subscription_payments(
    db: AsyncSession,
    subscription_id: int | None = None,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[SubscriptionPayment]:
    if subscription_id:
        filters = filters or {}
        filters["subscription_id"] = subscription_id

    data = await dao_subscription_payments.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_subscription_payment(
    db: AsyncSession, obj_in: SubscriptionPaymentCreate
) -> SubscriptionPayment | None:
    result = await dao_subscription_payments.create(db, obj_in=obj_in)
    return result


async def update_subscription_payment(
    db: AsyncSession,
    payment_id: int,
    obj_in: SubscriptionPaymentUpdate,
) -> SubscriptionPayment:
    result = await dao_subscription_payments.update(
        db, db_obj_id=payment_id, obj_in=obj_in
    )
    return result


async def remove_subscription_payment(db: AsyncSession, payment_id: int) -> None:
    payment = await dao_subscription_payments.get(db, payment_id)
    await dao_subscription_payments.delete(db, payment)

    return
