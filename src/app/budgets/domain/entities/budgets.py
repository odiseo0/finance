from datetime import date
from decimal import Decimal
from typing import Any

from src.app.budgets.domain.repository.models import (
    BudgetRecurrence,
    BudgetStatus,
    BudgetType,
    PrivacyLevel,
)
from src.core.schema import BaseModel

from .categories import BudgetCategoryResponse
from .expenses import BudgetExpenseResponse


class Budget(BaseModel):
    name: str | None = None
    description: str | None = None
    budget_type: BudgetType | None = None
    status: BudgetStatus | None = None
    total_amount: Decimal | None = None
    amount_spent: Decimal | None = None
    amount_remaining: Decimal | None = None
    currency: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    recurrence: BudgetRecurrence | None = None
    recurrence_end_date: date | None = None
    notify_on_threshold: bool | None = None
    threshold_percentage: int | None = None
    color: str | None = None
    icon: str | None = None
    privacy_level: PrivacyLevel | None = None
    metadata: dict[str, Any] | None = None
    notes: str | None = None
    tags: list[str] | None = None
    parent_budget_id: int | None = None


class BudgetCreate(Budget):
    name: str
    budget_type: BudgetType
    total_amount: Decimal
    start_date: date
    currency: str = "USD"


class BudgetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    budget_type: BudgetType | None = None
    status: BudgetStatus | None = None
    total_amount: Decimal | None = None
    amount_spent: Decimal | None = None
    amount_remaining: Decimal | None = None
    currency: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    recurrence: BudgetRecurrence | None = None
    recurrence_end_date: date | None = None
    notify_on_threshold: bool | None = None
    threshold_percentage: int | None = None
    color: str | None = None
    icon: str | None = None
    privacy_level: PrivacyLevel | None = None
    metadata: dict[str, Any] | None = None
    notes: str | None = None
    tags: list[str] | None = None


class BudgetResponse(Budget):
    id: int
    categories: list[BudgetCategoryResponse] | None = None
    expenses: list[BudgetExpenseResponse] | None = None
