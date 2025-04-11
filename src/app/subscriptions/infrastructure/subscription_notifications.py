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
    create_subscription_notification,
    get_subscription_notification,
    get_subscription_notifications,
    remove_subscription_notification,
    update_subscription_notification,
)
from src.app.subscriptions.domain import (
    SubscriptionNotificationCreate,
    SubscriptionNotificationResponse,
    SubscriptionNotificationUpdate,
)


@get(
    "/notifications/{notification_id:int}",
    summary="Get one Subscription Notification",
    status_code=HTTP_200_OK,
)
async def read(
    notification_id: int, db: AsyncSession, state: ImmutableState
) -> SubscriptionNotificationResponse:
    data = await get_subscription_notification(db, notification_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return SubscriptionNotificationResponse.model_validate(
        data.ok_value, context=state.settings
    )


@get(
    "/notifications/", summary="Get subscription notifications", status_code=HTTP_200_OK
)
async def read_multi(
    db: AsyncSession,
    subscription_id: Annotated[
        int | None, Parameter(query="subscriptionId", default=None, required=False)
    ],
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    state: ImmutableState,
) -> list[SubscriptionNotificationResponse]:
    data = await get_subscription_notifications(
        db, subscription_id=subscription_id, page=page, shows=shows
    )

    if data.is_err():
        raise HTTPException(
            detail="Error retrieving subscription notifications.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return [
        SubscriptionNotificationResponse.model_validate(item, context=state.settings)
        for item in data.ok_value
    ]


@post(
    "/notifications/",
    summary="Create Subscription Notification",
    status_code=HTTP_201_CREATED,
)
async def add(
    data: Annotated[SubscriptionNotificationCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SubscriptionNotificationResponse:
    result = await create_subscription_notification(db, data)

    if result.is_err():
        raise HTTPException(
            detail="Error creating subscription notification.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SubscriptionNotificationResponse.model_validate(
        result.ok_value, context=state.settings
    )


@put(
    "/notifications/{notification_id:int}",
    summary="Update Subscription Notification",
    status_code=HTTP_200_OK,
)
async def edit(
    notification_id: int,
    data: Annotated[SubscriptionNotificationUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SubscriptionNotificationResponse:
    result = await update_subscription_notification(db, notification_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Error updating subscription notification.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SubscriptionNotificationResponse.model_validate(
        result.ok_value, context=state.settings
    )


@delete(
    "/notifications/{notification_id:int}",
    summary="Delete Subscription Notification",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(notification_id: int, db: AsyncSession) -> None:
    result = await remove_subscription_notification(db, notification_id)

    if result.is_err():
        raise HTTPException(
            detail="Error deleting subscription notification.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
