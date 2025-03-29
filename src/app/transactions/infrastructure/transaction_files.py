from math import ceil
from typing import Annotated, Any

from litestar import Response, delete, get, post, put
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body, Parameter
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.transactions.application import (
    create_file,
    get_transaction_files,
    remove_file,
    update_file,
)
from src.app.transactions.domain import TransactionFileResponse, TransactionFileUpdate


@get(
    "/files/{transaction_id:int}",
    summary="Get multiple operation files",
    status_code=HTTP_200_OK,
)
async def read_multi(
    transaction_id: int,
    db: AsyncSession,
    page: Annotated[int, Parameter(default=1, gt=0, query="page")],
    shows: Annotated[int, Parameter(default=20, ge=10, query="shows")],
) -> list[Any]:
    data = await get_transaction_files(db, transaction_id, page, shows)
    return TransactionFileResponse.model_validate(
        {"data": data.ok_value[0], "pages": ceil(data.ok_value[1] / shows)}
    )


@post(
    "/files/{transaction_id:int}",
    summary="Create TransactionFile",
    status_code=HTTP_201_CREATED,
)
async def add(
    transaction_id: int,
    data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
    db: AsyncSession,
) -> TransactionFileResponse:
    result = await create_file(db, data, transaction_id)

    if result.is_err():
        raise HTTPException(
            detail="An error has ocurred",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    file = result.ok_value

    return TransactionFileResponse.model_validate(file)


@put("/files/{file_id:int}", summary="Update TransactionFile", status_code=HTTP_200_OK)
async def edit(
    file_id: int,
    data: Annotated[TransactionFileUpdate, Body()],
    db: AsyncSession,
) -> TransactionFileResponse:
    result = await update_file(db, file_id, data)

    if result.is_err():
        raise HTTPException(
            detail="Not found", status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

    return result


@delete(
    "/files/{file_id:int}",
    summary="Delete TransactionFile",
    status_code=HTTP_204_NO_CONTENT,
)
async def eliminate(file_id: int, db: AsyncSession) -> None:
    await remove_file(db, file_id)

    return Response(None, status_code=HTTP_204_NO_CONTENT)
