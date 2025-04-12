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
    create_saved_article,
    get_saved_article,
    get_saved_articles,
    remove_saved_article,
    update_saved_article,
)
from src.app.news.domain.entities.saved_articles import (
    SavedArticleCreate,
    SavedArticleResponse,
    SavedArticleUpdate,
)


@get(
    "/articles/{article_id:int}",
    summary="Get one Saved Article",
    status_code=HTTP_200_OK,
)
async def read(
    article_id: int, db: AsyncSession, state: ImmutableState
) -> SavedArticleResponse:
    data = await get_saved_article(db, article_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return SavedArticleResponse.model_validate(data.ok_value, context=state.settings)


@get("/articles/", summary="Get saved articles", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    subscription_id: Annotated[
        int | None, Parameter(query="subscriptionId", default=None, required=False)
    ],
    is_read: Annotated[
        bool | None, Parameter(query="isRead", default=None, required=False)
    ],
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    state: ImmutableState,
) -> list[SavedArticleResponse]:
    filters = {}

    if subscription_id:
        filters["subscription_id"] = subscription_id

    if is_read is not None:
        filters["is_read"] = is_read

    data = await get_saved_articles(db, page=page, shows=shows, filters=filters)

    if data.is_err():
        raise HTTPException(
            detail="Error retrieving saved articles.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return [
        SavedArticleResponse.model_validate(item, context=state.settings)
        for item in data.ok_value
    ]


@post(
    "/articles/",
    summary="Create Saved Article",
    status_code=HTTP_201_CREATED,
)
async def add(
    data: Annotated[SavedArticleCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SavedArticleResponse:
    result = await create_saved_article(db, data)

    if result.is_err():
        raise HTTPException(
            detail="Error creating saved article.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SavedArticleResponse.model_validate(result.ok_value, context=state.settings)


@put(
    "/articles/{article_id:int}",
    summary="Update Saved Article",
    status_code=HTTP_200_OK,
)
async def edit(
    article_id: int,
    data: Annotated[SavedArticleUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SavedArticleResponse:
    result = await update_saved_article(db, article_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Error updating saved article.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SavedArticleResponse.model_validate(result.ok_value, context=state.settings)


@delete(
    "/articles/{article_id:int}",
    summary="Delete Saved Article",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(article_id: int, db: AsyncSession) -> None:
    result = await remove_saved_article(db, article_id)

    if result.is_err():
        raise HTTPException(
            detail="Error deleting saved article.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
