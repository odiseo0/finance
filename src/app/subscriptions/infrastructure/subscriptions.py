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

from src.app.subscriptions.application import (
    create_subscription,
    get_subscription,
    get_subscriptions,
    remove_subscription,
    update_subscription,
)
from src.app.subscriptions.domain import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)


@get("/{subscription_id:int}", summary="Get one Subscription", status_code=HTTP_200_OK)
async def read(
    subscription_id: int, db: AsyncSession, state: ImmutableState
) -> SubscriptionResponse:
    data = await get_subscription(db, subscription_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return SubscriptionResponse.model_validate(data.ok_value, context=state.settings)


@get("/", summary="Get subscriptions", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    category: Annotated[
        str | None, Parameter(query="category", default=None, required=False)
    ],
    is_active: Annotated[
        bool | None, Parameter(query="isActive", default=None, required=False)
    ],
    state: ImmutableState,
) -> list[SubscriptionResponse]:
    filters = {}

    if category:
        filters["category"] = category

    if is_active is not None:
        filters["is_active"] = is_active

    data = await get_subscriptions(db, page=page, shows=shows, filters=filters)

    if data.is_err():
        raise HTTPException(
            detail="Error retrieving subscriptions.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return [
        SubscriptionResponse.model_validate(item, context=state.settings)
        for item in data.ok_value
    ]


@post("/", summary="Create Subscription", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[SubscriptionCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SubscriptionResponse:
    result = await create_subscription(db, data)

    if result.is_err():
        raise HTTPException(
            detail="Error creating subscription.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SubscriptionResponse.model_validate(result.ok_value, context=state.settings)


@put("/{subscription_id:int}", summary="Update Subscription", status_code=HTTP_200_OK)
async def edit(
    subscription_id: int,
    data: Annotated[SubscriptionUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SubscriptionResponse:
    result = await update_subscription(db, subscription_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Error updating subscription.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SubscriptionResponse.model_validate(result.ok_value, context=state.settings)


@delete(
    "/{subscription_id:int}",
    summary="Delete Subscription",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(subscription_id: int, db: AsyncSession) -> None:
    result = await remove_subscription(db, subscription_id)

    if result.is_err():
        raise HTTPException(
            detail="Error deleting subscription.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
