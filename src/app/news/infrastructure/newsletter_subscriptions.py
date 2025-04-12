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
    create_newsletter_subscription,
    get_newsletter_subscription,
    get_newsletter_subscriptions,
    remove_newsletter_subscription,
    update_newsletter_subscription,
)
from src.app.news.domain.entities.newsletter_subscriptions import (
    NewsletterSubscriptionCreate,
    NewsletterSubscriptionResponse,
    NewsletterSubscriptionUpdate,
)


@get(
    "/subscriptions/{subscription_id:int}",
    summary="Get one Newsletter Subscription",
    status_code=HTTP_200_OK,
)
async def read(
    subscription_id: int, db: AsyncSession, state: ImmutableState
) -> NewsletterSubscriptionResponse:
    data = await get_newsletter_subscription(db, subscription_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return NewsletterSubscriptionResponse.model_validate(
        data.ok_value, context=state.settings
    )


@get("/subscriptions/", summary="Get newsletter subscriptions", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    news_source_id: Annotated[
        int | None, Parameter(query="newsSourceId", default=None, required=False)
    ],
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    state: ImmutableState,
) -> list[NewsletterSubscriptionResponse]:
    filters = {}

    if news_source_id:
        filters["news_source_id"] = news_source_id

    data = await get_newsletter_subscriptions(
        db, page=page, shows=shows, filters=filters
    )

    if data.is_err():
        raise HTTPException(
            detail="Error retrieving newsletter subscriptions.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return [
        NewsletterSubscriptionResponse.model_validate(item, context=state.settings)
        for item in data.ok_value
    ]


@post(
    "/subscriptions/",
    summary="Create Newsletter Subscription",
    status_code=HTTP_201_CREATED,
)
async def add(
    data: Annotated[NewsletterSubscriptionCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> NewsletterSubscriptionResponse:
    result = await create_newsletter_subscription(db, data)

    if result.is_err():
        raise HTTPException(
            detail="Error creating newsletter subscription.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return NewsletterSubscriptionResponse.model_validate(
        result.ok_value, context=state.settings
    )


@put(
    "/subscriptions/{subscription_id:int}",
    summary="Update Newsletter Subscription",
    status_code=HTTP_200_OK,
)
async def edit(
    subscription_id: int,
    data: Annotated[NewsletterSubscriptionUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> NewsletterSubscriptionResponse:
    result = await update_newsletter_subscription(db, subscription_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Error updating newsletter subscription.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return NewsletterSubscriptionResponse.model_validate(
        result.ok_value, context=state.settings
    )


@delete(
    "/subscriptions/{subscription_id:int}",
    summary="Delete Newsletter Subscription",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(subscription_id: int, db: AsyncSession) -> None:
    result = await remove_newsletter_subscription(db, subscription_id)

    if result.is_err():
        raise HTTPException(
            detail="Error deleting newsletter subscription.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
