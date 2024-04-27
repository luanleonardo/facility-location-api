from copy import deepcopy

import numpy as np

from config import settings
from src.models import Client, Facility, LocationProblem


def scale_problem_parameters(
    location_problem: LocationProblem,
) -> tuple[list[Client], list[Facility], np.ndarray]:
    """Scale problem factors to become integer"""

    scale_factor = settings.SCALE_FACTOR
    scaled_clients = deepcopy(location_problem.clients)
    for client in scaled_clients:
        client.demand = round(scale_factor * client.demand)

    scaled_fixed_facilities = deepcopy(location_problem.fixed_facilities)
    for facility in scaled_fixed_facilities:
        facility.demand.min = round(scale_factor * facility.demand.min)
        facility.demand.max = round(scale_factor * facility.demand.max)

    scaled_cost_matrix = location_problem.cost_matrix.copy()
    scaled_cost_matrix *= scale_factor

    return (
        scaled_clients,
        scaled_fixed_facilities,
        scaled_cost_matrix.astype(int),
    )
