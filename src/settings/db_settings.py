from typing import Any, ClassVar

from asyncpg import Record
from asyncpg.connection import Connection
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DSN: str

    connect_kwargs: dict[str, Any] | None = None
    """A dictionary of arguments which will be passed directly to the ``connect()`` method as kwargs"""
    connection_class: type[Connection] | None = None
    """The class to use for connections. Must be a subclass of Connection"""
    record_class: type[Record] | None = None

    pool_size: int = 10
    """The number of connections to keep open inside the connection pool."""
    pool_overflow: int = 10
    """
    The number of connections to allow in connection pool “overflow”, that is connections that can be opened above
    and beyond the pool_size setting, which defaults to 10.
    """

    max_queries: int | None = None
    """
    Number of queries after a connection is closed and replaced with a new connection.
    """
    pool_recycle: int = 3600
    pool_timeout: int = 60
    max_inactive_connection_lifetime: float = 300.0  # 5 minutes

    model_config: ClassVar[SettingsConfigDict] = {"env_file": ".env", "extra": "ignore"}

    @property
    def url(self) -> str:
        """Database driver URL"""

        return f"postgresql+asyncpg://{self.DSN}"


db_settings = DatabaseSettings()
