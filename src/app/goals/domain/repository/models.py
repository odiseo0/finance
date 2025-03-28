import enum
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.core.db import Base
from src.core.db import Date as BaseDate


if TYPE_CHECKING:
    from src.app.transactions.domain.repository.models import Transaction


class GoalCategory(enum.Enum):
    """Categories for different types of financial goals"""

    VEHICLE = "vehicle"  # Car, motorcycle, bicycle
    PROPERTY = "property"  # House, apartment, land
    TRAVEL = "travel"  # Vacation, trip
    EDUCATION = "education"  # Tuition, courses, certifications
    RETIREMENT = "retirement"  # Retirement savings
    EMERGENCY_FUND = "emergency_fund"  # Emergency savings
    DEBT_PAYMENT = "debt_payment"  # Paying off loans, credit cards
    MAJOR_PURCHASE = "major_purchase"  # Electronics, furniture, appliances
    BUSINESS = "business"  # Starting or expanding a business
    GIFT = "gift"  # Saving for a gift
    OTHER = "other"  # Custom goals


class GoalStatus(enum.Enum):
    """Current status of a financial goal"""

    ACTIVE = "active"  # Currently saving
    COMPLETED = "completed"  # Goal reached
    ABANDONED = "abandoned"  # No longer pursuing
    PAUSED = "paused"  # Temporarily paused
    ADJUSTED = "adjusted"  # Goal parameters changed


class Goal(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Financial goal that a user is saving toward"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]  # Name of the goal
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Goal details
    category: Mapped[GoalCategory] = mapped_column(Enum(GoalCategory))
    status: Mapped[GoalStatus] = mapped_column(
        Enum(GoalStatus), default=GoalStatus.ACTIVE
    )

    # Financial targets
    target_amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    current_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=2), default=Decimal("0.00")
    )
    currency: Mapped[str] = mapped_column(String(3), default="USD")  # ISO currency code
    initial_deposit: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )

    # Time frames
    start_date: Mapped[date] = mapped_column(Date)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Savings strategy
    monthly_contribution_target: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    auto_contribution: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_contribution_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    auto_contribution_frequency: Mapped[str | None] = mapped_column(
        nullable=True
    )  # weekly, monthly, etc.

    # Visualization and motivation
    priority: Mapped[int] = mapped_column(Integer, default=3)  # 1=highest, 5=lowest
    icon: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Icon for UI representation
    color: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Color for UI representation

    # Goal-specific metadata
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # Notes and tags
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    contributions: Mapped[list["GoalContribution"]] = relationship(
        "GoalContribution", back_populates="goal", cascade="all, delete-orphan"
    )
    milestones: Mapped[list["GoalMilestone"]] = relationship(
        "GoalMilestone", back_populates="goal", cascade="all, delete-orphan"
    )


class GoalContribution(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Individual contribution toward a financial goal"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    goal_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("goals.id", ondelete="CASCADE")
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    contribution_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Contribution type
    is_automatic: Mapped[bool] = mapped_column(Boolean, default=False)
    is_initial_deposit: Mapped[bool] = mapped_column(Boolean, default=False)

    # Link to transactions if available
    transaction_id: Mapped[int | None] = mapped_column(nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    goal: Mapped["Goal"] = relationship("Goal", back_populates="contributions")

    # Optional relationship to transactions if they exist
    transaction: Mapped["Transaction"] = (
        relationship(
            "src.app.transactions.domain.repository.models.Transaction",
            primaryjoin="GoalContribution.transaction_id == foreign(Transaction.id)",
            viewonly=True,
            lazy="joined",
        )
        if TYPE_CHECKING
        else None
    )


class GoalMilestone(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Milestone or achievement marker for a goal"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    goal_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("goals.id", ondelete="CASCADE")
    )
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Milestone target
    target_amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    target_percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=5, scale=2)
    )  # e.g., 25.00 for 25%
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Milestone status
    is_achieved: Mapped[bool] = mapped_column(Boolean, default=False)
    achieved_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # UI/UX elements
    icon: Mapped[str | None] = mapped_column(nullable=True)

    # Relationships
    goal: Mapped["Goal"] = relationship("Goal", back_populates="milestones")


class GoalCalculation(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Calculation and projections for goal achievement"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    goal_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("goals.id", ondelete="CASCADE"), unique=True
    )

    # Progress metrics
    progress_percentage: Mapped[Decimal] = mapped_column(Numeric(precision=5, scale=2))
    amount_remaining: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))

    # Time projections
    days_remaining: Mapped[int | None] = mapped_column(nullable=True)
    estimated_completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Required savings rates
    required_monthly_contribution: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    required_weekly_contribution: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )

    # Historical performance
    average_monthly_contribution: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    contribution_frequency: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=10, scale=2), nullable=True
    )  # Average days between contributions

    # Last calculation timestamp
    last_calculated: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Goal
    goal: Mapped["Goal"] = relationship("Goal")
