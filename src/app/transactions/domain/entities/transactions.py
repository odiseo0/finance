from datetime import datetime
from decimal import Decimal
from typing import Any

from src.core.schema import BaseModel

from .files import TransactionFileResponse


class Transaction(BaseModel):
    transaction_type_id: int | None = None
    currency: dict[str, Any] | None = None
    value: Decimal | None = None
    value_in_usd: Decimal | None = None
    concept: str | None = None
    note: str | None = None
    payment_reference: str | None = None
    transaction_date: datetime | None = None


class TransactionCreate(Transaction):
    value: Decimal


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""


class TransactionResponse(Transaction):
    id: int
    files: list[TransactionFileResponse] | None = None
