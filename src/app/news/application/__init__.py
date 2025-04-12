from src.app.news.application.news_sources_cases import (
    create_news_source,
    get_news_source,
    get_news_sources,
    remove_news_source,
    update_news_source,
)
from src.app.news.application.newsletter_subscriptions_cases import (
    create_newsletter_subscription,
    get_newsletter_subscription,
    get_newsletter_subscriptions,
    remove_newsletter_subscription,
    update_newsletter_subscription,
)
from src.app.news.application.saved_articles_cases import (
    create_saved_article,
    get_saved_article,
    get_saved_articles,
    remove_saved_article,
    update_saved_article,
)


__all__ = [
    "get_news_source",
    "get_news_sources",
    "create_news_source",
    "update_news_source",
    "remove_news_source",
    "get_newsletter_subscription",
    "get_newsletter_subscriptions",
    "create_newsletter_subscription",
    "update_newsletter_subscription",
    "remove_newsletter_subscription",
    "get_saved_article",
    "get_saved_articles",
    "create_saved_article",
    "update_saved_article",
    "remove_saved_article",
]
