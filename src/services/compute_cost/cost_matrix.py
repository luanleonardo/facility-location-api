import numpy as np

from src.models import CostProblem, CostType
from src.services import osrm_cost_matrix, spherical_cost_matrix

OSRM_COST_TYPE_MAPPING = {
    CostType.TRAVEL_DISTANCE.value: "distances",
    CostType.TRAVEL_DURATION.value: "durations",
}


def compute_cost_matrix(cost_problem: CostProblem) -> np.ndarray:
    """Compute cost matrix with a given cost type"""

    sources = np.array(
        [
            x.location.to_list()
            for x in cost_problem.fixed_facilities + cost_problem.clients
        ]
    )
    destinations = np.array(
        [client.location.to_list() for client in cost_problem.clients]
    )
    demands = np.array([client.demand for client in cost_problem.clients])

    if cost_problem.cost_type == CostType.PROXIMITY:
        return demands * spherical_cost_matrix(
            sources=sources, destinations=destinations
        )

    return demands * osrm_cost_matrix(
        sources=sources,
        destinations=destinations,
        osrm_server_address=cost_problem.osrm_server_address,
        osrm_batch_size=cost_problem.osrm_batch_size,
        cost_type=OSRM_COST_TYPE_MAPPING[cost_problem.cost_type.value],
    )
