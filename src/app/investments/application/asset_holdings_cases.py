from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.investments.domain.entities.asset_holdings import (
    AssetHolding,
    AssetHoldingCreate,
    AssetHoldingUpdate,
)
from src.app.investments.domain.repository.daos import dao_asset_holdings


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_asset_holding(db: AsyncSession, holding_id: int) -> AssetHolding:
    """
    Retrieve a single asset holding by its ID.

    Args:
        db: The database session
        holding_id: The ID of the asset holding to retrieve

    Returns:
        The asset holding with the specified ID
    """
    data = await dao_asset_holdings.get(db, holding_id)
    return data


async def get_asset_holdings(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[AssetHolding]:
    """
    Retrieve multiple asset holdings with pagination and filtering.

    Args:
        db: The database session
        page: The page number (1-indexed)
        shows: The number of items per page
        filters: Optional filters to apply to the query

    Returns:
        A list of asset holdings matching the criteria
    """
    data = await dao_asset_holdings.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_asset_holding(
    db: AsyncSession, obj_in: AssetHoldingCreate
) -> AssetHolding | None:
    """
    Create a new asset holding.

    Args:
        db: The database session
        obj_in: The asset holding data to create

    Returns:
        The created asset holding or None if creation failed
    """
    result = await dao_asset_holdings.create(db, obj_in=obj_in)
    return result


async def update_asset_holding(
    db: AsyncSession,
    holding_id: int,
    obj_in: AssetHoldingUpdate,
) -> AssetHolding:
    """
    Update an existing asset holding.

    Args:
        db: The database session
        holding_id: The ID of the asset holding to update
        obj_in: The updated asset holding data

    Returns:
        The updated asset holding
    """
    result = await dao_asset_holdings.update(db, db_obj_id=holding_id, obj_in=obj_in)
    return result


async def remove_asset_holding(db: AsyncSession, holding_id: int) -> None:
    """
    Remove an asset holding.

    Args:
        db: The database session
        holding_id: The ID of the asset holding to remove
    """
    asset_holding = await dao_asset_holdings.get(db, holding_id)
    await dao_asset_holdings.delete(db, asset_holding)

    return
