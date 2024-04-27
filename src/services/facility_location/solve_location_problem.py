from typing import List, Tuple

import numpy as np

from src.api.schemas.locate import LocationRequest
from src.models import Client, CostProblem, LocationProblem, LocationSolution
from src.services import (
    cluster_clients,
    compute_cost_matrix,
    scale_demands,
    solve_integer_formulation,
)


def _handle_nans(
    cost_matrix: np.ndarray,
    clients: List[Client],
) -> Tuple[np.ndarray, List[Client]]:
    """
    Some `cost_matrix` entries may experience problems and receive a NaN.
    In this case, there is not much we can do other than remove them from
    the analysis.

    This means that we should remove all such columns from the `cost_matrix`,
    plus delete these clients from the request. Notice the remaining ones
    should be rescaled to keep the original total demand.
    """
    _, invalid_client_indices = np.nonzero(np.isnan(cost_matrix))
    unique_invalid_client_indices = np.unique(invalid_client_indices)
    valid_cost_matrix = np.delete(
        cost_matrix, unique_invalid_client_indices, axis=1
    )
    valid_clients = [
        client
        for i, client in enumerate(clients)
        if i not in unique_invalid_client_indices
    ]

    original_total_demand = sum([client.demand for client in clients])
    scaled_valid_clients = scale_demands(
        clients=valid_clients,
        new_total_demand=original_total_demand,
    )

    return valid_cost_matrix, scaled_valid_clients


def solve_facility_location(
    location_request: LocationRequest,
) -> LocationSolution:

    clustered_clients = cluster_clients(
        clients=location_request.clients,
        number_clusters=location_request.number_client_clusters,
    )

    cost_problem = CostProblem(
        clients=clustered_clients,
        fixed_facilities=location_request.fixed_facilities,
        cost_type=location_request.cost_type,
    )

    cost_matrix = compute_cost_matrix(cost_problem=cost_problem)
    valid_cost_matrix, scaled_valid_clients = _handle_nans(
        cost_matrix=cost_matrix, clients=cost_problem.clients
    )

    location_problem = LocationProblem(
        clients=scaled_valid_clients,
        fixed_facilities=location_request.fixed_facilities,
        cost_matrix=valid_cost_matrix,
        number_new_facilities=location_request.number_new_facilities,
    )

    return solve_integer_formulation(location_problem=location_problem)
