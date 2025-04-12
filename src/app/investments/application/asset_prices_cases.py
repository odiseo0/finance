from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.investments.domain.entities.asset_prices import (
    AssetPrice,
    AssetPriceCreate,
    AssetPriceUpdate,
)
from src.app.investments.domain.repository.daos import dao_asset_prices


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_asset_price(db: AsyncSession, price_id: int) -> AssetPrice:
    """
    Retrieve a single asset price by its ID.

    Args:
        db: The database session
        price_id: The ID of the asset price to retrieve

    Returns:
        The asset price with the specified ID
    """
    data = await dao_asset_prices.get(db, price_id)
    return data


async def get_asset_prices(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[AssetPrice]:
    """
    Retrieve multiple asset prices with pagination and filtering.

    Args:
        db: The database session
        page: The page number (1-indexed)
        shows: The number of items per page
        filters: Optional filters to apply to the query

    Returns:
        A list of asset prices matching the criteria
    """
    data = await dao_asset_prices.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_asset_price(
    db: AsyncSession, obj_in: AssetPriceCreate
) -> AssetPrice | None:
    """
    Create a new asset price.

    Args:
        db: The database session
        obj_in: The asset price data to create

    Returns:
        The created asset price or None if creation failed
    """
    result = await dao_asset_prices.create(db, obj_in=obj_in)
    return result


async def update_asset_price(
    db: AsyncSession,
    price_id: int,
    obj_in: AssetPriceUpdate,
) -> AssetPrice:
    """
    Update an existing asset price.

    Args:
        db: The database session
        price_id: The ID of the asset price to update
        obj_in: The updated asset price data

    Returns:
        The updated asset price
    """
    result = await dao_asset_prices.update(db, db_obj_id=price_id, obj_in=obj_in)
    return result


async def remove_asset_price(db: AsyncSession, price_id: int) -> None:
    """
    Remove an asset price.

    Args:
        db: The database session
        price_id: The ID of the asset price to remove
    """
    asset_price = await dao_asset_prices.get(db, price_id)
    await dao_asset_prices.delete(db, asset_price)

    return
