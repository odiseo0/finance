from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from src.core.schema import BaseModel


class BillingFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    BIANNUALLY = "biannually"
    ANNUALLY = "annually"
    CUSTOM = "custom"


class SubscriptionCategory(str, Enum):
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


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    TRIAL = "trial"
    PENDING = "pending"
    EXPIRED = "expired"


class Subscription(BaseModel):
    name: str | None = None
    description: str | None = None
    category: SubscriptionCategory | None = None
    status: SubscriptionStatus | None = None
    url: str | None = None

    cost: Decimal | None = None
    billing_frequency: BillingFrequency | None = None
    custom_billing_days: int | None = None

    start_date: datetime | None = None
    next_billing_date: datetime | None = None
    end_date: datetime | None = None
    trial_end_date: datetime | None = None

    remind_before_billing: bool | None = None
    reminder_days: int | None = None

    shared_with_family: bool | None = None
    family_members_count: int | None = None

    note: str | None = None
    tags: list[str] | None = None

    account_email: str | None = None
    account_username: str | None = None
    account_details: dict[str, Any] | None = None
    has_password_manager: bool | None = None

    annual_cost: Decimal | None = None
    cost_per_use: Decimal | None = None


class SubscriptionCreate(Subscription):
    name: str
    category: SubscriptionCategory
    cost: Decimal
    billing_frequency: BillingFrequency
    start_date: datetime


class SubscriptionUpdate(BaseModel):
    pass


class SubscriptionResponse(Subscription):
    id: int
