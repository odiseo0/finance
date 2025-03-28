from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List

from src.core.schema import BaseModel


if TYPE_CHECKING:
    from src.app.news.domain.entities.news_sources import NewsSourceResponse
    from src.app.news.domain.entities.saved_articles import SavedArticleResponse


class NewsletterSubscription(BaseModel):
    news_source_id: int | None = None
    email: str | None = None
    frequency: str | None = None
    last_received: datetime | None = None
    subscription_date: datetime | None = None
    subscription_cost: Decimal | None = None
    content_preferences: Dict[str, str | bool] | None = None


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
    content_preferences: Dict[str, str | bool] | None = None


class NewsletterSubscriptionResponse(NewsletterSubscription):
    id: int
    news_source: "NewsSourceResponse" | None = None
    saved_articles: List["SavedArticleResponse"] | None = None
