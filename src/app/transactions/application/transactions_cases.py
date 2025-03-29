from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.transactions.domain import (
    Transaction,
    TransactionCreate,
    TransactionUpdate,
    dao_transactions,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_transaction(db: AsyncSession, transaction_id: int) -> Transaction:
    data = await dao_transactions.get(db, transaction_id)
    return data


async def get_transactions(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[Transaction]:
    data = await dao_transactions.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_transaction(
    db: AsyncSession, obj_in: TransactionCreate
) -> Transaction | None:
    result = await dao_transactions.create(db, obj_in=obj_in)
    return result


async def update_transaction(
    db: AsyncSession,
    transaction_id: int,
    obj_in: TransactionUpdate,
) -> Transaction:
    result = await dao_transactions.update(db, db_obj_id=transaction_id, obj_in=obj_in)
    return result


async def remove_transaction(db: AsyncSession, transaction_id: int) -> None:
    """Ensure we remove the transaction with its files."""
    transaction = await dao_transactions.get(db, transaction_id)
    await dao_transactions.delete(db, transaction)

    return
