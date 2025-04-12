from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.investments.domain.entities.assets import Asset, AssetCreate, AssetUpdate
from src.app.investments.domain.repository.daos import dao_assets


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_asset(db: AsyncSession, asset_id: int) -> Asset:
    """
    Retrieve a single asset by its ID.

    Args:
        db: The database session
        asset_id: The ID of the asset to retrieve

    Returns:
        The asset with the specified ID
    """
    data = await dao_assets.get(db, asset_id)
    return data


async def get_assets(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[Asset]:
    """
    Retrieve multiple assets with pagination and filtering.

    Args:
        db: The database session
        page: The page number (1-indexed)
        shows: The number of items per page
        filters: Optional filters to apply to the query

    Returns:
        A list of assets matching the criteria
    """
    data = await dao_assets.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_asset(db: AsyncSession, obj_in: AssetCreate) -> Asset | None:
    """
    Create a new asset.

    Args:
        db: The database session
        obj_in: The asset data to create

    Returns:
        The created asset or None if creation failed
    """
    result = await dao_assets.create(db, obj_in=obj_in)
    return result


async def update_asset(
    db: AsyncSession,
    asset_id: int,
    obj_in: AssetUpdate,
) -> Asset:
    """
    Update an existing asset.

    Args:
        db: The database session
        asset_id: The ID of the asset to update
        obj_in: The updated asset data

    Returns:
        The updated asset
    """
    result = await dao_assets.update(db, db_obj_id=asset_id, obj_in=obj_in)
    return result


async def remove_asset(db: AsyncSession, asset_id: int) -> None:
    """
    Remove an asset and its related data.

    Args:
        db: The database session
        asset_id: The ID of the asset to remove
    """
    asset = await dao_assets.get(db, asset_id)
    await dao_assets.delete(db, asset)

    return
