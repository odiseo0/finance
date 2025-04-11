from datetime import datetime
from decimal import Decimal

from src.core.schema import BaseModel


class SubscriptionPayment(BaseModel):
    subscription_id: int | None = None
    transaction_id: int | None = None
    amount: Decimal | None = None
    payment_date: datetime | None = None
    expected_amount: Decimal | None = None
    price_change: bool | None = None
    notes: str | None = None


class SubscriptionPaymentCreate(SubscriptionPayment):
    subscription_id: int
    amount: Decimal
    payment_date: datetime


class SubscriptionPaymentUpdate(BaseModel):
    transaction_id: int | None = None
    amount: Decimal | None = None
    payment_date: datetime | None = None
    expected_amount: Decimal | None = None
    price_change: bool | None = None
    notes: str | None = None


class SubscriptionPaymentResponse(SubscriptionPayment):
    id: int
