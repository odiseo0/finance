from src.app.investments.infrastructure.asset_holdings import add as add_asset_holding
from src.app.investments.infrastructure.asset_holdings import edit as edit_asset_holding
from src.app.investments.infrastructure.asset_holdings import (
    eliminate as eliminate_asset_holding,
)
from src.app.investments.infrastructure.asset_holdings import read as read_asset_holding
from src.app.investments.infrastructure.asset_holdings import (
    read_multi as read_asset_holdings,
)
from src.app.investments.infrastructure.asset_prices import add as add_asset_price
from src.app.investments.infrastructure.asset_prices import edit as edit_asset_price
from src.app.investments.infrastructure.asset_prices import (
    eliminate as eliminate_asset_price,
)
from src.app.investments.infrastructure.asset_prices import read as read_asset_price
from src.app.investments.infrastructure.asset_prices import (
    read_multi as read_asset_prices,
)
from src.app.investments.infrastructure.assets import add as add_asset
from src.app.investments.infrastructure.assets import edit as edit_asset
from src.app.investments.infrastructure.assets import eliminate as eliminate_asset
from src.app.investments.infrastructure.assets import read as read_asset
from src.app.investments.infrastructure.assets import read_multi as read_assets
from src.app.investments.infrastructure.benchmarks import add as add_asset_benchmark
from src.app.investments.infrastructure.benchmarks import edit as edit_asset_benchmark
from src.app.investments.infrastructure.benchmarks import (
    eliminate as eliminate_asset_benchmark,
)
from src.app.investments.infrastructure.benchmarks import read as read_asset_benchmark
from src.app.investments.infrastructure.benchmarks import (
    read_multi as read_asset_benchmarks,
)


__all__ = [
    # Assets
    "add_asset",
    "edit_asset",
    "eliminate_asset",
    "read_asset",
    "read_assets",
    # Asset Prices
    "add_asset_price",
    "edit_asset_price",
    "eliminate_asset_price",
    "read_asset_price",
    "read_asset_prices",
    # Asset Benchmarks
    "add_asset_benchmark",
    "edit_asset_benchmark",
    "eliminate_asset_benchmark",
    "read_asset_benchmark",
    "read_asset_benchmarks",
    # Asset Holdings
    "add_asset_holding",
    "edit_asset_holding",
    "eliminate_asset_holding",
    "read_asset_holding",
    "read_asset_holdings",
]
