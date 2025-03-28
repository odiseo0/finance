from src.app.budgets.domain.entities import (
    BudgetAnalysisCreate,
    BudgetAnalysisUpdate,
    BudgetCategoryCreate,
    BudgetCategoryUpdate,
    BudgetCreate,
    BudgetExpenseCreate,
    BudgetExpenseUpdate,
    BudgetTemplateCreate,
    BudgetTemplateUpdate,
    BudgetUpdate,
)
from src.core.db import DAO

from .models import (
    Budget,
    BudgetAnalysis,
    BudgetCategory,
    BudgetExpense,
    BudgetTemplate,
)


class DAOBudget(DAO[Budget, BudgetCreate, BudgetUpdate]):
    pass


class DAOBudgetCategory(
    DAO[BudgetCategory, BudgetCategoryCreate, BudgetCategoryUpdate]
):
    pass


class DAOBudgetExpense(DAO[BudgetExpense, BudgetExpenseCreate, BudgetExpenseUpdate]):
    pass


class DAOBudgetTemplate(
    DAO[BudgetTemplate, BudgetTemplateCreate, BudgetTemplateUpdate]
):
    pass


class DAOBudgetAnalysis(
    DAO[BudgetAnalysis, BudgetAnalysisCreate, BudgetAnalysisUpdate]
):
    pass


dao_budgets = DAOBudget(Budget)
dao_budget_categories = DAOBudgetCategory(BudgetCategory)
dao_budget_expenses = DAOBudgetExpense(BudgetExpense)
dao_budget_templates = DAOBudgetTemplate(BudgetTemplate)
dao_budget_analysis = DAOBudgetAnalysis(BudgetAnalysis)
