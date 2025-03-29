from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import RequestError

from src.app.transactions.domain import TransactionFileCreate, dao_transaction_files
from src.core.aws import s3_client
from src.core.utils import randomized_name


if TYPE_CHECKING:
    from litestar.datastructures import UploadFile
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.app.transactions.domain import TransactionFile, TransactionFileUpdate


async def get_transaction_files(
    db: AsyncSession,
    transaction_id: int,
    page: int = 1,
    shows: int = 100,
) -> list[TransactionFile]:
    data = await dao_transaction_files.get_multi(
        db,
        where={"transaction_id": transaction_id},
        page=(page - 1) * shows,
        shows=shows,
    )

    return data


async def upload_file(file: UploadFile, transaction_id: int) -> str:
    ext = file.filename.split(".")[-1]
    name = randomized_name()

    try:
        await s3_client.upload(
            f"transactions/{transaction_id}/{name}.{ext}",
            await file.read(),
            content_type=file.content_type,
            acl="public-read",
        )
    except RequestError:
        raise

    return f"{name}.{ext}"


async def create_file(
    db: AsyncSession, file: UploadFile, transaction_id: int
) -> TransactionFile:
    filename = await upload_file(file, transaction_id)
    obj_in = TransactionFileCreate(
        transaction_id=transaction_id,
        file=f"transactions/{transaction_id}/{filename}",
    )
    result = await dao_transaction_files.create(db, obj_in=obj_in)

    return result


async def create_many_files(
    db: AsyncSession, transaction_id: int, names: list[str]
) -> list[TransactionFile]:
    objs = [
        TransactionFileCreate(
            transaction_id=transaction_id, file=f"transactions/{transaction_id}/{name}"
        )
        for name in names
    ]

    result = await dao_transaction_files.create_many(db, objs_in=objs)

    return result


async def update_file(
    db: AsyncSession,
    file_id: int,
    obj_in: TransactionFileUpdate,
) -> TransactionFile:
    result = await dao_transaction_files.update(db, db_obj_id=file_id, obj_in=obj_in)

    return result


async def remove_file(db: AsyncSession, file_id: int) -> None:
    file = await dao_transaction_files.get(db, file_id)
    await dao_transaction_files.delete(db, file)

    try:
        await s3_client.delete(file.file)
    except RequestError:
        raise
