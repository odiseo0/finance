from datetime import datetime
from decimal import Decimal

from src.core.schema import BaseModel


class NewsletterSubscription(BaseModel):
    news_source_id: int | None = None
    email: str | None = None
    frequency: str | None = None
    last_received: datetime | None = None
    subscription_date: datetime | None = None
    subscription_cost: Decimal | None = None
    content_preferences: dict[str, str | bool] | None = None


class NewsletterSubscriptionCreate(NewsletterSubscription):
    news_source_id: int
    email: str
    frequency: str
    subscription_date: datetime


class NewsletterSubscriptionUpdate(BaseModel):
    email: str | None = None
    frequency: str | None = None
    last_received: datetime | None = None
    subscription_cost: Decimal | None = None
    content_preferences: dict[str, str | bool] | None = None


class NewsletterSubscriptionResponse(NewsletterSubscription):
    id: int
