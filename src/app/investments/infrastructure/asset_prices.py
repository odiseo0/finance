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
    create_asset_price,
    get_asset_price,
    get_asset_prices,
    remove_asset_price,
    update_asset_price,
)
from src.app.investments.domain.entities.asset_prices import (
    AssetPriceCreate,
    AssetPriceResponse,
    AssetPriceUpdate,
)


@get("/{price_id:int}", summary="Get one Asset Price", status_code=HTTP_200_OK)
async def read(
    price_id: int, db: AsyncSession, state: ImmutableState
) -> AssetPriceResponse:
    data = await get_asset_price(db, price_id)

    if data is None:
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return AssetPriceResponse.model_validate(data, context=state.settings)


@get("/", summary="Get asset prices", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=100, ge=10, query="shows")],
    asset_id: Annotated[
        int | None, Parameter(query="asset_id", default=None, required=False)
    ],
    state: ImmutableState,
) -> list[AssetPriceResponse]:
    filters = {}

    if asset_id:
        filters["asset_id"] = asset_id

    data = await get_asset_prices(db, page=page, shows=shows, filters=filters)

    return [
        AssetPriceResponse.model_validate(item, context=state.settings) for item in data
    ]


@post("/", summary="Create Asset Price", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[AssetPriceCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetPriceResponse:
    result = await create_asset_price(db, data)

    if result is None:
        raise HTTPException(
            detail="Error creating asset price.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetPriceResponse.model_validate(result, context=state.settings)


@put("/{price_id:int}", summary="Update Asset Price", status_code=HTTP_200_OK)
async def edit(
    price_id: int,
    data: Annotated[AssetPriceUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> AssetPriceResponse:
    result = await update_asset_price(db, price_id, data)

    if result is None:
        raise HTTPException(
            detail="Error updating asset price.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AssetPriceResponse.model_validate(result, context=state.settings)


@delete(
    "/{price_id:int}",
    summary="Delete Asset Price",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(price_id: int, db: AsyncSession) -> None:
    await remove_asset_price(db, price_id)
