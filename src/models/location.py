from pydantic import BaseModel


class Location(BaseModel):
    """Model representing a location."""

    lat: float
    lng: float

    def to_list(self, reverse: bool = False) -> list[float]:
        if reverse:
            return [self.lng, self.lat]
        return [self.lat, self.lng]
