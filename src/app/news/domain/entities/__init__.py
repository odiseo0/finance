from src.app.news.domain.entities.news_sources import (
    NewsSource,
    NewsSourceCreate,
    NewsSourceResponse,
    NewsSourceUpdate,
)
from src.app.news.domain.entities.newsletter_subscriptions import (
    NewsletterSubscription,
    NewsletterSubscriptionCreate,
    NewsletterSubscriptionResponse,
    NewsletterSubscriptionUpdate,
)
from src.app.news.domain.entities.saved_articles import (
    SavedArticle,
    SavedArticleCreate,
    SavedArticleResponse,
    SavedArticleUpdate,
)


__all__ = [
    # News Sources
    "NewsSource",
    "NewsSourceCreate",
    "NewsSourceUpdate",
    "NewsSourceResponse",
    # Newsletter Subscriptions
    "NewsletterSubscription",
    "NewsletterSubscriptionCreate",
    "NewsletterSubscriptionUpdate",
    "NewsletterSubscriptionResponse",
    # Saved Articles
    "SavedArticle",
    "SavedArticleCreate",
    "SavedArticleUpdate",
    "SavedArticleResponse",
]
