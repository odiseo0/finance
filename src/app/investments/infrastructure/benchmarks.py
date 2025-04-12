from typing import Annotated

from litestar import delete, get, post, put
from litestar.datastructures import ImmutableState
from litestar.exceptions import HTTPException
from litestar.params import Body, Parameter
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.investments.application import (
    create_asset_benchmark,
    get_asset_benchmark,
    get_asset_benchmarks,
    remove_asset_benchmark,
    update_asset_benchmark,
)
from src.app.investments.domain.entities.benchmarks import (
    AssetBenchmarkCreate,
    AssetBenchmarkResponse,
    AssetBenchmarkUpdate,
)


@get("/{benchmark_id:int}", summary="Get one Asset Benchmark", status_code=HTTP_200_OK)
async def read(
    benchmark_id: int, db: AsyncSession, state: ImmutableState
) -> AssetBenchmarkResponse:
    data = await get_asset_benchmark(db, benchmark_id)

    if data is None:
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return AssetBenchmarkResponse.model_validate(data, context=state.settings)


@get("/", summary="Get asset benchmarks", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=100, ge=10, query="shows")],
    asset_id: Annotated[
        int | None, Parameter(query="asset_id", default=None, required=False)
    ],
    state: ImmutableState,
) -> list[AssetBenchmarkResponse]:
    filters = {}

    if asset_id:
        filters["asset_id"] = asset_id

    data = await get_asset_benchmarks(db, page=page, shows=shows, filters=filters)

    return [
        AssetBenchmarkResponse.model_validate(item, context=state.settings)
        for item in data
    ]


@post("/", summary="Create Asset Benchmark", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[AssetBenchmarkCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetBenchmarkResponse:
    result = await create_asset_benchmark(db, data)

    if result is None:
        raise HTTPException(
            detail="Error creating asset benchmark.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetBenchmarkResponse.model_validate(result, context=state.settings)


@put("/{benchmark_id:int}", summary="Update Asset Benchmark", status_code=HTTP_200_OK)
async def edit(
    benchmark_id: int,
    data: Annotated[AssetBenchmarkUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetBenchmarkResponse:
    result = await update_asset_benchmark(db, benchmark_id, data)

    if result is None:
        raise HTTPException(
            detail="Error updating asset benchmark.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetBenchmarkResponse.model_validate(result, context=state.settings)


@delete(
    "/{benchmark_id:int}",
    summary="Delete Asset Benchmark",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(benchmark_id: int, db: AsyncSession) -> None:
    await remove_asset_benchmark(db, benchmark_id)
