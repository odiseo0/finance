from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.contrib.pydantic import PydanticPlugin
from litestar.di import Provide
from litestar.stores.memory import MemoryStore
from litestar.stores.registry import StoreRegistry

from src.core.db import get_db
from src.core.utils.filters import filter_dependencies
from src.settings import api_settings, docs_config


cors_config = CORSConfig(expose_headers=["Content-Disposition"])
plugin = PydanticPlugin(prefer_alias=True)


@get("/")
async def index() -> str:
    return "Finance API"


app = Litestar(
    route_handlers=[index],
    openapi_config=docs_config,
    docs_url=api_settings.DOCS_URL,
    dependencies={"db": Provide(get_db), **filter_dependencies},
    debug=api_settings.DEV_MODE,
    plugins=[plugin],
    cors_config=cors_config,
    stores=StoreRegistry({"store": MemoryStore()}),
)
