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
    create_asset_holding,
    get_asset_holding,
    get_asset_holdings,
    remove_asset_holding,
    update_asset_holding,
)
from src.app.investments.domain.entities.asset_holdings import (
    AssetHoldingCreate,
    AssetHoldingResponse,
    AssetHoldingUpdate,
)


@get("/{holding_id:int}", summary="Get one Asset Holding", status_code=HTTP_200_OK)
async def read(
    holding_id: int, db: AsyncSession, state: ImmutableState
) -> AssetHoldingResponse:
    data = await get_asset_holding(db, holding_id)

    if data is None:
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return AssetHoldingResponse.model_validate(data, context=state.settings)


@get("/", summary="Get asset holdings", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=100, ge=10, query="shows")],
    asset_id: Annotated[
        int | None, Parameter(query="asset_id", default=None, required=False)
    ],
    state: ImmutableState,
) -> list[AssetHoldingResponse]:
    filters = {}

    if asset_id:
        filters["asset_id"] = asset_id

    data = await get_asset_holdings(db, page=page, shows=shows, filters=filters)

    return [
        AssetHoldingResponse.model_validate(item, context=state.settings)
        for item in data
    ]


@post("/", summary="Create Asset Holding", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[AssetHoldingCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetHoldingResponse:
    result = await create_asset_holding(db, data)

    if result is None:
        raise HTTPException(
            detail="Error creating asset holding.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetHoldingResponse.model_validate(result, context=state.settings)


@put("/{holding_id:int}", summary="Update Asset Holding", status_code=HTTP_200_OK)
async def edit(
    holding_id: int,
    data: Annotated[AssetHoldingUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetHoldingResponse:
    result = await update_asset_holding(db, holding_id, data)

    if result is None:
        raise HTTPException(
            detail="Error updating asset holding.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetHoldingResponse.model_validate(result, context=state.settings)


@delete(
    "/{holding_id:int}",
    summary="Delete Asset Holding",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(holding_id: int, db: AsyncSession) -> None:
    await remove_asset_holding(db, holding_id)
