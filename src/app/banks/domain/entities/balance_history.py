from datetime import date
from decimal import Decimal

from src.core.schema import BaseModel


class BalanceHistory(BaseModel):
    account_id: int | None = None
    balance: Decimal | None = None
    balance_date: date | None = None
    is_eod: bool | None = True  # End of day
    is_manual: bool | None = False  # Manual entry


class BalanceHistoryCreate(BalanceHistory):
    account_id: int
    balance: Decimal
    balance_date: date


class BalanceHistoryUpdate(BaseModel):
    balance: Decimal | None = None
    balance_date: date | None = None
    is_eod: bool | None = None
    is_manual: bool | None = None


class BalanceHistoryResponse(BalanceHistory):
    id: int
