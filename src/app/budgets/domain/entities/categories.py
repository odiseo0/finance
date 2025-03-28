from decimal import Decimal

from src.core.schema import BaseModel

from .subcategories import BudgetSubcategoryResponse


class BudgetCategory(BaseModel):
    budget_id: int | None = None
    name: str | None = None
    description: str | None = None
    allocated_amount: Decimal | None = None
    amount_spent: Decimal | None = None
    amount_remaining: Decimal | None = None
    is_essential: bool | None = None
    priority: int | None = None
    color: str | None = None
    icon: str | None = None


class BudgetCategoryCreate(BudgetCategory):
    budget_id: int
    name: str
    allocated_amount: Decimal


class BudgetCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    allocated_amount: Decimal | None = None
    amount_spent: Decimal | None = None
    amount_remaining: Decimal | None = None
    is_essential: bool | None = None
    priority: int | None = None
    color: str | None = None
    icon: str | None = None


class BudgetCategoryResponse(BudgetCategory):
    id: int
    subcategories: list[BudgetSubcategoryResponse] | None = None
