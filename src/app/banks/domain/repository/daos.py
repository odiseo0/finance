from src.app.banks.domain.entities import (
    AccountCreate,
    AccountLinkCreate,
    AccountLinkUpdate,
    AccountUpdate,
    BalanceHistoryCreate,
    BalanceHistoryUpdate,
    BankMovementCreate,
    BankMovementUpdate,
    InstitutionCreate,
    InstitutionUpdate,
)
from src.core.db import DAO

from .models import (
    AccountLink,
    BalanceHistory,
    BankMovement,
    FinancialInstitution,
    InstitutionAccount,
)


class DAOFinancialInstitution(
    DAO[FinancialInstitution, InstitutionCreate, InstitutionUpdate]
):
    pass


class DAOInstitutionAccount(DAO[InstitutionAccount, AccountCreate, AccountUpdate]):
    pass


class DAOBankMovement(DAO[BankMovement, BankMovementCreate, BankMovementUpdate]):
    pass


class DAOBalanceHistory(
    DAO[BalanceHistory, BalanceHistoryCreate, BalanceHistoryUpdate]
):
    pass


class DAOAccountLink(DAO[AccountLink, AccountLinkCreate, AccountLinkUpdate]):
    pass


dao_institutions = DAOFinancialInstitution(FinancialInstitution)
dao_accounts = DAOInstitutionAccount(InstitutionAccount)
dao_bank_movements = DAOBankMovement(BankMovement)
dao_balance_history = DAOBalanceHistory(BalanceHistory)
dao_account_links = DAOAccountLink(AccountLink)
