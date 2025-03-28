from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.core.db import Base, Date


class NewsSource(MappedAsDataclass, Base, Date, kw_only=True):
    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]
    url: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text)
    logo_url: Mapped[str | None]
    category: Mapped[str]  # e.g., "markets", "personal finance", "cryptocurrency"

    subscriptions: Mapped[list["NewsletterSubscription"]] = relationship(
        "NewsletterSubscription",
        back_populates="news_source",
        cascade="all, delete-orphan",
    )


class NewsletterSubscription(MappedAsDataclass, Base, Date, kw_only=True):
    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    news_source_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("news_sources.id", ondelete="CASCADE")
    )
    email: Mapped[str]
    frequency: Mapped[str]  # e.g., "daily", "weekly", "monthly"
    last_received: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    subscription_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    subscription_cost: Mapped[Decimal | None] = mapped_column(
        BigInteger, nullable=True
    )  # Cost if it's a paid subscription

    news_source: Mapped["NewsSource"] = relationship(
        "NewsSource",
        back_populates="subscriptions",
    )
    content_preferences: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True
    )  # User preferences for content


class SavedArticle(MappedAsDataclass, Base, Date, kw_only=True):
    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    subscription_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("newsletter_subscriptions.id", ondelete="CASCADE")
    )
    title: Mapped[str]
    url: Mapped[str]
    author: Mapped[str | None]
    publish_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    summary: Mapped[str | None] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text)

    subscription: Mapped["NewsletterSubscription"] = relationship(
        "NewsletterSubscription",
        backref="saved_articles",
    )
