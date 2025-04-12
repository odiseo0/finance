from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.app.investments.domain.entities.benchmarks import (
    AssetBenchmark,
    AssetBenchmarkCreate,
    AssetBenchmarkUpdate,
)
from src.app.investments.domain.repository.daos import dao_asset_benchmarks


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_asset_benchmark(db: AsyncSession, benchmark_id: int) -> AssetBenchmark:
    """
    Retrieve a single asset benchmark by its ID.

    Args:
        db: The database session
        benchmark_id: The ID of the asset benchmark to retrieve

    Returns:
        The asset benchmark with the specified ID
    """
    data = await dao_asset_benchmarks.get(db, benchmark_id)
    return data


async def get_asset_benchmarks(
    db: AsyncSession,
    page: int = 1,
    shows: int = 100,
    filters: dict[str, Any] | None = None,
) -> list[AssetBenchmark]:
    """
    Retrieve multiple asset benchmarks with pagination and filtering.

    Args:
        db: The database session
        page: The page number (1-indexed)
        shows: The number of items per page
        filters: Optional filters to apply to the query

    Returns:
        A list of asset benchmarks matching the criteria
    """
    data = await dao_asset_benchmarks.get_multi(
        db,
        where=filters,
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def create_asset_benchmark(
    db: AsyncSession, obj_in: AssetBenchmarkCreate
) -> AssetBenchmark | None:
    """
    Create a new asset benchmark.

    Args:
        db: The database session
        obj_in: The asset benchmark data to create

    Returns:
        The created asset benchmark or None if creation failed
    """
    result = await dao_asset_benchmarks.create(db, obj_in=obj_in)
    return result


async def update_asset_benchmark(
    db: AsyncSession,
    benchmark_id: int,
    obj_in: AssetBenchmarkUpdate,
) -> AssetBenchmark:
    """
    Update an existing asset benchmark.

    Args:
        db: The database session
        benchmark_id: The ID of the asset benchmark to update
        obj_in: The updated asset benchmark data

    Returns:
        The updated asset benchmark
    """
    result = await dao_asset_benchmarks.update(
        db, db_obj_id=benchmark_id, obj_in=obj_in
    )
    return result


async def remove_asset_benchmark(db: AsyncSession, benchmark_id: int) -> None:
    """
    Remove an asset benchmark.

    Args:
        db: The database session
        benchmark_id: The ID of the asset benchmark to remove
    """
    asset_benchmark = await dao_asset_benchmarks.get(db, benchmark_id)
    await dao_asset_benchmarks.delete(db, asset_benchmark)

    return
