from typing import ClassVar

from litestar.openapi import OpenAPIConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


docs_config = OpenAPIConfig(
    title="App Finance API",
    version="0.0.1",
    description="App Finance Application Programming Interface",
    root_schema_site="elements",
)


class APISettings(BaseSettings):
    DEV_MODE: bool = False
    API_KEY: str | None = None

    model_config: ClassVar[SettingsConfigDict] = {"env_file": ".env", "extra": "ignore"}


api_settings = APISettings()
