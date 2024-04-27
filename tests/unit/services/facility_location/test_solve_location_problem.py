import pytest

from src.api.schemas.locate import LocationRequest
from src.models import (
    Client,
    CostProblem,
    CostType,
    Facility,
    Location,
    LocationProblem,
)
from src.models.location_solution import SolutionStatus
from src.services import (
    compute_cost_matrix,
    solve_facility_location,
    solve_integer_formulation,
)
from src.utils import field_to_valid_multipolygon


@pytest.fixture
def clients_in_square():
    coordinates = [
        (0.75, 0.75),
        (0.5, 1.5),
        (1.5, 1.5),
        (1.5, 0.5),
        (2.5, 3.5),
        (2.5, 2.5),
        (3.5, 2.5),
        (3.5, 3.5),
    ]

    return [
        Client(id=f"client_{i}", location=Location(lat=lat, lng=lng))
        for i, (lat, lng) in enumerate(coordinates)
    ]


@pytest.fixture
def facilities_in_square():
    facilities_data = [
        {
            "id": "1",
            "name": "FC1",
            "location": {"lat": 1.0, "lng": 1.0},
            "demand": {"max": 1},
        },
        {
            "id": "2",
            "name": "FC2",
            "location": {"lat": 3.0, "lng": 3.0},
        },
    ]

    return [Facility(**data) for data in facilities_data]


@pytest.fixture
def facilities_with_exclusive_region():
    exclusive_region_1 = {
        "coordinates": [
            [
                [2.25, 2.25],
                [2.75, 2.25],
                [2.75, 2.75],
                [2.25, 2.75],
                [2.25, 2.25],
            ]
        ],
        "type": "Polygon",
    }
    exclusive_region_2 = {
        "coordinates": [
            [
                [1.25, 1.25],
                [1.75, 1.25],
                [1.75, 1.75],
                [1.25, 1.75],
                [1.25, 1.25],
            ]
        ],
        "type": "Polygon",
    }

    facilities_data = [
        {
            "id": "1",
            "name": "FC1",
            "location": {"lat": 1.0, "lng": 1.0},
            "demand": {"min": 3},
            "exclusive_region": exclusive_region_1,
        },
        {
            "id": "2",
            "name": "FC2",
            "location": {"lat": 3.0, "lng": 3.0},
            "demand": {"min": 3, "max": 6},
            "exclusive_region": exclusive_region_2,
        },
    ]

    return [Facility(**data) for data in facilities_data]


@pytest.fixture
def facilities_with_intersecting_exclusive_region():
    exclusive_region_1 = {
        "coordinates": [
            [
                [2.25, 2.25],
                [2.75, 2.25],
                [2.75, 2.75],
                [2.25, 2.75],
                [2.25, 2.25],
            ]
        ],
        "type": "Polygon",
    }

    facilities_data = [
        {
            "id": "1",
            "name": "FC1",
            "location": {"lat": 1.0, "lng": 1.0},
            "demand": {"min": 3},
            "exclusive_region": exclusive_region_1,
        },
        {
            "id": "2",
            "name": "FC2",
            "location": {"lat": 3.0, "lng": 3.0},
            "demand": {"min": 3, "max": 6},
            "exclusive_region": exclusive_region_1,
        },
    ]

    return [Facility(**data) for data in facilities_data]


@pytest.fixture
def location_problem(clients_in_square, facilities_in_square):
    cost_problem = CostProblem(
        clients=clients_in_square,
        fixed_facilities=facilities_in_square,
        cost_type=CostType.PROXIMITY,
    )
    cost_matrix = compute_cost_matrix(cost_problem)

    return LocationProblem(
        number_new_facilities=1,
        clients=clients_in_square,
        fixed_facilities=facilities_in_square,
        cost_matrix=cost_matrix,
    )


@pytest.fixture
def location_problem_with_exclusive_regions(
    clients_in_square, facilities_with_exclusive_region
):
    cost_problem = CostProblem(
        clients=clients_in_square,
        fixed_facilities=facilities_with_exclusive_region,
        cost_type=CostType.PROXIMITY,
    )
    cost_matrix = compute_cost_matrix(cost_problem)

    return LocationProblem(
        number_new_facilities=1,
        clients=clients_in_square,
        fixed_facilities=facilities_with_exclusive_region,
        cost_matrix=cost_matrix,
    )


@pytest.fixture
def location_problem_with_intersecting_exclusive_regions(
    request, clients_in_square, facilities_with_intersecting_exclusive_region
):
    cost_problem = CostProblem(
        clients=clients_in_square,
        fixed_facilities=facilities_with_intersecting_exclusive_region,
        cost_type=CostType.PROXIMITY,
    )
    cost_matrix = compute_cost_matrix(cost_problem)

    return LocationProblem(
        number_new_facilities=1,
        clients=clients_in_square,
        fixed_facilities=facilities_with_intersecting_exclusive_region,
        cost_matrix=cost_matrix,
    )


def test_optimal_location_problem(location_problem):

    solution = solve_integer_formulation(location_problem=location_problem)

    assert solution.status == SolutionStatus.OPTIMAL


def test_optimal_location_problem_with_exclusive_regions(
    location_problem_with_exclusive_regions,
):

    solution = solve_integer_formulation(
        location_problem=location_problem_with_exclusive_regions
    )

    assert solution.status == SolutionStatus.OPTIMAL


def test_optimal_location_problem_with_intersecting_exclusive_regions(
    location_problem_with_intersecting_exclusive_regions,
):
    solution = solve_integer_formulation(
        location_problem=location_problem_with_intersecting_exclusive_regions
    )

    assert solution.status == SolutionStatus.INFEASIBLE
    assert "Impossible solve the problem!" in solution.message


def test_infeasible_location_problem(location_problem):
    """
    When there are no available places to locate the new facility,
    the problem is infeasible
    """
    exclusive_region = {
        "coordinates": [
            [
                [0.0, 0.0],
                [0.0, 4.0],
                [4.0, 4.0],
                [0.0, 4.0],
                [0.0, 0.0],
            ]
        ],
        "type": "Polygon",
    }
    location_problem.fixed_facilities[0].exclusive_region = (
        field_to_valid_multipolygon(field=exclusive_region)
    )

    solution = solve_integer_formulation(location_problem=location_problem)

    assert solution.status == SolutionStatus.INFEASIBLE
    assert "Demonstrated that problem is infeasible" in solution.message


def test_solve_facility_location(clients, facilities):

    request = LocationRequest(
        number_new_facilities=1,
        clients=clients,
        fixed_facilities=facilities,
    )

    location_solution = solve_facility_location(location_request=request)

    assert location_solution.status == SolutionStatus.OPTIMAL
    assert len(location_solution.facilities) == 4
    assert sum(
        facility.demand.expected for facility in location_solution.facilities
    ) == sum(client.demand for client in clients)
