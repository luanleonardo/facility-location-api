import cost_matrix
import numpy as np

from src.models import CostProblem, CostType


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
        return demands * cost_matrix.spherical(
            sources=sources, destinations=destinations
        )

    return demands * cost_matrix.osrm(
        sources=sources,
        destinations=destinations,
        server_address=cost_problem.osrm_server_address,
        batch_size=cost_problem.osrm_batch_size,
        cost_type=cost_problem.cost_type.value,
    )
