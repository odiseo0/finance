from typing import Annotated

from litestar import delete, get, post, put
from litestar.exceptions import HTTPException
from litestar.params import Body, Parameter
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.transactions.application import (
    create_transaction_type,
    get_one_transaction_type,
    get_transaction_types,
    remove_transaction_type,
    update_transaction_type,
)
from src.app.transactions.domain import (
    TransactionTypeCreate,
    TransactionTypeResponse,
    TransactionTypeUpdate,
)


@get("/types/", summary="Get transaction types", status_code=HTTP_200_OK)
async def read_multi(
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=20, ge=10, query="shows")],
) -> list[TransactionTypeResponse]:
    data = await get_transaction_types(db, page, shows, None)

    if data.is_err():
        return []

    return [TransactionTypeResponse.model_validate(obj) for obj in data.ok_value[0]]


@get(
    "/types/{transaction_type_id:int}",
    summary="Get one TransactionTypes",
    status_code=HTTP_200_OK,
)
async def read(transaction_type_id: int, db: AsyncSession) -> TransactionTypeResponse:
    data = await get_one_transaction_type(db, transaction_type_id)

    if data.is_err():
        raise HTTPException(detail="Not found.", status_code=HTTP_404_NOT_FOUND)

    return TransactionTypeResponse.model_validate(data.ok_value)


@post("/types/", summary="Create TransactionTypes", status_code=HTTP_201_CREATED)
async def add(
    data: Annotated[TransactionTypeCreate, Body()], db: AsyncSession
) -> TransactionTypeResponse:
    result = await create_transaction_type(db, data)
    return TransactionTypeResponse.model_validate(result.ok_value)


@put(
    "/types/{transaction_type_id:int}",
    summary="Update TransactionTypes",
    status_code=HTTP_200_OK,
)
async def edit(
    transaction_type_id: int,
    data: Annotated[TransactionTypeUpdate, Body()],
    db: AsyncSession,
) -> TransactionTypeResponse:
    result = await update_transaction_type(db, transaction_type_id, data)
    return TransactionTypeResponse.model_validate(result.ok_value)


@delete(
    "/types/{transaction_type_id:int}",
    summary="Delete TransactionTypes",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(transaction_type_id: int, db: AsyncSession) -> None:
    await remove_transaction_type(db, transaction_type_id)
