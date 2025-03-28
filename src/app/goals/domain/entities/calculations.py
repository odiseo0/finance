from datetime import date, datetime
from decimal import Decimal

from src.core.schema import BaseModel


class GoalCalculation(BaseModel):
    goal_id: int | None = None
    progress_percentage: Decimal | None = None
    amount_remaining: Decimal | None = None
    days_remaining: int | None = None
    estimated_completion_date: date | None = None
    required_monthly_contribution: Decimal | None = None
    required_weekly_contribution: Decimal | None = None
    average_monthly_contribution: Decimal | None = None
    contribution_frequency: Decimal | None = None
    last_calculated: datetime | None = None


class GoalCalculationCreate(GoalCalculation):
    goal_id: int
    progress_percentage: Decimal
    amount_remaining: Decimal
    last_calculated: datetime = datetime.now()


class GoalCalculationUpdate(BaseModel):
    progress_percentage: Decimal | None = None
    amount_remaining: Decimal | None = None
    days_remaining: int | None = None
    estimated_completion_date: date | None = None
    required_monthly_contribution: Decimal | None = None
    required_weekly_contribution: Decimal | None = None
    average_monthly_contribution: Decimal | None = None
    contribution_frequency: Decimal | None = None
    last_calculated: datetime | None = None


class GoalCalculationResponse(GoalCalculation):
    id: int
