from src.models import Client
from src.services import cluster_clients


def test_client_clustering(clients):
    number_clusters = 10
    total_client_demand = sum(client.demand for client in clients)
    clustered_clients = cluster_clients(clients, number_clusters)

    assert len(clustered_clients) == number_clusters
    assert all(isinstance(client, Client) for client in clustered_clients)
    assert all(client.demand > 0 for client in clustered_clients)
    assert all(client.location is not None for client in clustered_clients)
    assert (
        sum(client.demand for client in clustered_clients)
        == total_client_demand
    )

    clustered_clients = cluster_clients(clients, number_clusters=len(clients))
    assert clustered_clients == clients
