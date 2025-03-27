from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DSN: str

    model_config: ClassVar[SettingsConfigDict] = {"env_file": ".env", "extra": "ignore"}

    @property
    def url(self) -> str:
        """Database driver URL"""

        return f"postgresql+asyncpg://{self.DSN}"


db_settings = DatabaseSettings()
