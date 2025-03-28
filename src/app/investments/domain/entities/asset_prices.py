from datetime import datetime
from decimal import Decimal

from src.core.schema import BaseModel


class AssetPrice(BaseModel):
    asset_id: int | None = None
    price: Decimal | None = None
    price_date: datetime | None = None
    currency: str | None = None
    source: str | None = None
    volume_24h: Decimal | None = None
    market_cap: Decimal | None = None


class AssetPriceCreate(AssetPrice):
    asset_id: int
    price: Decimal
    price_date: datetime
    currency: str


class AssetPriceUpdate(BaseModel):
    price: Decimal | None = None
    price_date: datetime | None = None
    currency: str | None = None
    source: str | None = None
    volume_24h: Decimal | None = None
    market_cap: Decimal | None = None


class AssetPriceResponse(AssetPrice):
    id: int
