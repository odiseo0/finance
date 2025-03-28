from src.app.investments.domain.entities import (
    AssetBenchmarkCreate,
    AssetBenchmarkUpdate,
    AssetCreate,
    AssetPriceCreate,
    AssetPriceUpdate,
    AssetUpdate,
    InvestmentCreate,
    InvestmentTransactionCreate,
    InvestmentTransactionUpdate,
    InvestmentUpdate,
    PortfolioSnapshotCreate,
    PortfolioSnapshotUpdate,
    PriceSourceCreate,
    PriceSourceUpdate,
)
from src.core.db import DAO

from .models import (
    AssetBenchmark,
    AssetPrice,
    Investment,
    InvestmentAsset,
    InvestmentTransaction,
    PortfolioSnapshot,
    PriceSource,
)


class DAOInvestmentAsset(DAO[InvestmentAsset, AssetCreate, AssetUpdate]):
    pass


class DAOAssetPrice(DAO[AssetPrice, AssetPriceCreate, AssetPriceUpdate]):
    pass


class DAOAssetBenchmark(
    DAO[AssetBenchmark, AssetBenchmarkCreate, AssetBenchmarkUpdate]
):
    pass


class DAOInvestment(DAO[Investment, InvestmentCreate, InvestmentUpdate]):
    pass


class DAOInvestmentTransaction(
    DAO[InvestmentTransaction, InvestmentTransactionCreate, InvestmentTransactionUpdate]
):
    pass


class DAOPriceSource(DAO[PriceSource, PriceSourceCreate, PriceSourceUpdate]):
    pass


class DAOPortfolioSnapshot(
    DAO[PortfolioSnapshot, PortfolioSnapshotCreate, PortfolioSnapshotUpdate]
):
    pass


dao_assets = DAOInvestmentAsset(InvestmentAsset)
dao_asset_prices = DAOAssetPrice(AssetPrice)
dao_asset_benchmarks = DAOAssetBenchmark(AssetBenchmark)
dao_investments = DAOInvestment(Investment)
dao_investment_transactions = DAOInvestmentTransaction(InvestmentTransaction)
dao_price_sources = DAOPriceSource(PriceSource)
dao_portfolio_snapshots = DAOPortfolioSnapshot(PortfolioSnapshot)
