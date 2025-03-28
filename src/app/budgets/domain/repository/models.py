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
    pass


class BudgetType(enum.Enum):
    """Types of budgets for different planning purposes"""

    MONTHLY = "monthly"  # Regular monthly budget
    ANNUAL = "annual"  # Yearly budget
    PROJECT = "project"  # One-time project budget
    EVENT = "event"  # Special event budget (wedding, vacation)
    CATEGORY = "category"  # Budget for specific category
    CUSTOM = "custom"  # Custom time period budget


class BudgetStatus(enum.Enum):
    """Current status of a budget"""

    ACTIVE = "active"  # Currently in use
    COMPLETED = "completed"  # Finished budget period
    DRAFT = "draft"  # In planning stage
    ARCHIVED = "archived"  # No longer in use but kept for records
    EXCEEDED = "exceeded"  # Budget limit exceeded


class BudgetRecurrence(enum.Enum):
    """Recurrence pattern for repeating budgets"""

    NONE = "none"  # One-time budget
    DAILY = "daily"  # Daily recurring budget
    WEEKLY = "weekly"  # Weekly recurring budget
    BIWEEKLY = "biweekly"  # Every two weeks
    MONTHLY = "monthly"  # Monthly recurring budget
    QUARTERLY = "quarterly"  # Quarterly recurring budget
    ANNUALLY = "annually"  # Yearly recurring budget


class Budget(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Budget for planning and tracking expenses"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]  # Name of the budget
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Budget details
    budget_type: Mapped[BudgetType] = mapped_column(Enum(BudgetType))
    status: Mapped[BudgetStatus] = mapped_column(
        Enum(BudgetStatus), default=BudgetStatus.ACTIVE
    )

    # Financial limits
    total_amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    amount_spent: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=2), default=Decimal("0.00")
    )
    amount_remaining: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=2), server_default="0.00"
    )
    currency: Mapped[str] = mapped_column(String(3), default="USD")  # ISO currency code

    # Time frames
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Recurrence settings
    recurrence: Mapped[BudgetRecurrence] = mapped_column(
        Enum(BudgetRecurrence), default=BudgetRecurrence.NONE
    )
    recurrence_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Alerts and notifications
    notify_on_threshold: Mapped[bool] = mapped_column(Boolean, default=False)
    threshold_percentage: Mapped[int | None] = mapped_column(
        nullable=True
    )  # e.g., 80 for 80%

    # Visualization
    color: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Color for UI representation
    icon: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Icon for UI representation

    # Budget-specific metadata
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # Notes and tags
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    categories: Mapped[list["BudgetCategory"]] = relationship(
        "BudgetCategory", back_populates="budget", cascade="all, delete-orphan"
    )
    expenses: Mapped[list["BudgetExpense"]] = relationship(
        "BudgetExpense", back_populates="budget", cascade="all, delete-orphan"
    )

    # If this budget is a recurring child
    parent_budget_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("budgets.id", ondelete="SET NULL"), nullable=True
    )

    # Child budgets from recurrence
    child_budgets: Mapped[list["Budget"]] = relationship(
        "Budget",
        foreign_keys=[parent_budget_id],
        backref=relationship.backref("parent_budget", remote_side=[id]),
    )


class BudgetCategory(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Category within a budget with its own allocation"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    budget_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("budgets.id", ondelete="CASCADE")
    )
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Category allocation
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    amount_spent: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=2), default=Decimal("0.00")
    )
    amount_remaining: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=2), server_default="0.00"
    )

    # Category details
    is_essential: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # Is this category essential/required
    priority: Mapped[int] = mapped_column(Integer, default=3)  # 1=highest, 5=lowest

    # Visualization
    color: Mapped[str | None] = mapped_column(nullable=True)
    icon: Mapped[str | None] = mapped_column(nullable=True)

    # Relationships
    budget: Mapped["Budget"] = relationship("Budget", back_populates="categories")
    expenses: Mapped[list["BudgetExpense"]] = relationship(
        "BudgetExpense", back_populates="category", cascade="all, delete-orphan"
    )


class BudgetExpense(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Individual expense tracked against a budget"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    budget_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("budgets.id", ondelete="CASCADE")
    )
    category_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("budget_categories.id"), nullable=True
    )

    # Expense details
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    expense_date: Mapped[date] = mapped_column(Date)

    # Classification
    is_planned: Mapped[bool] = mapped_column(
        Boolean, default=True
    )  # Was this planned in the budget
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)

    # Notes
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    budget: Mapped["Budget"] = relationship("Budget", back_populates="expenses")
    category: Mapped["BudgetCategory"] = relationship(
        "BudgetCategory", back_populates="expenses"
    )


class BudgetTemplate(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Reusable budget template for quick budget creation"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    budget_type: Mapped[BudgetType] = mapped_column(Enum(BudgetType))

    # Template structure
    total_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    duration_days: Mapped[int | None] = mapped_column(nullable=True)

    # Template content
    categories: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB
    )  # Category definitions with allocations

    # Sharing
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    # Usage stats
    usage_count: Mapped[int] = mapped_column(Integer, default=0)


class BudgetAnalysis(MappedAsDataclass, Base, BaseDate, kw_only=True):
    """Analysis and statistics about budget performance"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    budget_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("budgets.id", ondelete="CASCADE"), unique=True
    )

    # Progress metrics
    completion_percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=5, scale=2)
    )
    spending_percentage: Mapped[Decimal] = mapped_column(Numeric(precision=5, scale=2))
    days_elapsed_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=5, scale=2), nullable=True
    )

    # Variance analysis
    total_variance: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=2)
    )  # Positive = under budget
    variance_percentage: Mapped[Decimal] = mapped_column(Numeric(precision=5, scale=2))

    # Category analysis
    over_budget_categories: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB, nullable=True
    )
    under_utilized_categories: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB, nullable=True
    )

    # Time analysis
    daily_average_spend: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    spending_trend: Mapped[str | None] = mapped_column(
        nullable=True
    )  # increasing, decreasing, stable

    # Last analysis timestamp
    last_analyzed: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Budget relationship
    budget: Mapped["Budget"] = relationship("Budget")
