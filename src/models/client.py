from pydantic import BaseModel, PositiveFloat

from src.models import Location


class Client(BaseModel):
    """Model representing a client."""

    id: str
    location: Location
    demand: PositiveFloat = 1.0
