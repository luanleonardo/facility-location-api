import numpy as np

from src.services import spherical_cost_matrix


def test_spherical_distance_matrix():

    sources = np.array([[-23.456, -46.456]])
    destinations = np.array([[-23.456, -46.456], [-23.789, -46.789]])

    distance_matrix = spherical_cost_matrix(sources, destinations)

    assert distance_matrix.shape == (1, 2)


def test_spherical_distance_matrix_km():
    """
    Calculate the distance between the Ezeiza Airport (Buenos
    Aires, Argentina) and the Charles de Gaulle Airport (Paris, France).

    References
    ----------
    [1] Haversine distance,
    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html
    """

    bsas = np.array([[-34.83333, -58.5166646]])
    paris = np.array([[49.0083899664, 2.53844117956]])
    expected_distance_in_km = 11099.54035582

    distance_matrix_meters = spherical_cost_matrix(
        sources=bsas, destinations=paris
    )

    assert distance_matrix_meters.shape == (1, 1)
    assert np.isclose(
        distance_matrix_meters[0, 0] / 1000, expected_distance_in_km, atol=1e-2
    )
