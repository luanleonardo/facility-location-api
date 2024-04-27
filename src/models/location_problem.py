import numpy as np
from pydantic import BaseModel, ConfigDict

from src.models import Client, Facility


class LocationProblem(BaseModel):
    """Model representing a facility location problem."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    number_new_facilities: int
    clients: list[Client]
    fixed_facilities: list[Facility]
    cost_matrix: np.ndarray
    solver_time_limit_seconds: int = 80
