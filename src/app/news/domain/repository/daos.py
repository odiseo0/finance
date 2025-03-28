from src.app.news.domain.entities import (
    NewsletterSubscriptionCreate,
    NewsletterSubscriptionUpdate,
    NewsSourceCreate,
    NewsSourceUpdate,
    SavedArticleCreate,
    SavedArticleUpdate,
)
from src.core.db import DAO

from .models import NewsletterSubscription, NewsSource, SavedArticle


class DAONewsSource(DAO[NewsSource, NewsSourceCreate, NewsSourceUpdate]):
    pass


class DAONewsletterSubscription(
    DAO[
        NewsletterSubscription,
        NewsletterSubscriptionCreate,
        NewsletterSubscriptionUpdate,
    ]
):
    pass


class DAOSavedArticle(DAO[SavedArticle, SavedArticleCreate, SavedArticleUpdate]):
    pass


dao_news_sources = DAONewsSource(NewsSource)
dao_newsletter_subscriptions = DAONewsletterSubscription(NewsletterSubscription)
dao_saved_articles = DAOSavedArticle(SavedArticle)
