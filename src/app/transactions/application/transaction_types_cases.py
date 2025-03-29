from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.transactions.domain import dao_transaction_types


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.app.transactions.domain import (
        TransactionType,
        TransactionTypeCreate,
        TransactionTypeUpdate,
    )


async def get_one_transaction_type(
    db: AsyncSession, transaction_type_id: int
) -> TransactionType:
    data = await dao_transaction_types.get(db, transaction_type_id)
    return data


async def get_transaction_types(
    db: AsyncSession,
    page: int = 1,
    shows: int = 20,
    filters: dict[str, Any] | None = None,
) -> tuple[list[TransactionType], int]:
    data, count = await dao_transaction_types.get_multi(
        db,
        page=(page - 1) * shows,
        shows=shows,
        where=filters,
    )

    return (data, count)


async def create_transaction_type(
    db: AsyncSession, obj_in: TransactionTypeCreate
) -> TransactionType:
    result = await dao_transaction_types.create(db, obj_in=obj_in)
    return result


async def update_transaction_type(
    db: AsyncSession,
    transaction_type_id: int,
    obj_in: TransactionTypeUpdate,
) -> TransactionType:
    result = await dao_transaction_types.update(db, transaction_type_id, obj_in)
    return result


async def remove_transaction_type(db: AsyncSession, transaction_type_id: int) -> None:
    transaction_type = await dao_transaction_types.get(db, transaction_type_id)
    await dao_transaction_types.delete(db, transaction_type)

    return
