from enum import Enum

from src.core.schema import BaseModel


class PriceSourceType(str, Enum):
    API = "api"
    MANUAL = "manual"
    SCRAPED = "scraped"
    CALCULATED = "calculated"
    IMPORTED = "imported"
    OTHER = "other"


class PriceSource(BaseModel):
    name: str | None = None
    source_type: PriceSourceType | None = None
    url: str | None = None
    api_key: str | None = None
    is_active: bool | None = None
    priority: int | None = None
    description: str | None = None
    update_frequency: str | None = None
    last_update: str | None = None
    config: dict | None = None


class PriceSourceCreate(PriceSource):
    name: str
    source_type: PriceSourceType


class PriceSourceUpdate(BaseModel):
    name: str | None = None
    source_type: PriceSourceType | None = None
    url: str | None = None
    api_key: str | None = None
    is_active: bool | None = None
    priority: int | None = None
    description: str | None = None
    update_frequency: str | None = None
    last_update: str | None = None
    config: dict | None = None


class PriceSourceResponse(PriceSource):
    id: int
