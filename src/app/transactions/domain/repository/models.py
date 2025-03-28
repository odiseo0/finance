import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.core.db import Base, Date


if TYPE_CHECKING:
    from src.app.banks.domain.repository.models import BankMovement


class TransactionCategory(enum.Enum):
    """Categories for classifying transactions"""

    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    INVESTMENT = "investment"
    LOAN = "loan"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"
    TAX = "tax"
    OTHER = "other"


class TransactionType(MappedAsDataclass, Base, Date, kw_only=True):
    """Types of transactions in the system"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[TransactionCategory | None] = mapped_column(
        Enum(TransactionCategory), nullable=True
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="transaction_type",
    )


class Transaction(MappedAsDataclass, Base, Date, kw_only=True):
    """Financial transactions recorded in the system"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    transaction_type_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("transaction_types.id")
    )
    value: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=8))
    value_in_usd: Mapped[Decimal | None] = mapped_column(Numeric(precision=19, scale=8))
    currency: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    concept: Mapped[str | None] = mapped_column(Text)
    payment_reference: Mapped[str | None]
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None] = mapped_column(Text)

    # Relationships
    transaction_type: Mapped[TransactionType] = relationship(
        "TransactionType",
        back_populates="transactions",
    )
    files: Mapped[list["TransactionFile"]] = relationship(
        "TransactionFile",
        back_populates="transaction",
        lazy="joined",
    )
    bank_movements: Mapped[list["BankMovement"]] = relationship(
        "src.app.banks.domain.repository.models.BankMovement",
        cascade="all, delete-orphan",
        lazy="noload",
    )
    tags: Mapped[list["TransactionTag"]] = relationship(
        "TransactionTag",
        secondary="transaction_tag_mapping",
        back_populates="transactions",
        lazy="joined",
    )


class TransactionFile(MappedAsDataclass, Base, Date, kw_only=True):
    """Files attached to transactions"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    transaction_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("transactions.id", ondelete="CASCADE")
    )
    file: Mapped[str]
    file_type: Mapped[str | None] = mapped_column(
        nullable=True
    )  # receipt, invoice, contract, etc.
    note: Mapped[str | None] = mapped_column(Text)
    is_encrypted: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # Privacy feature

    transaction: Mapped["Transaction"] = relationship(
        "Transaction",
        back_populates="files",
    )


class TransactionTag(MappedAsDataclass, Base, Date, kw_only=True):
    """Tags for categorizing and filtering transactions"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str | None] = mapped_column(nullable=True)  # Hex color for UI

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        secondary="transaction_tag_mapping",
        back_populates="tags",
    )


class TransactionTagMapping(MappedAsDataclass, Base, Date, kw_only=True):
    """Mapping table for transactions to tags many-to-many relationship"""

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, autoincrement=True, primary_key=True
    )
    transaction_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("transactions.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("transaction_tags.id", ondelete="CASCADE"),
        primary_key=True,
    )
