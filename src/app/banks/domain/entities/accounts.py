from datetime import date, datetime
from decimal import Decimal
from typing import Any

from src.core.schema import BaseModel


class Account(BaseModel):
    institution_id: int | None = None
    name: str | None = None
    account_number_masked: str | None = None
    current_balance: Decimal | None = None
    available_balance: Decimal | None = None
    last_updated: datetime | None = None
    opened_date: date | None = None
    closed_date: date | None = None
    interest_rate: Decimal | None = None
    credit_limit: Decimal | None = None
    payment_due_date: date | None = None
    minimum_payment: Decimal | None = None
    last_sync_attempt: datetime | None = None
    exclude_from_net_worth: bool | None = None
    notes: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class AccountCreate(Account):
    institution_id: int
    name: str
    current_balance: Decimal
    last_updated: datetime = datetime.now()


class AccountUpdate(BaseModel):
    name: str | None = None
    account_number_masked: str | None = None
    current_balance: Decimal | None = None
    available_balance: Decimal | None = None
    last_updated: datetime | None = None
    opened_date: date | None = None
    closed_date: date | None = None
    interest_rate: Decimal | None = None
    credit_limit: Decimal | None = None
    payment_due_date: date | None = None
    minimum_payment: Decimal | None = None
    exclude_from_net_worth: bool | None = None
    notes: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class AccountResponse(Account):
    id: int
