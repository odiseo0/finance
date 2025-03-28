from datetime import date
from decimal import Decimal

from src.core.schema import BaseModel


class GoalMilestone(BaseModel):
    goal_id: int | None = None
    name: str | None = None
    description: str | None = None
    target_amount: Decimal | None = None
    target_percentage: Decimal | None = None
    target_date: date | None = None
    is_achieved: bool | None = None
    achieved_date: date | None = None
    icon: str | None = None


class GoalMilestoneCreate(GoalMilestone):
    goal_id: int
    name: str
    target_amount: Decimal
    target_percentage: Decimal


class GoalMilestoneUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    target_amount: Decimal | None = None
    target_percentage: Decimal | None = None
    target_date: date | None = None
    is_achieved: bool | None = None
    achieved_date: date | None = None
    icon: str | None = None


class GoalMilestoneResponse(GoalMilestone):
    id: int
