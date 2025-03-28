from src.app.transactions.domain.entities import (
    TransactionCreate,
    TransactionFileCreate,
    TransactionFileUpdate,
    TransactionTypeCreate,
    TransactionTypeUpdate,
    TransactionUpdate,
)
from src.core.db import DAO

from .models import Transaction, TransactionFile, TransactionType


class DAOTransactionType(
    DAO[TransactionType, TransactionTypeCreate, TransactionTypeUpdate]
):
    pass


class DAOTransaction(DAO[Transaction, TransactionCreate, TransactionUpdate]):
    pass


class DAOTransactionFiles(
    DAO[TransactionFile, TransactionFileCreate, TransactionFileUpdate]
):
    pass


dao_transaction_types = DAOTransactionType(TransactionType)
dao_transactions = DAOTransaction(Transaction)
dao_transaction_files = DAOTransactionFiles(TransactionFile)
