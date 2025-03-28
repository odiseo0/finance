from src.core.schema import BaseModel


class AssetBenchmark(BaseModel):
    asset_id: int | None = None
    benchmark_name: str | None = None
    benchmark_symbol: str | None = None
    is_default: bool | None = None


class AssetBenchmarkCreate(AssetBenchmark):
    asset_id: int
    benchmark_name: str


class AssetBenchmarkUpdate(BaseModel):
    benchmark_name: str | None = None
    benchmark_symbol: str | None = None
    is_default: bool | None = None


class AssetBenchmarkResponse(AssetBenchmark):
    id: int
