from src.models import Client, Location


def test_client_model(clients_data):
    clients = [Client(**data) for data in clients_data]

    assert all(isinstance(client, Client) for client in clients)
    assert all(isinstance(client.id, str) for client in clients)
    assert all(isinstance(client.location, Location) for client in clients)
    assert all(client.demand > 0 for client in clients)
