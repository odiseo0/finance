from datetime import datetime

from src.core.schema import BaseModel


class TransactionFile(BaseModel):
    transaction_id: int | None = None
    file: str | None = None
    note: str | None = None


class TransactionFileCreate(TransactionFile):
    transaction_id: int
    file: str


class TransactionFileUpdate(TransactionFile):
    """Update File"""


class TransactionFileResponse(TransactionFile):
    id: int
    file: str | None = None
    date_added: datetime
    date_updated: datetime | None = None


class TransactionFileLockup(BaseModel):
    data: list[TransactionFileResponse] = []
    page: int = 1
