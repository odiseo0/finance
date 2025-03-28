from datetime import date
from decimal import Decimal
from typing import Any

from src.app.goals.domain.repository.models import GoalCategory, GoalStatus
from src.core.schema import BaseModel

from .contributions import GoalContributionResponse
from .milestones import GoalMilestoneResponse


class Goal(BaseModel):
    name: str | None = None
    description: str | None = None
    category: GoalCategory | None = None
    status: GoalStatus | None = None
    target_amount: Decimal | None = None
    current_amount: Decimal | None = None
    currency: str | None = None
    initial_deposit: Decimal | None = None
    start_date: date | None = None
    target_date: date | None = None
    completion_date: date | None = None
    monthly_contribution_target: Decimal | None = None
    auto_contribution: bool | None = None
    auto_contribution_amount: Decimal | None = None
    auto_contribution_frequency: str | None = None
    priority: int | None = None
    icon: str | None = None
    color: str | None = None
    metadata: dict[str, Any] | None = None
    notes: str | None = None
    tags: list[str] | None = None


class GoalCreate(Goal):
    name: str
    category: GoalCategory
    target_amount: Decimal
    start_date: date
    currency: str = "USD"


class GoalUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: GoalCategory | None = None
    status: GoalStatus | None = None
    target_amount: Decimal | None = None
    current_amount: Decimal | None = None
    currency: str | None = None
    initial_deposit: Decimal | None = None
    start_date: date | None = None
    target_date: date | None = None
    completion_date: date | None = None
    monthly_contribution_target: Decimal | None = None
    auto_contribution: bool | None = None
    auto_contribution_amount: Decimal | None = None
    auto_contribution_frequency: str | None = None
    priority: int | None = None
    icon: str | None = None
    color: str | None = None
    metadata: dict[str, Any] | None = None
    notes: str | None = None
    tags: list[str] | None = None


class GoalResponse(Goal):
    id: int
    contributions: list[GoalContributionResponse] | None = None
    milestones: list[GoalMilestoneResponse] | None = None
