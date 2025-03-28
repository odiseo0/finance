from src.app.subscriptions.domain.entities import (
    SubscriptionCreate,
    SubscriptionNotificationCreate,
    SubscriptionNotificationUpdate,
    SubscriptionPaymentCreate,
    SubscriptionPaymentUpdate,
    SubscriptionUpdate,
)
from src.core.db import DAO

from .models import Subscription, SubscriptionNotification, SubscriptionPayment


class DAOSubscription(DAO[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    pass


class DAOSubscriptionPayment(
    DAO[SubscriptionPayment, SubscriptionPaymentCreate, SubscriptionPaymentUpdate]
):
    pass


class DAOSubscriptionNotification(
    DAO[
        SubscriptionNotification,
        SubscriptionNotificationCreate,
        SubscriptionNotificationUpdate,
    ]
):
    pass


dao_subscriptions = DAOSubscription(Subscription)
dao_subscription_payments = DAOSubscriptionPayment(SubscriptionPayment)
dao_subscription_notifications = DAOSubscriptionNotification(SubscriptionNotification)
