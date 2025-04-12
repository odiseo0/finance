from src.app.news.infrastructure.news_sources import add as add_news_source
from src.app.news.infrastructure.news_sources import edit as edit_news_source
from src.app.news.infrastructure.news_sources import eliminate as eliminate_news_source
from src.app.news.infrastructure.news_sources import read as read_news_source
from src.app.news.infrastructure.news_sources import read_multi as read_news_sources
from src.app.news.infrastructure.newsletter_subscriptions import (
    add as add_newsletter_subscription,
)
from src.app.news.infrastructure.newsletter_subscriptions import (
    edit as edit_newsletter_subscription,
)
from src.app.news.infrastructure.newsletter_subscriptions import (
    eliminate as eliminate_newsletter_subscription,
)
from src.app.news.infrastructure.newsletter_subscriptions import (
    read as read_newsletter_subscription,
)
from src.app.news.infrastructure.newsletter_subscriptions import (
    read_multi as read_newsletter_subscriptions,
)
from src.app.news.infrastructure.saved_articles import add as add_saved_article
from src.app.news.infrastructure.saved_articles import edit as edit_saved_article
from src.app.news.infrastructure.saved_articles import (
    eliminate as eliminate_saved_article,
)
from src.app.news.infrastructure.saved_articles import read as read_saved_article
from src.app.news.infrastructure.saved_articles import read_multi as read_saved_articles


__all__ = [
    "add_news_source",
    "edit_news_source",
    "eliminate_news_source",
    "read_news_source",
    "read_news_sources",
    "add_newsletter_subscription",
    "edit_newsletter_subscription",
    "eliminate_newsletter_subscription",
    "read_newsletter_subscription",
    "read_newsletter_subscriptions",
    "add_saved_article",
    "edit_saved_article",
    "eliminate_saved_article",
    "read_saved_article",
    "read_saved_articles",
]
