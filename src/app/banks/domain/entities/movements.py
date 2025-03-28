from datetime import datetime
from decimal import Decimal
from typing import Any

from src.core.schema import BaseModel


class BankMovement(BaseModel):
    account_id: int | None = None
    transaction_id: int | None = None
    amount: Decimal | None = None
    date: datetime | None = None
    description: str | None = None
    running_balance: Decimal | None = None
    reference: str | None = None
    merchant_name: str | None = None
    category: str | None = None
    needs_review: bool | None = False
    raw_data: dict[str, Any] | None = None
    notes: str | None = None


class BankMovementCreate(BankMovement):
    account_id: int
    amount: Decimal
    date: datetime


class BankMovementUpdate(BaseModel):
    amount: Decimal | None = None
    date: datetime | None = None
    description: str | None = None
    running_balance: Decimal | None = None
    reference: str | None = None
    merchant_name: str | None = None
    category: str | None = None
    needs_review: bool | None = None
    raw_data: dict[str, Any] | None = None
    notes: str | None = None
    transaction_id: int | None = None


class BankMovementResponse(BankMovement):
    id: int
