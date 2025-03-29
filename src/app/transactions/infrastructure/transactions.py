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

from src.app.transactions.application import (
    create_transaction,
    get_transaction,
    get_transactions,
    remove_transaction,
    update_transaction,
)
from src.app.transactions.domain import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)


@get("/{transaction_id:int}", summary="Get one Transaction", status_code=HTTP_200_OK)
async def read(
    transaction_id: int, db: AsyncSession, state: ImmutableState
) -> TransactionResponse:
    data = await get_transaction(db, transaction_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return TransactionResponse.model_validate(data.ok_value, context=state.settings)


@get("/", summary="Get transactions", status_code=HTTP_200_OK)
async def read_multi(
    operation_id: Annotated[int, Parameter(query="operationId", required=True)],
    transaction_type_id: Annotated[
        int | None, Parameter(query="transactionType", default=None, required=False)
    ],
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=200, ge=10, query="shows")],
    state: ImmutableState,
) -> list[TransactionResponse]:
    filters = {"operation_id": operation_id}

    if transaction_type_id:
        filters.update({"transaction_type_id": transaction_type_id})

    data = await get_transactions(db, page, shows, filters)

    return [
        TransactionResponse.model_validate(transaction, context=state.settings)
        for transaction in data
    ]


@post("/", summary="Create Transaction", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[TransactionCreate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> TransactionResponse:
    result = await create_transaction(db, data)

    if result.is_err():
        raise HTTPException(
            detail="An error has ocurred",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return TransactionResponse.model_validate(result.ok_value, context=state.settings)


@put("/{transaction_id:int}", summary="Update Transaction", status_code=HTTP_200_OK)
async def edit(
    transaction_id: int,
    data: Annotated[TransactionUpdate, Body()],
    db: AsyncSession,
    state: ImmutableState,
) -> TransactionResponse:

    result = await update_transaction(db, transaction_id, data)

    if result.is_err():
        raise HTTPException(
            detail="An error has ocurred",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return TransactionResponse.model_validate(result.ok_value, context=state.settings)


@delete(
    "/{transaction_id:int}",
    summary="Delete Transaction",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(transaction_id: int, db: AsyncSession) -> None:
    result = await remove_transaction(db, transaction_id)

    if result.is_err():
        raise HTTPException(
            detail="An error has ocurred",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
