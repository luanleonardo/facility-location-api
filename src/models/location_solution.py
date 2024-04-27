from enum import Enum
from math import inf

from pydantic import BaseModel, NonNegativeFloat

from src.models import Facility


class SolutionStatus(Enum):
    """Status of the solution"""

    INFEASIBLE = "infeasible"
    FEASIBLE = "feasible"
    OPTIMAL = "optimal"


class LocationSolution(BaseModel):
    """Model representing a facility location solution."""

    total_costs: NonNegativeFloat = inf
    facilities: list[Facility] = []
    status: SolutionStatus = SolutionStatus.INFEASIBLE
    message: str = ""
