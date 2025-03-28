from datetime import datetime
from typing import TYPE_CHECKING

from src.core.schema import BaseModel


if TYPE_CHECKING:
    from src.app.news.domain.entities.newsletter_subscriptions import (
        NewsletterSubscriptionResponse,
    )


class SavedArticle(BaseModel):
    subscription_id: int | None = None
    title: str | None = None
    url: str | None = None
    author: str | None = None
    publish_date: datetime | None = None
    summary: str | None = None
    is_read: bool | None = None
    notes: str | None = None


class SavedArticleCreate(SavedArticle):
    subscription_id: int
    title: str
    url: str


class SavedArticleUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    author: str | None = None
    publish_date: datetime | None = None
    summary: str | None = None
    is_read: bool | None = None
    notes: str | None = None


class SavedArticleResponse(SavedArticle):
    id: int
    subscription: "NewsletterSubscriptionResponse" | None = None
