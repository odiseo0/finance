from datetime import datetime

from src.core.schema import BaseModel


class AccountLink(BaseModel):
    account_id: int | None = None
    provider: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    token_expiry: datetime | None = None
    last_successful_sync: datetime | None = None
    credentials_hash: str | None = None


class AccountLinkCreate(AccountLink):
    account_id: int


class AccountLinkUpdate(BaseModel):
    provider: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    token_expiry: datetime | None = None
    last_successful_sync: datetime | None = None
    credentials_hash: str | None = None


class AccountLinkResponse(AccountLink):
    id: int
