import numpy as np
from sklearn.cluster import MiniBatchKMeans

from src.models import Client, Location


def cluster_clients(
    clients: list[Client], number_clusters: int
) -> list[Client]:
    """Cluster the clients into a given number of clusters using KMeans."""

    if number_clusters >= len(clients):
        return clients

    client_locations = np.array(
        [client.location.to_list() for client in clients]
    )
    kmeans = MiniBatchKMeans(n_clusters=number_clusters, n_init=1).fit(
        client_locations
    )

    clustered_clients: list[Client] = []
    for label in range(number_clusters):
        client_indices = np.nonzero(kmeans.labels_ == label)[0]
        if not client_indices.size:
            continue

        cluster_demand = sum([clients[j].demand for j in client_indices])
        cluster_center_lat, cluster_center_lng = kmeans.cluster_centers_[label]
        clustered_clients.append(
            Client(
                id=f"client_cluster_{label}",
                demand=cluster_demand,
                location=Location(
                    lat=cluster_center_lat, lng=cluster_center_lng
                ),
            )
        )

    return clustered_clients
