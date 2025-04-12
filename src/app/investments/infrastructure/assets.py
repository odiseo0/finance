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
    create_asset,
    get_asset,
    get_assets,
    remove_asset,
    update_asset,
)
from src.app.investments.domain.entities.assets import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
)


@get("/{asset_id:int}", summary="Get one Asset", status_code=HTTP_200_OK)
async def read(asset_id: int, db: AsyncSession, state: ImmutableState) -> AssetResponse:
    data = await get_asset(db, asset_id)

    if data is None:
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return AssetResponse.model_validate(data, context=state.settings)


@get("/", summary="Get assets", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=100, ge=10, query="shows")],
    asset_type: Annotated[
        str | None, Parameter(query="asset_type", default=None, required=False)
    ],
    state: ImmutableState,
) -> list[AssetResponse]:
    filters = {}

    if asset_type:
        filters["asset_type"] = asset_type

    data = await get_assets(db, page=page, shows=shows, filters=filters)

    return [AssetResponse.model_validate(item, context=state.settings) for item in data]


@post("/", summary="Create Asset", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[AssetCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetResponse:
    result = await create_asset(db, data)

    if result is None:
        raise HTTPException(
            detail="Error creating asset.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetResponse.model_validate(result, context=state.settings)


@put("/{asset_id:int}", summary="Update Asset", status_code=HTTP_200_OK)
async def edit(
    asset_id: int,
    data: Annotated[AssetUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetResponse:
    result = await update_asset(db, asset_id, data)

    if result is None:
        raise HTTPException(
            detail="Error updating asset.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetResponse.model_validate(result, context=state.settings)


@delete(
    "/{asset_id:int}",
    summary="Delete Asset",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(asset_id: int, db: AsyncSession) -> None:
    await remove_asset(db, asset_id)
