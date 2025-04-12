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

from src.app.news.application import (
    create_news_source,
    get_news_source,
    get_news_sources,
    remove_news_source,
    update_news_source,
)
from src.app.news.domain.entities.news_sources import (
    NewsSourceCreate,
    NewsSourceResponse,
    NewsSourceUpdate,
)


@get("/{news_source_id:int}", summary="Get one News Source", status_code=HTTP_200_OK)
async def read(
    news_source_id: int, db: AsyncSession, state: ImmutableState
) -> NewsSourceResponse:
    data = await get_news_source(db, news_source_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return NewsSourceResponse.model_validate(data.ok_value, context=state.settings)


@get("/", summary="Get news sources", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    category: Annotated[
        str | None, Parameter(query="category", default=None, required=False)
    ],
    state: ImmutableState,
) -> list[NewsSourceResponse]:
    filters = {}

    if category:
        filters["category"] = category

    data = await get_news_sources(db, page=page, shows=shows, filters=filters)

    if data.is_err():
        raise HTTPException(
            detail="Error retrieving news sources.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return [
        NewsSourceResponse.model_validate(item, context=state.settings)
        for item in data.ok_value
    ]


@post("/", summary="Create News Source", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[NewsSourceCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> NewsSourceResponse:
    result = await create_news_source(db, data)

    if result.is_err():
        raise HTTPException(
            detail="Error creating news source.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return NewsSourceResponse.model_validate(result.ok_value, context=state.settings)


@put("/{news_source_id:int}", summary="Update News Source", status_code=HTTP_200_OK)
async def edit(
    news_source_id: int,
    data: Annotated[NewsSourceUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> NewsSourceResponse:
    result = await update_news_source(db, news_source_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Error updating news source.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return NewsSourceResponse.model_validate(result.ok_value, context=state.settings)


@delete(
    "/{news_source_id:int}",
    summary="Delete News Source",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(news_source_id: int, db: AsyncSession) -> None:
    result = await remove_news_source(db, news_source_id)

    if result.is_err():
        raise HTTPException(
            detail="Error deleting news source.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
