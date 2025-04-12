import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.core.db import Base, Date


if TYPE_CHECKING:
    from src.app.transactions.domain.repository.models import Transaction


class RiskLevel(enum.Enum):
    """Risk classification for investment assets"""

    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    SPECULATIVE = "speculative"


class AssetType(enum.Enum):
    CRYPTOCURRENCY = "cryptocurrency"
    STOCK = "stock"
    ETF = "etf"
    BOND = "bond"
    REAL_ESTATE = "real_estate"
    COMMODITY = "commodity"
    FOREX = "forex"
    OTHER = "other"


class InvestmentAsset(MappedAsDataclass, Base, Date, kw_only=True):
    """Base asset that can be invested in (cryptocurrency, stock, etc.)"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    symbol: Mapped[str]  # Ticker symbol or unique identifier
    name: Mapped[str]
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Risk assessment
    risk_level: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel), nullable=True)

    # Educational content
    educational_content_url: Mapped[str | None] = mapped_column(nullable=True)
    asset_class_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # For cryptocurrencies, stocks might have additional metadata
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    price_history: Mapped[list["AssetPrice"]] = relationship(
        "AssetPrice", back_populates="asset", cascade="all, delete-orphan"
    )
    investments: Mapped[list["Investment"]] = relationship(
        "Investment", back_populates="asset"
    )

    # Benchmarks for comparison
    benchmarks: Mapped[list["AssetBenchmark"]] = relationship(
        "AssetBenchmark", back_populates="asset", cascade="all, delete-orphan"
    )


class AssetBenchmark(MappedAsDataclass, Base, Date, kw_only=True):
    """Benchmark data for comparing asset performance"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    asset_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("investment_assets.id", ondelete="CASCADE")
    )
    benchmark_name: Mapped[str]  # e.g., "S&P 500", "Bitcoin"
    benchmark_symbol: Mapped[str | None] = mapped_column(nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    asset: Mapped["InvestmentAsset"] = relationship(
        "InvestmentAsset", back_populates="benchmarks"
    )


class AssetPrice(MappedAsDataclass, Base, Date, kw_only=True):
    """Historical and current price data for assets"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    asset_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("investment_assets.id", ondelete="CASCADE")
    )
    price: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=8))
    price_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    currency: Mapped[str]  # USD, EUR, etc.
    source: Mapped[str | None]  # API or data source name

    # Volume and market data
    volume_24h: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    market_cap: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )

    # Relationships
    asset: Mapped["InvestmentAsset"] = relationship(
        "InvestmentAsset", back_populates="price_history"
    )


class InvestmentGoal(enum.Enum):
    """Purpose of the investment"""

    RETIREMENT = "retirement"
    EDUCATION = "education"
    HOUSE = "house_purchase"
    EMERGENCY_FUND = "emergency_fund"
    WEALTH_BUILDING = "wealth_building"
    INCOME = "income_generation"
    SPECULATION = "speculation"
    OTHER = "other"


class Investment(MappedAsDataclass, Base, Date, kw_only=True):
    """User's investment in a particular asset"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    user_id: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Link to user if applicable
    asset_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("investment_assets.id")
    )
    nickname: Mapped[str | None] = mapped_column(
        nullable=True
    )  # User's custom name for this investment
    target_allocation: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=5, scale=2), nullable=True
    )  # Target % in portfolio
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Investment purpose and goals
    investment_goal: Mapped[InvestmentGoal | None] = mapped_column(
        Enum(InvestmentGoal), nullable=True
    )
    target_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )  # Target date for goal achievement

    # Aggregated data (calculated fields)
    total_units: Mapped[Decimal] = mapped_column(
        Numeric(precision=19, scale=8), default=Decimal("0")
    )
    average_buy_price: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=8), nullable=True
    )
    acquisition_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Performance metrics
    current_value: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    return_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=10, scale=4), nullable=True
    )  # Overall return percentage
    annualized_return: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=10, scale=4), nullable=True
    )  # Annualized return

    # Live pricing settings
    enable_live_updates: Mapped[bool] = mapped_column(Boolean, default=False)
    price_alert_high: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=8), nullable=True
    )
    price_alert_low: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=8), nullable=True
    )

    # Relationships
    asset: Mapped["InvestmentAsset"] = relationship(
        "InvestmentAsset", back_populates="investments"
    )

    # Link to transactions system
    transactions: Mapped[list["Transaction"]] = relationship(
        "src.app.transactions.domain.repository.models.Transaction",
        secondary="investment_transactions",
        backref="investments",
        lazy="noload",
    )

    # Educational notes and disclaimers
    educational_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    has_disclaimer_accepted: Mapped[bool] = mapped_column(Boolean, default=False)


class InvestmentTransaction(MappedAsDataclass, Base, Date, kw_only=True):
    """Junction table linking investments to transactions"""

    investment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("investments.id", ondelete="CASCADE"), primary_key=True
    )
    transaction_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("transactions.id", ondelete="CASCADE"), primary_key=True
    )
    # Additional metadata about this specific investment transaction can be added here
    investment_transaction_type: Mapped[str | None] = mapped_column(
        nullable=True
    )  # BUY, SELL, DIVIDEND, etc.
    units: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=8), nullable=True
    )


class TransactionType(enum.Enum):
    BUY = "buy"
    SELL = "sell"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    STAKING_REWARD = "staking_reward"
    MINING_REWARD = "mining_reward"
    DIVIDEND = "dividend"
    INTEREST = "interest"
    FEE = "fee"
    SPLIT = "split"
    OTHER = "other"


class PriceSource(MappedAsDataclass, Base, Date, kw_only=True):
    """Configuration for price data sources and APIs"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]  # Name of the price source/API
    base_url: Mapped[str]  # Base URL for API calls
    api_key: Mapped[str | None] = mapped_column(nullable=True)  # API key if required
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Configuration details
    supports_live_updates: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # Whether this source supports websockets/live data
    supported_asset_types: Mapped[list[str] | None] = mapped_column(
        JSONB, nullable=True
    )  # Which asset types this source supports
    update_frequency: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Update frequency in seconds
    config: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )  # Additional configuration

    # Rate limiting
    rate_limit: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Requests per minute

    # Asset mappings (how assets are identified in this source)
    asset_mappings: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # Data agreement terms
    data_terms_url: Mapped[str | None] = mapped_column(nullable=True)
    data_terms_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_educational_only: Mapped[bool] = mapped_column(
        Boolean, default=True
    )  # Indicates if data is for educational purposes only


class PortfolioSnapshot(MappedAsDataclass, Base, Date, kw_only=True):
    """Point-in-time snapshot of the investment portfolio"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    snapshot_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    total_value: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    base_currency: Mapped[str]  # USD, EUR, etc.
    snapshot_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB
    )  # Complete portfolio data
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Performance metrics
    overall_return: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=10, scale=4), nullable=True
    )
    period_return: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=10, scale=4), nullable=True
    )  # Return since last snapshot

    # For educational purposes
    includes_disclaimer: Mapped[bool] = mapped_column(Boolean, default=True)
    disclaimer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
