from pydantic import BaseModel, Field

from src.models import Client, CostType, Facility


class LocationRequest(BaseModel):
    """Request model for the locate endpoint."""

    cost_type: CostType = CostType.PROXIMITY
    number_new_facilities: int = Field(ge=1)
    fixed_facilities: list[Facility] = []
    number_client_clusters: int = Field(ge=1, default=300)
    clients: list[Client] = Field(min_length=1)
