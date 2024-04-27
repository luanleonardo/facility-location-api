from config import settings
from src.services import scale_problem_parameters


def test_scale_assignment_problem_parameters(location_problem):
    """Test scaling of assignment problem parameters"""
    scale_factor = settings.SCALE_FACTOR

    # Scale problem parameters to become integer
    scaled_clients, scaled_facilities, scaled_cost_matrix = (
        scale_problem_parameters(
            location_problem=location_problem,
        )
    )

    assert all(client.demand % scale_factor == 0 for client in scaled_clients)
    assert all(
        facility.demand.min % scale_factor == 0
        and facility.demand.max % scale_factor == 0
        for facility in scaled_facilities
    )
    assert scaled_cost_matrix.dtype == int
