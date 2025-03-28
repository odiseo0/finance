from typing import Any

from src.app.investments.domain.repository.models import AssetType, RiskLevel
from src.core.schema import BaseModel

from .asset_prices import AssetPriceResponse
from .benchmarks import AssetBenchmarkResponse


class Asset(BaseModel):
    symbol: str | None = None
    name: str | None = None
    asset_type: AssetType | None = None
    description: str | None = None
    icon_url: str | None = None
    is_active: bool | None = None
    risk_level: RiskLevel | None = None
    educational_content_url: str | None = None
    asset_class_description: str | None = None
    metadata: dict[str, Any] | None = None


class AssetCreate(Asset):
    symbol: str
    name: str
    asset_type: AssetType


class AssetUpdate(BaseModel):
    symbol: str | None = None
    name: str | None = None
    asset_type: AssetType | None = None
    description: str | None = None
    icon_url: str | None = None
    is_active: bool | None = None
    risk_level: RiskLevel | None = None
    educational_content_url: str | None = None
    asset_class_description: str | None = None
    metadata: dict[str, Any] | None = None


class AssetResponse(Asset):
    id: int
    price_history: list[AssetPriceResponse] | None = None
    benchmarks: list[AssetBenchmarkResponse] | None = None
