from src.app.goals.domain.entities import (
    GoalCalculationCreate,
    GoalCalculationUpdate,
    GoalContributionCreate,
    GoalContributionUpdate,
    GoalCreate,
    GoalMilestoneCreate,
    GoalMilestoneUpdate,
    GoalUpdate,
)
from src.core.db import DAO

from .models import Goal, GoalCalculation, GoalContribution, GoalMilestone


class DAOGoal(DAO[Goal, GoalCreate, GoalUpdate]):
    pass


class DAOGoalContribution(
    DAO[GoalContribution, GoalContributionCreate, GoalContributionUpdate]
):
    pass


class DAOGoalMilestone(DAO[GoalMilestone, GoalMilestoneCreate, GoalMilestoneUpdate]):
    pass


class DAOGoalCalculation(
    DAO[GoalCalculation, GoalCalculationCreate, GoalCalculationUpdate]
):
    pass


dao_goals = DAOGoal(Goal)
dao_goal_contributions = DAOGoalContribution(GoalContribution)
dao_goal_milestones = DAOGoalMilestone(GoalMilestone)
dao_goal_calculations = DAOGoalCalculation(GoalCalculation)
