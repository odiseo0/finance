from datetime import date
from decimal import Decimal

from src.core.schema import BaseModel


class BudgetExpense(BaseModel):
    budget_id: int | None = None
    category_id: int | None = None
    subcategory_id: int | None = None
    amount: Decimal | None = None
    currency: str | None = None
    description: str | None = None
    expense_date: date | None = None
    is_planned: bool | None = None
    is_recurring: bool | None = None
    transaction_id: int | None = None
    notes: str | None = None


class BudgetExpenseCreate(BudgetExpense):
    budget_id: int
    amount: Decimal
    expense_date: date
    currency: str = "USD"


class BudgetExpenseUpdate(BaseModel):
    category_id: int | None = None
    subcategory_id: int | None = None
    amount: Decimal | None = None
    currency: str | None = None
    description: str | None = None
    expense_date: date | None = None
    is_planned: bool | None = None
    is_recurring: bool | None = None
    transaction_id: int | None = None
    notes: str | None = None


class BudgetExpenseResponse(BudgetExpense):
    id: int
