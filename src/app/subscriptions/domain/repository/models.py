import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.core.db import Base, Date


if TYPE_CHECKING:
    from src.app.transactions.domain.repository.models import Transaction


class BillingFrequency(enum.Enum):
    """Frequency at which a subscription is billed"""

    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    BIANNUALLY = "biannually"
    ANNUALLY = "annually"
    CUSTOM = "custom"  # For custom billing periods


class SubscriptionCategory(enum.Enum):
    """Categories for classifying subscriptions"""

    ENTERTAINMENT = "entertainment"
    MUSIC = "music"
    FITNESS = "fitness"
    SOFTWARE = "software"
    GAMING = "gaming"
    NEWS = "news"
    EDUCATION = "education"
    FOOD = "food"
    STORAGE = "storage"
    OTHER = "other"


class SubscriptionStatus(enum.Enum):
    """Current status of a subscription"""

    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    TRIAL = "trial"
    PENDING = "pending"
    EXPIRED = "expired"


class Subscription(MappedAsDataclass, Base, Date, kw_only=True):
    """User subscription to a service"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[SubscriptionCategory] = mapped_column(Enum(SubscriptionCategory))
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE
    )
    url: Mapped[str | None] = mapped_column(nullable=True)  # Website for the service

    cost: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=8))
    billing_frequency: Mapped[BillingFrequency] = mapped_column(Enum(BillingFrequency))
    custom_billing_days: Mapped[int | None] = mapped_column(nullable=True)

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    next_billing_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    trial_end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    remind_before_billing: Mapped[bool] = mapped_column(Boolean, default=True)
    reminder_days: Mapped[int] = mapped_column(
        Integer, default=3
    )  # Days before billing to remind

    shared_with_family: Mapped[bool] = mapped_column(Boolean, default=False)
    family_members_count: Mapped[int | None] = mapped_column(nullable=True)

    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)

    account_email: Mapped[str | None] = mapped_column(nullable=True)
    account_username: Mapped[str | None] = mapped_column(nullable=True)
    account_details: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    has_password_manager: Mapped[bool] = mapped_column(Boolean, default=False)

    annual_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    cost_per_use: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )

    billing_history: Mapped[list["SubscriptionPayment"]] = relationship(
        "SubscriptionPayment",
        back_populates="subscription",
        cascade="all, delete-orphan",
    )
    notifications: Mapped[list["SubscriptionNotification"]] = relationship(
        "SubscriptionNotification",
        back_populates="subscription",
        cascade="all, delete-orphan",
    )


class SubscriptionPayment(MappedAsDataclass, Base, Date, kw_only=True):
    """Record of payments made for subscriptions"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    subscription_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("subscriptions.id", ondelete="CASCADE")
    )
    transaction_id: Mapped[int | None] = mapped_column(nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=8))
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expected_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    price_change: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    subscription: Mapped["Subscription"] = relationship(
        "Subscription", back_populates="billing_history"
    )
    transaction: Mapped["Transaction"] = relationship(
        "src.app.transactions.domain.repository.models.Transaction",
        primaryjoin="SubscriptionPayment.transaction_id == foreign(Transaction.id)",
        viewonly=True,
        lazy="joined",
    )


class SubscriptionNotification(MappedAsDataclass, Base, Date, kw_only=True):
    """Notifications for subscriptions (billing reminders, price changes, etc.)"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    subscription_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("subscriptions.id", ondelete="CASCADE")
    )
    notification_type: Mapped[str]  # billing_reminder, price_change, trial_ending, etc.
    message: Mapped[str] = mapped_column(Text)
    notification_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    subscription: Mapped["Subscription"] = relationship(
        "Subscription", back_populates="notifications"
    )
