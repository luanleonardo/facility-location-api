import orjson
import pytest

from src.models import Client, CostProblem, CostType, Facility, LocationProblem
from src.services import compute_cost_matrix

CLIENTS_FILE = "data/json/clients.json"
FACILITIES_FILE = "data/json/facilities.json"


@pytest.fixture
def clients_data():
    with open(CLIENTS_FILE) as file:
        return orjson.loads(file.read())


@pytest.fixture
def clients(clients_data):
    return [Client(**data) for data in clients_data]


@pytest.fixture
def facilities_data():
    with open(FACILITIES_FILE) as file:
        return orjson.loads(file.read())


@pytest.fixture
def facilities(facilities_data):
    return [Facility(**data) for data in facilities_data]


@pytest.fixture
def location_problem(request, facilities, clients):
    cost_problem = CostProblem(
        clients=clients[:10],
        fixed_facilities=facilities,
        cost_type=CostType.PROXIMITY,
    )
    cost_matrix = compute_cost_matrix(cost_problem)

    return LocationProblem(
        number_new_facilities=1,
        clients=clients[:10],
        fixed_facilities=facilities,
        cost_matrix=cost_matrix,
    )
