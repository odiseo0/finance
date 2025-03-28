from datetime import datetime
from decimal import Decimal
from typing import Any

from src.core.schema import BaseModel


class BudgetAnalysis(BaseModel):
    budget_id: int | None = None
    completion_percentage: Decimal | None = None
    spending_percentage: Decimal | None = None
    days_elapsed_percentage: Decimal | None = None
    total_variance: Decimal | None = None
    variance_percentage: Decimal | None = None
    over_budget_categories: list[dict[str, Any]] | None = None
    under_utilized_categories: list[dict[str, Any]] | None = None
    daily_average_spend: Decimal | None = None
    spending_trend: str | None = None
    last_analyzed: datetime | None = None


class BudgetAnalysisCreate(BudgetAnalysis):
    budget_id: int
    last_analyzed: datetime = datetime.now()


class BudgetAnalysisUpdate(BaseModel):
    completion_percentage: Decimal | None = None
    spending_percentage: Decimal | None = None
    days_elapsed_percentage: Decimal | None = None
    total_variance: Decimal | None = None
    variance_percentage: Decimal | None = None
    over_budget_categories: list[dict[str, Any]] | None = None
    under_utilized_categories: list[dict[str, Any]] | None = None
    daily_average_spend: Decimal | None = None
    spending_trend: str | None = None
    last_analyzed: datetime | None = None


class BudgetAnalysisResponse(BudgetAnalysis):
    id: int
