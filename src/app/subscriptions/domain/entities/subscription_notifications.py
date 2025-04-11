from datetime import datetime

from src.core.schema import BaseModel


class SubscriptionNotification(BaseModel):
    subscription_id: int | None = None
    notification_type: str | None = None
    message: str | None = None
    notification_date: datetime | None = None
    is_read: bool | None = None


class SubscriptionNotificationCreate(SubscriptionNotification):
    subscription_id: int
    notification_type: str
    message: str
    notification_date: datetime


class SubscriptionNotificationUpdate(BaseModel):
    notification_type: str | None = None
    message: str | None = None
    notification_date: datetime | None = None
    is_read: bool | None = None


class SubscriptionNotificationResponse(SubscriptionNotification):
    id: int
