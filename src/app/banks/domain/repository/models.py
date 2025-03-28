import enum
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.core.db import Base, Date


if TYPE_CHECKING:
    from src.app.transactions.domain.repository.models import Transaction


class InstitutionType(enum.Enum):
    """Types of financial institutions or money storage locations"""

    BANK = "bank"  # Traditional banks
    CREDIT_UNION = "credit_union"  # Credit unions
    DIGITAL_WALLET = "digital_wallet"  # PayPal, Venmo, Cash App
    CRYPTO_EXCHANGE = "crypto_exchange"  # Coinbase, Binance
    INVESTMENT_PLATFORM = "investment"  # Brokerages, investment platforms
    PREPAID_CARD = "prepaid_card"  # Prepaid debit cards
    PHYSICAL_WALLET = "physical_wallet"  # Physical cash storage
    NEOBANK = "neobank"  # Neobanks and fintech apps
    OTHER = "other"  # Other financial institutions


class FinancialInstitution(MappedAsDataclass, Base, Date, kw_only=True):
    """Financial institutions where users store money"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]  # Name of the institution
    institution_type: Mapped[InstitutionType] = mapped_column(Enum(InstitutionType))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Institution details
    website: Mapped[str | None] = mapped_column(nullable=True)
    phone: Mapped[str | None] = mapped_column(nullable=True)
    logo_url: Mapped[str | None] = mapped_column(nullable=True)
    country: Mapped[str | None] = mapped_column(nullable=True)  # Country code

    # Integration information
    has_api_integration: Mapped[bool] = mapped_column(Boolean, default=False)
    api_details: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    accounts: Mapped[list["InstitutionAccount"]] = relationship(
        "InstitutionAccount", back_populates="institution", cascade="all, delete-orphan"
    )


class InstitutionAccount(MappedAsDataclass, Base, Date, kw_only=True):
    """User accounts at financial institutions"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("financial_institutions.id", ondelete="CASCADE")
    )
    name: Mapped[str]  # Account name (e.g., "Main Checking")
    account_number_masked: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Masked for security

    # Balance information
    current_balance: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    available_balance: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Account details
    opened_date: Mapped[date | None] = mapped_column(nullable=True)
    closed_date: Mapped[date | None] = mapped_column(nullable=True)
    interest_rate: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=6, scale=4), nullable=True
    )

    # Credit accounts
    credit_limit: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )  # For credit cards
    payment_due_date: Mapped[date | None] = mapped_column(nullable=True)
    minimum_payment: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )

    last_sync_attempt: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    exclude_from_net_worth: Mapped[bool] = mapped_column(Boolean, default=False)

    # Additional information
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    institution: Mapped["FinancialInstitution"] = relationship(
        "FinancialInstitution", back_populates="accounts"
    )
    bank_movements: Mapped[list["BankMovement"]] = relationship(
        "BankMovement", back_populates="account", cascade="all, delete-orphan"
    )


class BankMovement(MappedAsDataclass, Base, Date, kw_only=True):
    """Movements of money in and out of accounts"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("financial_accounts.id", ondelete="CASCADE")
    )
    transaction_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("src.app.transactions.domain.repository.models.Transaction.id"),
        nullable=True,
    )

    # Movement details
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Balance information
    running_balance: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=19, scale=2), nullable=True
    )

    # Transaction data
    reference: Mapped[str | None] = mapped_column(nullable=True)  # Bank reference
    merchant_name: Mapped[str | None] = mapped_column(nullable=True)
    category: Mapped[str | None] = mapped_column(nullable=True)  # Bank category

    # Reconciliation status
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False)

    # Additional data
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )  # Original transaction data
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    account: Mapped["InstitutionAccount"] = relationship(
        "InstitutionAccount", back_populates="bank_movements"
    )
    transaction: Mapped["Transaction"] = relationship(
        "src.app.transactions.domain.repository.models.Transaction",
        backref="bank_movements",
        viewonly=True,
    )


class BalanceHistory(MappedAsDataclass, Base, Date, kw_only=True):
    """Historical balance records for accounts"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("financial_accounts.id", ondelete="CASCADE")
    )

    # Balance information
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    balance_date: Mapped[date] = mapped_column()

    # Snapshot type
    is_eod: Mapped[bool] = mapped_column(Boolean, default=True)  # End of day
    is_manual: Mapped[bool] = mapped_column(Boolean, default=False)  # Manual entry

    # Account relationship
    account: Mapped["InstitutionAccount"] = relationship("InstitutionAccount")


class AccountLink(MappedAsDataclass, Base, Date, kw_only=True):
    """Secure credentials and connection details for account sync"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("financial_accounts.id", ondelete="CASCADE"), unique=True
    )

    # Connection details
    provider: Mapped[str | None] = mapped_column(nullable=True)  # Integration provider
    access_token: Mapped[str | None] = mapped_column(nullable=True)  # Encrypted
    refresh_token: Mapped[str | None] = mapped_column(nullable=True)  # Encrypted
    token_expiry: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    last_successful_sync: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Secure storage
    credentials_hash: Mapped[str | None] = mapped_column(
        nullable=True
    )  # For manual verification

    # Account relationship
    account: Mapped["InstitutionAccount"] = relationship("InstitutionAccount")
