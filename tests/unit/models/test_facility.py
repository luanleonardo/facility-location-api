from uuid import uuid4

import pytest
from pydantic import ValidationError
from shapely import MultiPolygon

from src.models import Facility, Location

INVALID_GEOJSON = [
    None,
    dict(),
    {"type": "FeatureCollection"},
    {"type": "FeatureCollection", "features": [{"geometry": {}}]},
    {
        "type": "FeatureCollection",
        "features": [{"geometry": {"coordinates": []}}],
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        -60.0134114599588,
                        -3.0916188609801765,
                    ],
                    "type": "Point",
                },
            }
        ],
    },
    {
        "type": "Polygon",
        "coordinates": [[[0.5, 0.75], [0.25, 0.5], [0.5, 0.75]]],
    },
]


def test_facility_model(facilities_data):
    """Test the facility model"""

    facilities = [Facility(**data) for data in facilities_data]
    facilities.append(
        Facility(
            **{
                "id": str(uuid4()),
                "name": "Facility 4",
                "location": {
                    "lat": -3.0905742061991424,
                    "lng": -59.985171470760335,
                },
                "demand": {"min": 5, "max": 10},
                "exclusive_region": MultiPolygon(),
            }
        )
    )
    facilities.append(
        Facility(
            **{
                "id": str(uuid4()),
                "name": "Facility 5",
                "demand": {"min": 10, "max": 100},
                "location": {
                    "lat": -3.1073436323084693,
                    "lng": -60.000580791394405,
                },
                "exclusive_region": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-59.992440783859905, -3.127959087842271],
                            [-59.992440783859905, -3.129075136040683],
                            [-59.99012932088348, -3.129075136040683],
                            [-59.99012932088348, -3.127959087842271],
                            [-59.992440783859905, -3.127959087842271],
                        ]
                    ],
                },
            }
        )
    )
    facilities.append(
        Facility(
            **{
                "id": str(uuid4()),
                "name": "Facility 6",
                "demand": {"min": 10, "max": 100},
                "location": {
                    "lat": -3.1073436323084693,
                    "lng": -60.000580791394405,
                },
                "exclusive_region": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [
                                    [
                                        [
                                            -59.992440783859905,
                                            -3.127959087842271,
                                        ],
                                        [
                                            -59.992440783859905,
                                            -3.129075136040683,
                                        ],
                                        [
                                            -59.99012932088348,
                                            -3.129075136040683,
                                        ],
                                        [
                                            -59.99012932088348,
                                            -3.127959087842271,
                                        ],
                                        [
                                            -59.992440783859905,
                                            -3.127959087842271,
                                        ],
                                    ]
                                ],
                            },
                        }
                    ],
                },
            }
        )
    )

    assert all(isinstance(facility, Facility) for facility in facilities)
    assert all(
        isinstance(facility.exclusive_region, MultiPolygon)
        for facility in facilities
    )
    assert all(facility.demand.min >= 0 for facility in facilities)
    assert all(facility.demand.max >= 0 for facility in facilities)


def test_exclusive_region_serializer():
    """Test the serializer for the exclusive service area of a facility"""

    facility = Facility(
        id=str(uuid4()),
        name="Facility 6",
        location=Location(lat=-3.0882045980707225, lng=-59.96466874582786),
    )

    expected_geojson = {
        "coordinates": [],
        "type": "MultiPolygon",
    }

    assert facility.model_dump()["exclusive_region"] == expected_geojson


@pytest.mark.parametrize("geojson", INVALID_GEOJSON)
def test_exclusive_region_validator(geojson):
    """Test the validator for the exclusive service area of a facility"""

    facility_data = {
        "id": "7",
        "name": "Facility 7",
        "demand": {"min": 5, "max": 10},
        "location": {"lat": -3.123, "lng": -60.014},
        "exclusive_region": geojson,
    }

    with pytest.raises(
        ValidationError,
        match="Not a valid GeoJSON dictionary or valid geometry.",
    ):
        Facility(**facility_data)
