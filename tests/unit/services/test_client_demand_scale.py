from math import isclose

from src.services import scale_demands


def test_scale_clients_demands(clients):

    original_total_demand = sum(client.demand for client in clients)
    expected_new_total_demand = 3 * original_total_demand
    scaled_clients = scale_demands(clients, expected_new_total_demand)
    new_total_demand = sum(client.demand for client in scaled_clients)

    assert isclose(new_total_demand, expected_new_total_demand)
