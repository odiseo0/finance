from decimal import Decimal
from typing import Any

from src.app.budgets.domain.repository.models import BudgetType
from src.core.schema import BaseModel


class BudgetTemplate(BaseModel):
    name: str | None = None
    description: str | None = None
    budget_type: BudgetType | None = None
    total_amount: Decimal | None = None
    duration_days: int | None = None
    categories: list[dict[str, Any]] | None = None
    is_public: bool | None = None
    usage_count: int | None = None


class BudgetTemplateCreate(BudgetTemplate):
    name: str
    budget_type: BudgetType
    categories: list[dict[str, Any]]


class BudgetTemplateUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    budget_type: BudgetType | None = None
    total_amount: Decimal | None = None
    duration_days: int | None = None
    categories: list[dict[str, Any]] | None = None
    is_public: bool | None = None
    usage_count: int | None = None


class BudgetTemplateResponse(BudgetTemplate):
    id: int
