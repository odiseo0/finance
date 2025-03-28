from datetime import datetime
from decimal import Decimal

from src.core.schema import BaseModel


class GoalContribution(BaseModel):
    goal_id: int | None = None
    amount: Decimal | None = None
    currency: str | None = None
    contribution_date: datetime | None = None
    is_automatic: bool | None = None
    is_initial_deposit: bool | None = None
    transaction_id: int | None = None
    notes: str | None = None


class GoalContributionCreate(GoalContribution):
    goal_id: int
    amount: Decimal
    contribution_date: datetime
    currency: str = "USD"


class GoalContributionUpdate(BaseModel):
    amount: Decimal | None = None
    currency: str | None = None
    contribution_date: datetime | None = None
    is_automatic: bool | None = None
    is_initial_deposit: bool | None = None
    transaction_id: int | None = None
    notes: str | None = None


class GoalContributionResponse(GoalContribution):
    id: int
