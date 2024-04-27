from copy import deepcopy

from src.models import Client


def scale_demands(
    clients: list[Client], new_total_demand: float
) -> list[Client]:
    """Scale the demands of the clients to a new total demand."""

    clients_copy = deepcopy(clients)
    original_total_demand = sum(client.demand for client in clients)
    scale_factor = new_total_demand / original_total_demand

    for client in clients_copy:
        client.demand = round(scale_factor * client.demand, ndigits=2)

    return clients_copy
