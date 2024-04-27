import orjson
from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeFloat,
    field_serializer,
    field_validator,
)
from shapely import MultiPolygon, to_geojson

from src.models import Location
from src.utils import field_to_valid_multipolygon


class Demand(BaseModel):
    """Model representing the demand of a facility."""

    min: NonNegativeFloat = 0.0
    expected: NonNegativeFloat = 0.0
    max: NonNegativeFloat = 0.0


class Facility(BaseModel):
    """Model representing a facility."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    id: str
    name: str
    demand: Demand = Demand()
    location: Location
    exclusive_region: MultiPolygon = MultiPolygon()

    @field_serializer("exclusive_region")
    def exclusive_region_serializer(self, field: MultiPolygon) -> dict:
        return orjson.loads(to_geojson(field))

    @field_validator("exclusive_region", mode="before")
    @classmethod
    def exclusive_region_validator(
        cls, field: dict | MultiPolygon
    ) -> MultiPolygon:
        return field_to_valid_multipolygon(field=field)
