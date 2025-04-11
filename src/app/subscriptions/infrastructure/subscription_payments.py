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
    create_subscription_payment,
    get_subscription_payment,
    get_subscription_payments,
    remove_subscription_payment,
    update_subscription_payment,
)
from src.app.subscriptions.domain import (
    SubscriptionPaymentCreate,
    SubscriptionPaymentResponse,
    SubscriptionPaymentUpdate,
)


@get(
    "/payments/{payment_id:int}",
    summary="Get one Subscription Payment",
    status_code=HTTP_200_OK,
)
async def read(
    payment_id: int, db: AsyncSession, state: ImmutableState
) -> SubscriptionPaymentResponse:
    data = await get_subscription_payment(db, payment_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return SubscriptionPaymentResponse.model_validate(
        data.ok_value, context=state.settings
    )


@get("/payments/", summary="Get subscription payments", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    subscription_id: Annotated[
        int | None, Parameter(query="subscriptionId", default=None, required=False)
    ],
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    state: ImmutableState,
) -> list[SubscriptionPaymentResponse]:
    data = await get_subscription_payments(
        db, subscription_id=subscription_id, page=page, shows=shows
    )

    if data.is_err():
        raise HTTPException(
            detail="Error retrieving subscription payments.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return [
        SubscriptionPaymentResponse.model_validate(item, context=state.settings)
        for item in data.ok_value
    ]


@post("/payments/", summary="Create Subscription Payment", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[SubscriptionPaymentCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SubscriptionPaymentResponse:
    result = await create_subscription_payment(db, data)

    if result.is_err():
        raise HTTPException(
            detail="Error creating subscription payment.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SubscriptionPaymentResponse.model_validate(
        result.ok_value, context=state.settings
    )


@put(
    "/payments/{payment_id:int}",
    summary="Update Subscription Payment",
    status_code=HTTP_200_OK,
)
async def edit(
    payment_id: int,
    data: Annotated[SubscriptionPaymentUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> SubscriptionPaymentResponse:
    result = await update_subscription_payment(db, payment_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Error updating subscription payment.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return SubscriptionPaymentResponse.model_validate(
        result.ok_value, context=state.settings
    )


@delete(
    "/payments/{payment_id:int}",
    summary="Delete Subscription Payment",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(payment_id: int, db: AsyncSession) -> None:
    result = await remove_subscription_payment(db, payment_id)

    if result.is_err():
        raise HTTPException(
            detail="Error deleting subscription payment.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
