from datetime import datetime
from decimal import Decimal
from enum import Enum

from src.core.schema import BaseModel


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    INTEREST = "interest"
    FEE = "fee"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    SPLIT = "split"
    OTHER = "other"


class Transaction(BaseModel):
    user_id: str | None = None
    investment_id: int | None = None
    transaction_type: TransactionType | None = None
    date: datetime | None = None
    units: Decimal | None = None
    price_per_unit: Decimal | None = None
    total_amount: Decimal | None = None
    fees: Decimal | None = None
    taxes: Decimal | None = None
    currency: str | None = None
    notes: str | None = None
    broker: str | None = None
    exchange: str | None = None
    settlement_date: datetime | None = None
    confirmation_number: str | None = None


class TransactionCreate(Transaction):
    investment_id: int
    transaction_type: TransactionType
    date: datetime
    units: Decimal
    total_amount: Decimal


class TransactionUpdate(BaseModel):
    transaction_type: TransactionType | None = None
    date: datetime | None = None
    units: Decimal | None = None
    price_per_unit: Decimal | None = None
    total_amount: Decimal | None = None
    fees: Decimal | None = None
    taxes: Decimal | None = None
    currency: str | None = None
    notes: str | None = None
    broker: str | None = None
    exchange: str | None = None
    settlement_date: datetime | None = None
    confirmation_number: str | None = None


class TransactionResponse(Transaction):
    id: int
    investment: dict | None = None
