from datetime import datetime
from decimal import Decimal
from typing import Any

from src.app.investments.domain.repository.models import InvestmentGoal
from src.core.schema import BaseModel


class Investment(BaseModel):
    user_id: str | None = None
    asset_id: int | None = None
    nickname: str | None = None
    target_allocation: Decimal | None = None
    notes: str | None = None
    investment_goal: InvestmentGoal | None = None
    target_date: datetime | None = None
    total_units: Decimal | None = None
    average_buy_price: Decimal | None = None
    acquisition_date: datetime | None = None
    current_value: Decimal | None = None
    return_percentage: Decimal | None = None
    annualized_return: Decimal | None = None
    enable_live_updates: bool | None = None
    price_alert_high: Decimal | None = None
    price_alert_low: Decimal | None = None
    educational_notes: str | None = None
    has_disclaimer_accepted: bool | None = None


class InvestmentCreate(Investment):
    asset_id: int
    total_units: Decimal


class InvestmentUpdate(BaseModel):
    user_id: str | None = None
    nickname: str | None = None
    target_allocation: Decimal | None = None
    notes: str | None = None
    investment_goal: InvestmentGoal | None = None
    target_date: datetime | None = None
    total_units: Decimal | None = None
    average_buy_price: Decimal | None = None
    acquisition_date: datetime | None = None
    current_value: Decimal | None = None
    return_percentage: Decimal | None = None
    annualized_return: Decimal | None = None
    enable_live_updates: bool | None = None
    price_alert_high: Decimal | None = None
    price_alert_low: Decimal | None = None
    educational_notes: str | None = None
    has_disclaimer_accepted: bool | None = None


class InvestmentResponse(Investment):
    id: int
    asset: Any | None = None
