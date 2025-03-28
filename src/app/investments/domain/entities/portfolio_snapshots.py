from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from src.core.schema import BaseModel


class AssetAllocation(BaseModel):
    asset_id: int
    allocation_percentage: Decimal
    current_value: Decimal


class PortfolioPerformance(BaseModel):
    time_period: str  # "1d", "1w", "1m", "3m", "6m", "1y", "ytd", "all"
    return_percentage: Decimal
    absolute_return: Decimal
    benchmark_return: Decimal | None = None
    benchmark_symbol: str | None = None


class PortfolioSnapshot(BaseModel):
    user_id: str | None = None
    snapshot_date: datetime | None = None
    total_value: Decimal | None = None
    cash_balance: Decimal | None = None
    invested_amount: Decimal | None = None
    total_return: Decimal | None = None
    return_percentage: Decimal | None = None
    annualized_return: Decimal | None = None
    asset_allocations: List[AssetAllocation] | None = None
    performance_data: Dict[str, PortfolioPerformance] | None = None
    risk_metrics: Dict[str, Decimal] | None = None
    currency: str | None = None
    notes: str | None = None


class PortfolioSnapshotCreate(PortfolioSnapshot):
    user_id: str
    snapshot_date: datetime
    total_value: Decimal


class PortfolioSnapshotUpdate(BaseModel):
    snapshot_date: datetime | None = None
    total_value: Decimal | None = None
    cash_balance: Decimal | None = None
    invested_amount: Decimal | None = None
    total_return: Decimal | None = None
    return_percentage: Decimal | None = None
    annualized_return: Decimal | None = None
    asset_allocations: List[AssetAllocation] | None = None
    performance_data: Dict[str, PortfolioPerformance] | None = None
    risk_metrics: Dict[str, Decimal] | None = None
    currency: str | None = None
    notes: str | None = None


class PortfolioSnapshotResponse(PortfolioSnapshot):
    id: int
