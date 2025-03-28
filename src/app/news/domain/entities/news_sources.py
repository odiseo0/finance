from typing import TYPE_CHECKING, List

from src.core.schema import BaseModel


if TYPE_CHECKING:
    from src.app.news.domain.entities.newsletter_subscriptions import (
        NewsletterSubscriptionResponse,
    )


class NewsSource(BaseModel):
    name: str | None = None
    url: str | None = None
    description: str | None = None
    logo_url: str | None = None
    category: str | None = None


class NewsSourceCreate(NewsSource):
    name: str
    url: str
    category: str


class NewsSourceUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    description: str | None = None
    logo_url: str | None = None
    category: str | None = None


class NewsSourceResponse(NewsSource):
    id: int
    subscriptions: List["NewsletterSubscriptionResponse"] | None = None
